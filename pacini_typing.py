#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Main entry point for the Pacini-Typing pipeline
This script is responsible for parsing command-line arguments and
initiating the pipeline.

Operations are performed in the following order:
    - Parsing all arguments into a dictionary
    - Setup logging format and level
    - Retrieve the input files based on args
    - Check for zipped .gz files
    - Validate input arguments
    - If makedatabase option is selected:
        - Run makedatabase operation
    - If query option is selected:
        - Get file type of input file(s)
        - Check if args options are valid for the file type
        - Check database existence
        - Run query

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

See the README.md file for more information about the pipeline
----------
"""

from __future__ import annotations

__author__ = "Mark van de Streek"
__data__ = "2024-10-24"
__all__ = ["PaciniTyping", "main"]

import argparse
import gzip
import logging
import os
import shutil
import sys
from typing import Any, Tuple

import preprocessing.argsparse.build_parser
from makedatabase import DatabaseBuilder
from parsing.config_manager import ParsingManager
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
from queries.query_runner import QueryRunner

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-5s %(process)d : %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)


class PaciniTyping:
    """
    Main class for the Pacini-Typing pipeline.
    This class is respsonsible for calling operations in the correct order.
    ----------
    Input:
        - input_args: argparse.Namespace object with parsed arguments

    Methods:
        - parse_all_args: Parse all arguments into a dictionary
        - setup_logging: Setup logging format and level
        - get_input_filenames: Retrieve the input files based on args
        - check_for_unzip_files: Check for zipped .gz files
        - validate_file_arguments: Validate input arguments
        - run_makedatabase: Run the makedatabase operation
        - get_file_type: Get file type of input file(s)
        - check_valid_option_with_args: Check if args options are valid for the file type
        - check_valid_database_path: Check database existence
        - run_query: Run query
        - run: Main method to run the pipeline
    ----------
    """

    def __init__(self, input_args: argparse.Namespace) -> None:
        """
        Constructor for the PaciniTyping class.
        The contstructor accepts the parsed input arguments from argparse.
        The input arguments are stored in the input_args attribute.
        All arguments and aditional information are
        stored in the self.option variable.
        The run method is responsible for calling all other methods.
        ----------
        Input:
            - input_args: argparse.Namespace object with parsed arguments
        ----------
        """
        self.input_args = input_args
        self.option: dict[str, Any] = {}
        self.sample_name: str = ""
        self.file_type: str = ""

    def parse_all_args(self) -> None:
        """
        Method to parse all arguments into a dictionary.
        The arguments are grouped together with the args options.
        The run_path is needed for operations that
        require a path to certain files.
        self.option is also used to store more information.
        """
        logging.debug(
            "Placing all args and necessary information in a dictionary"
        )
        self.set_general_attributes()
        if self.input_args.options == "query":
            self.set_query_attributes()
        elif self.input_args.options == "makedatabase":
            self.set_makedatabase_attributes()
        elif self.input_args.options is None:
            self.set_config_attributes()

    def set_general_attributes(self):
        """
        Method to set the general attributes.
        It sets the general attributes of the self.option variable.
        This means, some general arguments that coming from argparse are
        stored in the option variable.
        Other specific arguments are parsed in set_query_attributes and
        set_makedatabase_attributes.
        """
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

    def set_query_attributes(self):
        """
        Function that sets the query related attributes.
        The query attributes are stored in the self.option variable.
        These options are used to run the query operation later on.
        """
        self.option["query"] = {
            "paired": self.input_args.paired,
            "single": self.input_args.single,
            "output": self.input_args.output,
            "filters": {
                "identity": self.input_args.identity,
            },
        }

    def set_makedatabase_attributes(self):
        """
        This function sets the makedatabase related attributes.
        The makedatabase attributes are stored in the self.option variable.
        These options are used to run the makedatabase operation manually later on.
        """
        self.option["makedatabase"] = {
            "database_type": self.input_args.database_type,
            "input": self.input_args.input_file,
        }

    def set_config_attributes(self):
        """
        This function comes into play when the config option is selected.
        The config attributes are stored in the self.option variable.
        These options are used to read the config file later on.
        From this config file, the input database and name are retrieved.
        """
        self.option["config"] = {
            "input": self.input_args.input,
            "config_path": self.input_args.config,
        }

    def setup_logging(self) -> None:
        """
        Simple method to setup the logging level.
        If user has selected verbose (args), the logging level is set to DEBUG.
        Otherwise, the logging level is set to INFO.
        """
        logging.debug("Setting up logging-level")
        logging.getLogger().setLevel(
            self.option["verbose"] and logging.DEBUG or logging.INFO
        )
        if self.input_args.log_file:
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
        which is stored in the self.option variable.
        """
        logging.debug("Retrieving input files and placing them in a list")
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
        self.option["input_file_list"] = input_files_list

    def retrieve_sample_name(self) -> None:
        """
        Function that retrieves the sample name from the input file.
        The sample name is the first part of the filename.
        """
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
        logging.debug("Searching for .gz files in the input list")
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
        Function that validates all input arguments.
        This function uses the ArgsValidator class to validate.
        This Class can be found in validation/validating_input_arguments.py
        In this file, in dept comments are provided about the validation.
        ----------
        Error:
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
        This means the DatabaseBuilder of the
        makedatabase.py is called.
        DatabaseBuilder requires a dictionary with the following keys
        - database_path: path to the database
        - database_name: name of the database
        - database_type: type of the database (fasta/fastq)
        - input_fasta_file: input file for the database

        The database_builder variable is needed because
        of the generic re-use of the DatabaseBuilder class later on.

        For more information about the DatabaseBuilder,
        see the makedatabase.py file.
        """
        logging.info("Creating the refernece database...")
        DatabaseBuilder(database_creation_args)

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
        Error:
            - If the program continues with the wrong file type,
                a lot of errors will occur.
            - The program will exit with code 1.
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

    def check_valid_database_path(
        self, database_builder: dict[str, Any]
    ) -> bool:
        """
        Function that calls the check_for_database_path function.
        The validation is done based on the following:
        - database_path: path to the database
        - database_name: name of the database
        - file_type: type of the database (fasta/fastq)

        The check_for_database_builder variable is needed because
        of the generic re-use of the this function later on.

        FASTQ and FASTA require different databases,
        more information can be found in
        validation/validate_database.py
        ----------
        Raises:
            - InvalidDatabaseError: Invalid or not found
        ----------
        """
        logging.debug("Checking if the database exists...")
        return check_for_database_path(arg_options=database_builder)

    def run_query(
        self, query_runner_builder: dict[str, Any]
    ) -> Tuple[str, str] | bool:
        """
        Function that runs the query operation.
        This means the QueryRunner of the query_runner.py is called.
        The self.option variable is passed to the QueryRunner.
        Result of the query is stored in the result variable.
        The QueryRunner class is responsible for running the query operation.
        For more information about the QueryRunner,
        See queries/query_runner.py
        ----------
        Returns:
            - result: Tuple with the result of the query
        ----------
        """
        logging.info("Running the input query against reference database...")
        runner = QueryRunner(run_options=query_runner_builder)
        result = runner.run()
        logging.info("Query finished in: %s seconds", runner.get_runtime())

        return result

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
        logging.debug("Initializing the ReadConfigPattern class...")
        pattern = ReadConfigPattern(
            self.option["config"]["config_path"],
            self.file_type,
        )
        # Additionally, the query input and output must be set.
        # The output is not specified by the user, because
        # this is based on the input files. Therefore,
        # the sample name is retrieved from the input file.
        # This is done in the function retrieve_sample_name().
        pattern.creation_dict["input_file_list"] = self.option["config"][
            "input"
        ]
        pattern.creation_dict["output"] = (
            pattern.pattern["database"]["run_output"] + self.sample_name
        )

        pattern.creation_dict["input_fasta_file"] = os.path.join(
            os.path.dirname(self.option["run_path"]),
            pattern.creation_dict["input_fasta_file"],
        )

        return pattern

    def save_intermediates(self) -> None:
        """
        # TODO: save_intermediates - Fill in later...
        """
        logging.info("Saving intermediate files in a zip archive...")
        os.makedirs(f"{self.sample_name}_intermediates", exist_ok=True)
        shutil.move("databases", f"{self.sample_name}_intermediates")
        shutil.move("output", f"{self.sample_name}_intermediates")
        shutil.make_archive(f"{self.sample_name}_intermediates", "tar")
        shutil.rmtree(f"{self.sample_name}_intermediates")

    def delete_intermediates(self) -> None:
        """
        # TODO: delete_intermediates - Fill in later...
        """
        logging.info("Deleting intermediate files...")
        shutil.rmtree("databases")
        shutil.rmtree("output")

    def run(self) -> None:
        """
        Main start point for the Pacini-Typing pipeline.
        This method calls all other methods in the correct order.
        The order is defined in top-module docstring.
        """
        # Retrieve the args object, arguments have been parsed at this point
        # Place all arguments in a dictionary
        self.parse_all_args()
        # Setup up the logging, i.e., level and format
        self.setup_logging()
        # Get the input files and retrieve the sample name
        self.get_input_filenames()
        self.retrieve_sample_name()
        # Check if they may need to be unzipped
        self.check_for_unzip_files()
        # Validate all input arguments
        self.validate_file_arguments()

        if self.option["makedatabase"]:
            # Define the required database args here,
            # so the run_makedatabase() method can be re-used by
            # other modules later on.
            database_builder = {
                "database_path": self.option["database_path"],
                "database_name": self.option["database_name"],
                "database_type": self.option["makedatabase"]["database_type"],
                "input_fasta_file": self.option["makedatabase"]["input"],
            }
            self.run_makedatabase(database_builder)
        else:
            # The input option is not makedatabase,
            # so it must be query or config.
            # Determine the file type and valid options
            self.get_file_type()
            self.check_valid_option_with_args()
            # Query option has different requirements than config option
            # split up the options and check if the database exists
            if self.option["query"]:
                # Create the right query builder for the query operation
                query_builder: dict[str, Any] = {
                    "file_type": self.file_type,
                    "input_file_list": self.option["input_file_list"],
                    "database_path": self.option["database_path"],
                    "database_name": self.option["database_name"],
                    "output": self.option["query"]["output"],
                }
                # Check if the database exists
                # If not raise an error because with the query operation,
                # there is no information to create a database.
                # Log an error and let the user know it should be
                # created first or use predefined configuration options.
                if self.check_valid_database_path(query_builder):
                    self.run_query(query_builder)
                else:
                    raise InvalidDatabaseError(
                        query_builder["database_name"],
                        query_builder["file_type"],
                    )
            else:
                # The config option is selected,
                # read the config file and validate it with
                # the ReadConfigPattern class
                pattern: ReadConfigPattern = (
                    self.initialize_config_pattern()
                )
                # Check if database exists
                # If not present, create it from the config options
                if not self.check_valid_database_path(pattern.creation_dict):
                    # Re-use the run_makedatabase() method with right params
                    self.run_makedatabase(pattern.creation_dict)
                # Check if database does exists at this point,
                # if not, raise an error and exit the program
                # Otherwise, run the query operation
                if not self.check_valid_database_path(pattern.creation_dict):
                    # Let the user know the database does not exist,
                    # if the code reaches here, the run_makedatabase() was
                    # called without errors, so a bigger issue is present here.
                    raise InvalidDatabaseError(
                        pattern.creation_dict["database_name"],
                        pattern.creation_dict["file_type"],
                    )
                else:
                    self.run_query(pattern.creation_dict)
                    # Parsing operations
                    ParsingManager(
                        pattern,
                        self.file_type,
                        self.sample_name,
                    )
                    #
                    # Save or delete intermediate files
                    # This code should be moved to a separate function
                    #
                    if self.input_args.save_intermediates:
                        self.save_intermediates()
                    else:
                        self.delete_intermediates()


def main(provided_args: list[str] | None = None) -> None:
    """
    Entry point for the Pacini-Typing pipeline.
    Parses command-line arguments and initiates the pipeline.

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


if __name__ == "__main__":
    logging.info("Starting the Pacini-Typing pipeline, parsing arguments...")
    main()

###########################################################################
###########################################################################

# TODO: query_runner:run - This return statement is not used anywhere, should it be removed?

# TODO : validating_input_arguments - Store certain values from main OPTION as class variable

# TODO : validating_input_arguments - Compare if two files really are paired

###########################################################################
###########################################################################
