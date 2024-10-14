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

import logging
import gzip
import shutil
import os
import sys
from makedatabase import DatabaseBuilder
import argument_parser.build_parser
import validating.validating_input_arguments
import validating.validate_database as db
from validating.determine_input_type import FileValidator
from run_queries.query_runner import QueryRunner


class PaciniTyping:
    """
    Main class for the Pacini-Typing pipeline.
    This class is respsonsible for calling operations in the correct order.
    The following operations are performed:
        - Parse all arguments into a dictionary
        - Setup logging

    """

    def __init__(self, input_args):
        """
        Constructor for the PaciniTyping class.
        The contstructor accepts the parsed input arguments from argparse.
        The input arguments are stored in the input_args attribute.
        The run method is responsible for calling all other methods.
        """
        self.input_args = input_args
        self.option = {}

    def parse_all_args(self):
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        self.option = {
            "database_path": self.input_args.database_path,
            "database_name": self.input_args.database_name,
            "option": self.input_args.options,
            "verbose": self.input_args.verbose,
            "run_path": os.path.abspath(__file__),
            "query": None,
            "makedatabase": None
        }
        if self.input_args.options == "query":
            self.option["query"] = {
                "paired": self.input_args.paired,
                "single": self.input_args.single,
                "output": self.input_args.output,
                "filters": {
                    "identity": self.input_args.identity,
                }
            }

        elif self.input_args.options == "makedatabase":
            self.option["makedatabase"] = {
                "database_type": self.input_args.database_type,
                "input": self.input_args.input
            }

    def setup_logging(self):
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        logging.basicConfig(
            level=self.option["verbose"] and logging.DEBUG or logging.INFO,
            format="%(asctime)s %(levelname)-5s %(process)d : %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S"
        )

    def get_input_filenames(self):
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        input_files_list = []
        if self.option["query"]:
            if self.option["query"]["single"]:
                input_files_list.append(self.option["query"]["single"])
            elif self.option["query"]["paired"]:
                input_files_list.extend(self.option["query"]["paired"])
        elif self.option["makedatabase"]:
            input_files_list.append(self.option["makedatabase"]["input"])
        self.option["input_file_list"] = input_files_list

    def check_for_unzip_files(self):
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        for file in self.option["input_file_list"]:
            if file.endswith(".gz"):
                logging.info("Unzipping file %s", file)
                self.unzip_gz_files()

    def unzip_gz_files(self):
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        unzipped_files = []
        for file in self.option["input_file_list"]:
            try:
                with gzip.open(file, "rb") as f_in:
                    with open(file[:-3], "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                unzipped_files.append(file[:-3])
            except Exception as e:
                logging.error("Error while unzipping file %s: %s", file, e)
                sys.exit(1)
        self.option["input_file_list"] = unzipped_files

    def validate_file_arguments(self):
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        if validating.validating_input_arguments.main(self.option["input_file_list"]):
            logging.info("Input arguments have been validated, found no issues.")
        else:
            logging.error("Error while validating the input arguments, "
                          "please check the above logs for more information.")
            sys.exit(1)

    def run_makedatabase(self):
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        DatabaseBuilder(
            arg_options=self.option
        )

    def get_file_type(self):
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        self.option["file_type"] = (
            FileValidator(self.option["input_file_list"])
            .get_file_type())

    def check_valid_option_with_args(self):
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
        if (len(self.option["input_file_list"]) == 1 and self.option["file_type"] == "FASTQ") or \
                (len(self.option["input_file_list"]) == 2 and self.option["file_type"] == "FASTA"):
            logging.error(
                "Only FASTA files are allowed for single files "
                "and only FASTQ files are allowed for paired files.")
            sys.exit(1)

    def check_valid_database_path(self):
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        db.check_for_database_path(arg_options=self.option)

    def run_query(self):
        """
        Still have to fill in the docstring...
        ----------
        Input:
        ----------
        """
        runner = QueryRunner(
            run_options=self.option
        )
        runner.run()
        logging.debug("Query runtime: %s seconds", runner.get_runtime())

    def run(self):
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

        # Construct and validate the filter arguments
        # IMPLEMENT
        # TODO - filter_arguments = self.parse_filter_arguments(args)

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

    ###########################################################################

    # TODO - Make the input db arguments required all the time,
    #   so that the database could be created if not found running the query

    # TODO - Translate this script to a class-based structure

    # TODO - Add logging to every method above to make debugging easier,
    #  keep in mind the verbosity level


if __name__ == "__main__":
    args = argument_parser.build_parser.main()
    pacini_typing = PaciniTyping(args)
    pacini_typing.run()
