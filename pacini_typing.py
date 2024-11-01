#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Fill in later...
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["PaciniTyping", "main"]

import argparse
import gzip
import logging
import os
import shutil
import sys
from typing import Any, Tuple

import argsparse.build_parser
import validation.validate_database as db
from makedatabase import DatabaseBuilder
from queries.query_runner import QueryRunner
from validation.determine_input_type import FileValidator
from validation.validating_input_arguments import ArgsValidator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-5s %(process)d : %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)


class PaciniTyping:
    """
    Main class for the Pacini-Typing pipeline.
    This class is respsonsible for calling operations in the correct order.
    The following operations are performed:
        - Parse all arguments into a dictionary
        - Setup logging
    """

    def __init__(self, input_args: argparse.Namespace) -> None:
        """
        Constructor for the PaciniTyping class.
        The contstructor accepts the parsed input arguments from argparse.
        The input arguments are stored in the input_args attribute.
        The run method is responsible for calling all other methods.
        """
        self.input_args = input_args
        self.option: dict[str, Any] = {}

    def parse_all_args(self) -> None:
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        logging.debug(
            "Placing all args and necessary information in a dictionary"
        )
        self.option = {
            "database_path": self.input_args.database_path,
            "database_name": self.input_args.database_name,
            "option": self.input_args.options,
            "verbose": self.input_args.verbose,
            "run_path": os.path.abspath(__file__).rsplit(".", 1)[0],
            "query": None,
            "makedatabase": None,
        }
        if self.input_args.options == "query":
            self.option["query"] = {
                "paired": self.input_args.paired,
                "single": self.input_args.single,
                "output": self.input_args.output,
                "filters": {
                    "identity": self.input_args.identity,
                },
            }

        elif self.input_args.options == "makedatabase":
            self.option["makedatabase"] = {
                "database_type": self.input_args.database_type,
                "input": self.input_args.input,
            }

    def setup_logging(self) -> None:
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        logging.debug("Setting up logging-level")
        logging.getLogger().setLevel(
            self.option["verbose"] and logging.DEBUG or logging.INFO
        )

    def get_input_filenames(self) -> None:
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        logging.debug("Retrieving input files and placing them in a list")
        input_files_list = []
        if self.option["query"]:
            if self.option["query"]["single"]:
                input_files_list.append(self.option["query"]["single"])
            elif self.option["query"]["paired"]:
                input_files_list.extend(self.option["query"]["paired"])
        elif self.option["makedatabase"]:
            input_files_list.append(self.option["makedatabase"]["input"])
        self.option["input_file_list"] = input_files_list

    def check_for_unzip_files(self) -> None:
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
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

    def unzip_gz_files(self, gz_files) -> None:
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        logging.debug("Unzipping files %s...", gz_files)
        unzipped_files = []
        for file in gz_files:
            try:
                with gzip.open(file, "rb") as f_in:
                    with open(file[:-3], "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                unzipped_files.append(file[:-3])
            except (OSError, gzip.BadGzipFile) as e:
                logging.error("Error while unzipping file %s: %s", file, e)
                sys.exit(1)
        logging.debug("Updating input file list with unzipped files")
        self.option["input_file_list"] = [
            file[:-3] if file in gz_files else file
            for file in self.option["input_file_list"]
        ]

    def validate_file_arguments(self) -> None:
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        logging.debug("Validating the input arguments...")
        argsvalidator = ArgsValidator(self.option)
        if argsvalidator.validate():
            logging.info(
                "Input arguments have been validated, found no issues."
            )
        else:
            logging.error(
                "Error while validation the input arguments, "
                "please check the above logs for more information."
            )
            sys.exit(1)

    def run_makedatabase(self) -> None:
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        logging.debug("Running the makedatabase operation...")
        DatabaseBuilder(arg_options=self.option)

    def get_file_type(self) -> None:
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        logging.debug("Determining the file type of the input file(s)...")
        self.option["file_type"] = FileValidator(
            self.option["input_file_list"]
        ).get_file_type()
        logging.info(
            "File type has been determined: %s", self.option["file_type"]
        )

    def check_valid_option_with_args(self) -> None:
        """
        This method checks if the file type is correct for the input arguments.
        To be precise, it checks if the file type is FASTA for single file input
        and FASTQ for paired files. If not, it will exit the program.
        This method is called after the file type has been determined.
        ----------
        Input:
            - file_type: string with the file type
            - args: object with the input arguments
        ----------
        """
        logging.debug(
            "Checking if the file type is correct for the input arguments..."
        )
        if (
            len(self.option["input_file_list"]) == 1
            and self.option["file_type"] == "FASTQ"
        ) or (
            len(self.option["input_file_list"]) == 2
            and self.option["file_type"] == "FASTA"
        ):
            logging.error(
                "Only FASTA files are allowed for single files "
                "and only FASTQ files are allowed for paired files."
            )
            sys.exit(1)

    def check_valid_database_path(self) -> None:
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        logging.debug("Checking if the database exists...")
        db.check_for_database_path(arg_options=self.option)

    def run_query(self) -> Tuple[str, str] | bool:
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        logging.debug("Running the query operation against database...")
        runner = QueryRunner(run_options=self.option)
        result = runner.run()
        logging.info("Query runtime: %s seconds", runner.get_runtime())

        return result

    def run(self) -> None:
        """
        Still have to fill in the docstring...
        """
        # Retrieve the args object, arguments have been parsed at this point
        # Place all arguments in a dictionary
        self.parse_all_args()
        # Setup up the logging, i.e., level and format
        self.setup_logging()
        # Get the input files
        self.get_input_filenames()
        # Check if they may need to be unzipped
        self.check_for_unzip_files()
        # Validate all input arguments
        self.validate_file_arguments()

        if self.option["makedatabase"]:
            # Run with the validated arguments
            self.run_makedatabase()
        elif self.option["query"]:
            # Retrieve the file type
            self.get_file_type()
            # Check if the file type is correct for the input arguments
            self.check_valid_option_with_args()
            # Make sure the database exists
            self.check_valid_database_path()
            # Run the query
            self.run_query()
            # result = self.run_query()
            # Parse the results.....

    ###########################################################################

    # TODO - Make the input db arguments required all the time,
    #   so that the database could be created if not found running the query

    # TODO - Add logging to every method above to make debugging easier,
    #  keep in mind the verbosity level

    # TODO - raise exceptions instead of sys.exit(1) to make the code more robust

    # TODO - With end2end tests, sys args are not empty. So when sys args,
    #  don't parse the arguments but use the sys args

    # TODO: query_runner:__str__ - Is this function necessary?

    # TODO: query_runner:run - This return statement is not used anywhere, should it be removed?

    # TODO : validating_input_arguments - Store certain values from main OPTION as class variable

    # TODO : validating_input_arguments - Compare if two files really are paired

    # TODO : Don't use a output file but take the output as a string:
    #  zcat/cat data/vibrio_genes.fasta | blastn -query data/VIB_AA4147AA_AS_2.fna
    # -subject - -outfmt '6 qseqid sseqid pident qcovs' -perc_identity 70
    #  Or: kma -i data/VIB_AA4147AA_AS_2.fna -t_db refdir/mykma -t 4 -ID 70 -mrc 0.7 -o
    # temp_output && cut -f 1,5 temp_output.res && rm temp_output.*


def main(provided_args: list[str] | None = None) -> None:
    """
    Main entry point for the Pacini-Typing pipeline.
    Parses command-line arguments and initiates the pipeline.

    If using (unit)tests, there is no sys.argv, so the provided_args are used.
    Otherwise, sys.argv is used to parse the arguments.
    """
    if provided_args:
        args = argsparse.build_parser.main(provided_args)
    else:
        args = argsparse.build_parser.main(sys.argv[1:])

    pacini_typing = PaciniTyping(args)
    pacini_typing.run()


if __name__ == "__main__":
    logging.info("Starting the Pacini-Typing pipeline, parsing arguments...")
    main()
