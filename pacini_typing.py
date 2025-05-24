#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Main entry point for the Pacini-Typing pipeline
This script is responsible for calling all operations
of the application in the correct order.

Operations are performed in the following order:
    - Parsing all arguments into a dictionary
    - Setup logging format and level
    - Retrieve the input files based on args
    - Check for zipped .gz files
    - Validate input arguments
    - If makedatabase option is selected:
        - Run makedatabase operation
    - If query or config option is selected:
        - Get file type of input file(s)
        - Start the query related operations
        - Start the config related operations

The run() function is the main method of the class.
This function can accept arguments on two ways:

    1. For test purposes, arguments can be provided as a list.
        Arguments will be parsed, but not based on sys.argv.

    2. For normal runs, provided_args is None and
        sys.argv is used for parsing arguments.
----------
For help:

    python3 pacini_typing.py -h

Or:
    pacini_typing -h

See the README.md file for more specific information.
----------
"""

__author__ = "Mark van de Streek"
__date__ = "2024-09-27"
__all__ = ["PaciniTyping", "main"]

import argparse
import gzip
import logging
import os
import shutil
import sys
import tarfile
from typing import Any

import preprocessing.argsparse.build_parser
from handle_search_modes import HandleSearchModes
from make_gene_database import GeneDatabaseBuilder
from parsing.parsing_manager import ParsingManager
from parsing.read_config_pattern import ReadConfigPattern
from preprocessing.exceptions.determine_input_type_exceptions import (
    InvalidSequencingTypesError,
)
from preprocessing.exceptions.validate_database_exceptions import (
    InvalidDatabaseError,
)
from preprocessing.validation.determine_input_type import InputFileInspector
from preprocessing.validation.validate_database import check_for_database_path
from preprocessing.validation.validating_input_arguments import ArgsValidator
from queries.query_runners import run_gene_query

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-5s %(process)d : %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)


class PaciniTyping:
    """
    Main class for the Pacini-Typing application.
    ----------
    Methods:
        - parse_all_args: Parse all arguments into a dictionary
        - setup_logging: Setup logging format and level
        - get_input_filenames: Retrieve the input files based on args
        - check_for_unzip_files: Check for zipped .gz files
        - validate_file_arguments: Validate input arguments
        - run_makedatabase: Run the makedatabase operation
        - get_file_type: Get file type of input file(s)
        - check_valid_option_with_args: Check if file type is correct
        - initialize_config_pattern: Initialize the ReadConfigPattern class
        - save_intermediates: Save intermediate files in a zip archive
        - delete_intermediates: Delete intermediate files
        - handle_makedatabase_option: Handle the makedatabase option
        - handle_config_or_query_option: Handle the config or query option
        - handle_config_option: Handle all config related operations
        - handle_config_option_parse_query: Parse the query operation
        - handle_query_option: Handle all query related operations
        - run: Main start point for the Pacini-Typing pipeline
    ----------
    """

    def __init__(self, input_args: argparse.Namespace) -> None:
        """
        Constructor for the PaciniTyping class.
        The constructor accepts the input arguments from argparse.
        All arguments and additional information are
        stored in the self.option variable, and
        other variables are set for type hinting.
        ----------
        Input:
            - input_args: argparse.Namespace object with parsed arguments
        ----------
        """
        self.input_args = input_args
        self.option: dict[str, Any] = {}
        self.sample_name: str = ""
        self.file_type: str = ""
        self.threads: int = self.input_args.threads
        self.output_dir = None

    def parse_all_args(self) -> None:
        """
        Function that parses all arguments into a dictionary.
        The arguments are grouped together with the args options.
        self.option is also used to store more information that
        is needed along the way.
        """
        logging.debug("Parsing all args and necessary information...")
        self.set_general_attributes()
        if self.input_args.options == "query":
            self.set_query_attributes()
        elif self.input_args.options == "makedatabase":
            self.set_makedatabase_attributes()
        elif self.input_args.options is None:
            self.set_config_attributes()

    def set_general_attributes(self) -> None:
        """
        Function that sets the general attributes of the self.option variable.
        This is a variable that is used throughout the application with mostly
        incoming user arguments.
        With general attributes, we mean attributes that are used
        in all operations of the application.
        """
        logging.debug("Parsing general attributes...")
        self.option = {
            "database_path": (
                self.input_args.database_path
                if hasattr(self.input_args, "database_path")
                else None
            ),
            "database_name": (
                self.input_args.database_name
                if hasattr(self.input_args, "database_name")
                else None
            ),
            "option": self.input_args.options,
            "verbose": self.input_args.verbose,
            "run_path": os.path.abspath(__file__).rsplit(".", 1)[0],
            "query": None,
            "makedatabase": None,
        }

    def set_query_attributes(self) -> None:
        """
        Function that sets the query related attributes
        in the self.option variable.
        """
        logging.debug("Parsing query-related attributes...")
        self.option["query"] = {
            "paired": self.input_args.paired,
            "single": self.input_args.single,
            "output": self.input_args.output,
        }

    def set_makedatabase_attributes(self) -> None:
        """
        Function that sets the makedatabase related attributes
        in the self.option variable.
        """
        logging.debug("Parsing makedatabase-related attributes...")
        self.option["makedatabase"] = {
            "database_type": self.input_args.database_type,
            "input": self.input_args.input_file,
        }

    def set_config_attributes(self) -> None:
        """
        Function that sets the config-scheme related attributes
        in the self.option variable.
        """
        logging.debug("Parsing config-related attributes...")
        self.option["config"] = {
            "input": self.input_args.input,
            "config_path": self.input_args.config,
            "fasta_out": self.input_args.fasta_out,
            "search_mode": self.input_args.search_mode,
        }

    def setup_logging(self) -> None:
        """
        Simple method to set up the logging level.
        If user has selected verbose (args), the logging level is set to DEBUG.
        Otherwise, the logging level is set to INFO.
        Additionally, if the log_file option is selected,
        a log file is created with the name pacini_typing.log.
        """
        logging.debug("Setting up logging-level")
        logging.getLogger().setLevel(
            self.option["verbose"] and logging.DEBUG or logging.INFO
        )
        if self.input_args.log_file:
            logging.debug("--log-file option selected, setting up log file...")
            file_handler = logging.FileHandler("pacini_typing.log")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)-5s %(process)d : %(message)s",
                    datefmt="%Y-%m-%dT%H:%M:%S",
                )
            )
            logging.getLogger().addHandler(file_handler)

    def get_input_filenames(self) -> None:
        """
        Function that, based on the input options,
        retrieves the right input files.

        using sub-options in argparse,
        arguments are stored in sub-variables:
            - args.query holds all options/args related to query
            - args.makedatabase holds all options/args related to makedatabase
        This means if you want to retrieve the input files,
        you must always check which sub-option is selected
        otherwise you will get an error.

        Therefore, the input files are once stored in a list,
        which is stored in the self.option variable and could
        be used throughout the application.
        """
        logging.debug("Retrieving input filenames from selected option...")
        input_files_list: list[str] = []
        if self.option["query"]:
            if self.option["query"]["single"]:
                input_files_list.append(self.option["query"]["single"])
            elif self.option["query"]["paired"]:
                input_files_list.extend(self.option["query"]["paired"])
        elif self.option["makedatabase"]:
            input_files_list.append(self.option["makedatabase"]["input"])
        # Double check if the config option is really the only option
        elif self.option["config"] and self.option["option"] is None:
            input_files_list.extend(self.option["config"]["input"])
        logging.debug("Input files have been retrieved: %s", input_files_list)
        logging.debug("Adding input files to the args variable...")
        self.option["input_file_list"] = input_files_list

    def retrieve_sample_name(self) -> None:
        """
        Function that retrieves the sample name from the input file.
        The sample name is the first part of the filename.
        """
        logging.debug("Retrieving the sample name from the input file...")
        self.sample_name = (
            self.option["input_file_list"][0]
            .split("/")[-1]
            .split(".")[0]
            .replace("_1", "")
            .replace("_pR1", "")
        )

    def check_for_unzip_files(self) -> None:
        """
        Small function that checks the input files for .gz files.
        if present, the files are placed in a list.
        This list is then passed to the unzip_gz_files function.
        See the unzip_gz_files function for more information.
        """
        logging.debug("Checking for .gz files in the input list...")
        gz_files = [
            file
            for file in self.option["input_file_list"]
            if file.endswith(".gz")
        ]
        if gz_files:
            logging.info("Found files that need to be unzipped, unzipping...")
            self.unzip_gz_files(gz_files)

    def unzip_gz_files(self, gz_files: list[str]) -> None:
        """
        Function that unzips .gz files.
        Files are being opened in binary mode and copied to a new file.
        The new file is the original file without the .gz extension.
        The input file list is then updated with the new files,
        minus the .gz extension.
        ----------
        Input:
            - gz_files: list with .gz files
        Raises:
            -gzip.BadGzipFile: Error while unzipping file,
                exits the program
        ----------
        """
        logging.debug("Unzipping files %s...", gz_files)
        for file in gz_files:
            try:
                with gzip.open(file, "rb") as f_in:
                    with open(file[:-3], "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
            except gzip.BadGzipFile as e:
                logging.error("Error while unzipping file %s: %s", file, e)
                sys.exit(1)
        logging.debug("Updating input file list with unzipped files")
        self.option["input_file_list"] = [
            file[:-3] if file in gz_files else file
            for file in self.option["input_file_list"]
        ]

    def validate_file_arguments(self) -> None:
        """
        Function that calls the validation of the input arguments.
        The ArgsValidator class is used to validate.
        This Class can be found in validation/validating_input_arguments.py
        For more in dept information about the validation,
        see the ArgsValidator class.

        The validation methods raise specific error exceptions,
        if the validation fails outside of this exceptions,
        something bigger is wrong and the program will exit.
        ----------
        Raises:
            - Every validation has his own error Exception class with
                explanation and suggestion.
            - If the program fails here, something bigger is wrong.
            - The program will exit with code 1.
        ----------
        """
        logging.debug("Validating the input arguments...")
        argsvalidator = ArgsValidator(self.option)
        if argsvalidator.validate():
            logging.info(
                "Input arguments have been validated, found no issues..."
            )
        else:
            logging.error(
                "Error while validation the input arguments, "
                "please check the above logs for more information."
            )
            sys.exit(1)

    def run_makedatabase(self, database_creation_args: dict[str, Any]) -> None:
        """
        Function that runs the makedatabase operation.
        The DatabaseBuilder of the make_gene_database.py is called.
        """
        logging.info("Creating the reference database...")
        GeneDatabaseBuilder(database_creation_args)

    def get_file_type(self) -> None:
        """
        Function that calls the FileValidator class.
        This class is responsible for determining the
        input file type.
        This file type is either FASTA or FASTQ.
        The file type is stored in the self.option variable
        See validation/determine_input_type.py for more information.
        """
        logging.debug("Determining the file type of the input file(s)...")
        self.file_type = InputFileInspector(
            self.option["input_file_list"]
        ).get_file_type()
        logging.info(
            "The input file type has been determined: %s",
            self.file_type,
        )

    def check_valid_option_with_args(self) -> None:
        """
        This method checks if the file type is correct for the input arguments.
        To be precise, it checks if the file type is FASTA for single file input
        and FASTQ for paired files. If not, it will exit the program.
        This method is called after the file type has been determined.
        ----------
        Raises:
            - InvalidSequencingTypesError: Wrong file type for input arguments
        ----------
        """
        logging.debug(
            "Checking if the file type is correct for the input arguments..."
        )
        if (
            len(self.option["input_file_list"]) == 1
            and self.file_type == "FASTQ"
        ) or (
            len(self.option["input_file_list"]) == 2
            and self.file_type == "FASTA"
        ):
            logging.error(
                "Only FASTA files are allowed for single files "
                "and only FASTQ files are allowed for paired files."
            )
            raise InvalidSequencingTypesError(self.option["input_file_list"])

    def check_valid_gene_database_path(
        self, database_builder: dict[str, Any]
    ) -> bool:
        """
        Function that calls the validation operation for the database.
        This function is responsible for checking if the database exists.
        The database_builder dictionary is required for the re-use of
        this method with different parameters.
        ----------
        Input:
            - database_builder: Dictionary with all necessary information
        Output:
            - True: If the database exists
            - False: If the database does not exist
        ----------
        """
        logging.debug("Checking if the database exists...")
        return check_for_database_path(database_builder)

    def initialize_config_pattern(self) -> ReadConfigPattern:
        """
        Function that initializes the ReadConfigPattern class.
        This class is responsible for reading the configuration file
        It also sets the required information for the makedatabase
        and query operation.
        ----------
        Output:
            - pattern: ReadConfigPattern object
        ----------
        """
        logging.debug("Initializing the configuration file...")
        pattern = ReadConfigPattern(
            self.option["config"]["config_path"],
            self.file_type,
            self.option["config"]["search_mode"],
        )
        # Additionally, the query input and output must be set.
        # The output is not specified by the user, because
        # this is based on the input files.
        logging.debug(
            "Setting additional information for the configuration..."
        )
        pattern.creation_dict["input_file_list"] = self.option["config"][
            "input"
        ]
        pattern.creation_dict["file_type"] = self.file_type
        pattern.creation_dict["output"] = (
            pattern.pattern["global_settings"]["run_output"] + self.sample_name
        )

        pattern.creation_dict["input_fasta_file"] = os.path.join(
            os.path.dirname(self.option["run_path"]),
            pattern.creation_dict["input_fasta_file"],
        )
        # Set threads for creation operations (makeblastdb/query)
        pattern.creation_dict["threads"] = self.threads
        # Store the fasta-output option in the pattern object
        pattern.pattern["fasta_out"] = self.option["config"]["fasta_out"]

        return pattern

    def handle_intermediate_saving(
        self, gene_output_dir: str, run_output_snps: str
    ) -> None:
        """
        Little helper function that contains some logic for saving
        intermediate files. In some sitations, the gene_output_dir
        or run_output_snps are the same or subdirectories of each other.
        Therefore, this checking is helpful to avoid wrong saving.
        ----------
        Input:
            - gene_output_dir: The output directory of the gene run
            - run_output_snps: The output directory of the SNP run
        ----------
        """
        if gene_output_dir == run_output_snps:
            self.save_intermediates(gene_output_dir)
        elif run_output_snps.startswith(gene_output_dir):
            self.save_intermediates(gene_output_dir)
        elif gene_output_dir.startswith(run_output_snps):
            self.save_intermediates(run_output_snps)
        else:
            self.save_intermediates(
                gene_output_dir,
                f"{self.sample_name}_intermediates_gene.tar.gz",
            )
            self.save_intermediates(
                run_output_snps, f"{self.sample_name}_intermediates_SNP.tar.gz"
            )

    def save_intermediates(
        self,
        output_dir: str,
        zip_name: str | None = None,
    ) -> None:
        """
        Function that saves intermediate files in a zip archive.
        The zip archive is named after the sample name.
        The zip format is .tar.gz.
        ----------
        Input:
            - output_dir: The output directory of the run
        ----------
        """
        if zip_name is None:
            zip_name = f"{self.sample_name}_intermediates.tar.gz"
        logging.info("Saving intermediate files in a zip archive...")
        with tarfile.open(zip_name, "w:gz") as tar:
            tar.add(output_dir, arcname=os.path.basename(output_dir))
        # Call the delete_intermediates function to
        # remove the original output directory
        logging.debug("Saved intermediate files in a zip...")
        self.delete_intermediates(output_dir)

    def delete_intermediates(self, output_dir: str) -> None:
        """
        Function that removes the intermediate files of a run,
        using the shutil module.
        ----------
        Input:
            - output_dir: The output directory of the run
                (either gene or SNP)
        ----------
        """
        logging.debug("Deleting intermediate files if they exist...")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        else:
            logging.debug(
                "Directory %s does not exist, skipping deletion", output_dir
            )

    def save_or_delete_intermediate(self, pattern: ReadConfigPattern):
        """
        Function that determines if the intermediate files of the run
        should be saved or deleted.
        The actual saving or deleting is delegated to other functions.
        ----------
        Input:
            - pattern: The configuration file options
        ----------
        """
        search_mode: str = self.option["config"]["search_mode"]
        if search_mode in ["both", "SNPs"]:
            run_output_snps = pattern.pattern["global_settings"][
                "run_output_snps"
            ]
        gene_output_dir: str = pattern.pattern["global_settings"]["run_output"]

        if self.input_args.save_intermediates:
            if search_mode == "both":
                self.handle_intermediate_saving(
                    gene_output_dir, run_output_snps
                )
            elif search_mode == "SNPs":
                self.save_intermediates(
                    run_output_snps,
                    f"{self.sample_name}_intermediates_SNP.tar.gz",
                )
                self.delete_intermediates(gene_output_dir)
            elif search_mode == "genes":
                self.save_intermediates(
                    gene_output_dir,
                    f"{self.sample_name}_intermediates_gene.tar.gz",
                )
        else:
            if search_mode == "both":
                self.delete_intermediates(gene_output_dir)
                self.delete_intermediates(run_output_snps)
            elif search_mode == "SNPs":
                self.delete_intermediates(run_output_snps)
            elif search_mode == "genes":
                self.delete_intermediates(gene_output_dir)

    def handle_makedatabase_option(self) -> None:
        """
        Little helper function to split up functionality.
        This function simply defines the database_builder dictionary
        and runs the run_makedatabase() method.
        The run_makedatabase() method is re-used by other modules later on,
        that's why this pattern is defined in this helper function.
        """
        logging.info(
            "Defining all necessary information for the database creation..."
        )
        database_builder = {
            "database_path": self.option["database_path"],
            "database_name": self.option["database_name"],
            "database_type": self.option["makedatabase"]["database_type"],
            "input_fasta_file": self.option["makedatabase"]["input"],
        }
        self.run_makedatabase(database_builder)

    def handle_config_or_query_option(self) -> None:
        """
        Function that handles the config or query option.
        It decides which operation to run based on the input arguments.
        """
        if self.option["query"]:
            logging.info("Query option selected, starting query operation...")
            self.handle_query_option()
        else:
            # The query option is not selected,
            # which means the config is selected.
            logging.info(
                "Config option selected, starting the configuration..."
            )
            self.handle_config_option()

    def handle_config_option(self) -> None:
        """
        Function that handles the calling of all the config
        related operations.
        The reading of the config file is first delegated to the
        ReadConfigPattern class.
        Then, the handler object is created with the pattern and
        the main self.option variable, of which the search mode
        is extracted.
        The handler object makes sure the databases are checked,
        and the query is executed in the correct runner.
        """
        pattern: ReadConfigPattern = self.initialize_config_pattern()
        handler: HandleSearchModes = HandleSearchModes(pattern, self.option)
        handler.handle()
        self.filter_and_parse_results(pattern)

    def filter_and_parse_results(self, pattern: ReadConfigPattern) -> None:
        """
        Function that handles the parsing of the genetic variation
        that is found by the query operation.
        The ParsingManager class is called with the right parameters.
        After parsing, the function makes a decision to save or delete
        the intermediate files based on the input arguments.
        ----------
        Input:
            - pattern: The configuration file options
        ----------
        """
        logging.info("Starting the parsing operation...")
        ParsingManager(
            pattern,
            self.file_type,
            self.sample_name,
            self.option["config"]["search_mode"],
        )
        # Determine if the intermediate files should be saved or deleted
        self.save_or_delete_intermediate(pattern)

    def handle_query_option(self) -> None:
        """
        Method that handles all query related operations.
        The function checks if the database exists,
        right before the query searching called.
        If the database does not exist, the program will exit.
        ----------
        Raises:
            - InvalidDatabaseError: Database existence check failed
        ----------
        """
        logging.debug(
            "Defining all necessary information for the query operation..."
        )
        query_builder: dict[str, Any] = {
            "file_type": self.file_type,
            "input_file_list": self.option["input_file_list"],
            "database_path": self.option["database_path"],
            "database_name": self.option["database_name"],
            "output": self.option["query"]["output"],
            "threads": self.threads,
        }
        if self.check_valid_gene_database_path(query_builder):
            run_gene_query(query_builder)
        else:
            raise InvalidDatabaseError(
                query_builder["database_name"],
                query_builder["file_type"],
            )

    def run(self) -> None:
        """
        Run method of the PaciniTyping class.
        This method calls all other methods in the correct order.
        After all preprocessing actions are done,
        this function will split if the makedatabase option is selected.
        Otherwise, the config or query option is selected.
        """
        self.parse_all_args()
        self.setup_logging()
        self.get_input_filenames()
        self.retrieve_sample_name()
        self.check_for_unzip_files()
        self.validate_file_arguments()

        if self.option["makedatabase"]:
            self.handle_makedatabase_option()
        else:
            self.get_file_type()
            self.check_valid_option_with_args()
            self.handle_config_or_query_option()


def main(provided_args: list[str] | None = None) -> None:
    """
    Main entry point for the Pacini-Typing application
    that initiates the pipeline.

    If using (unit)tests, there is no sys.argv, so the provided_args are used.
    Otherwise, sys.argv is used to parse the arguments.
    ----------
    Input:
        - provided_args: list with arguments for testing purposes or None
    ----------
    """
    if provided_args:
        args = preprocessing.argsparse.build_parser.main(provided_args)
    else:
        args = preprocessing.argsparse.build_parser.main(sys.argv[1:])

    pacini_typing = PaciniTyping(args)
    pacini_typing.run()
    logging.info("Pacini-typing pipeline has finished successfully!")


if __name__ == "__main__":
    logging.info("Starting Pacini-typing, parsing arguments...")
    main()
