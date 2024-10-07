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
import sys
from makedatabase import DatabaseBuilder
import argument_parser.build_parser
import validating.validating_input_arguments
import validating.validate_database as db
from validating.determine_input_type import FileValidator
from run_queries.query_runner import QueryRunner


def setup_logging(logging_args):
    """
    Fill in later...
    """
    logging.basicConfig(
        level=logging_args.verbose and logging.DEBUG or logging.INFO,
        format="%(asctime)s %(levelname)-5s %(process)d : %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )
    logging.info("Starting the application...")


def validate_arguments(validate_args):
    """
    Fill in later...
    ----------
    Input:
    ----------
    """
    if validating.validating_input_arguments.main(validate_args):
        logging.info("Input arguments have been validated, found no issues.")
    else:
        logging.error("Error while validating the input arguments, "
                      "please check the above logs for more information.")
        sys.exit(1)


def run_makedatabase(makedatabase_args):
    """
    Fill in later...
    ----------
    Input:
    ----------
    """
    DatabaseBuilder(
        database_path=makedatabase_args.database_path,
        database_name=makedatabase_args.database_name,
        input_fasta_file=makedatabase_args.input,
        database_type=makedatabase_args.database_type
    )


def get_file_type(file_type_args):
    """
    Fill in later...
    ----------
    Input:
    ----------
    """
    if hasattr(file_type_args, "single") and file_type_args.single:
        return FileValidator([file_type_args.single]).get_file_type()
    return FileValidator(file_type_args.paired).get_file_type()


def check_valid_option_with_args(validate_option_args, input_file_type):
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
    if ((input_file_type == "FASTQ" and validate_option_args.single) or
            (input_file_type == "FASTA" and validate_option_args.paired)):
        logging.error(
            "Only FASTA files are allowed for single files "
            "and only FASTQ files are allowed for paired files.")
        sys.exit(1)


def check_valid_database_path(database_args, input_file_type):
    """
    Fill in later...
    ----------
    Input:
    ----------
    """
    db.check_for_database_path(database_args, input_file_type)


def run_query(query_args, input_file_type):
    """
    Fill in later...
    ----------
    Input:
    ----------
    """
    # TODO - Way to many input arguments, consider refactoring
    runner = QueryRunner(
        input_file_type=input_file_type,
        input_file=query_args.single if input_file_type == "FASTA" else query_args.paired,
        database_path=query_args.database_path,
        database_name=query_args.database_name,
        output_file=query_args.output
    )
    runner.run()
    logging.debug("Query runtime: %s seconds", runner.get_runtime())


if __name__ == "__main__":
    # Retrieve the args object, arguments have been parsed at this point
    args = argument_parser.build_parser.main()

    # TODO - Make the input db arguments required all the time,
    #   so that the database could be created if not found running the query

    # TODO - Translate this script to a class-based structure

    # TODO - Add logging to every method above to make debugging easier,
    #  keep in mind the verbosity level

    # Setup up the logging, i.e., level and format
    setup_logging(args)
    # Validate all input arguments
    validate_arguments(args)

    # Subcommand makedatabase
    if args.options == "makedatabase":
        # Run with the validated arguments
        run_makedatabase(args)

    elif args.options == "query":
        # Reterieve the file type
        file_type = get_file_type(args)
        # Make sure the database exists
        check_valid_database_path(args, file_type)
        # Run the query
        run_query(args, file_type)

    ##################################################################################

    # OLD CODE BELOW

    # Still considering how to refactor the code to make it more readable and maintainable

    # file_validator = None
    # file_type = None
    #
    # if hasattr(args, "single") and args.single:
    #     run_file_checks(args.single)
    #     file_validator = FileValidator([args.single])
    # elif hasattr(args, "paired") and args.paired:
    #     if all(run_file_checks(file) for file in args.paired):
    #         check_for_same_name(args)
    #         compare_paired_files(args)
    #         check_paired_names(args)
    #     file_validator = FileValidator(args.paired)
    # elif hasattr(args, "input") and args.input:
    #     run_file_checks(args.input)
    #
    # if file_validator:
    #     file_type = file_validator.get_file_type()
    #     file_validator.check_single_file(file_type, args)
    #     db.check_for_database_path(args, file_type)
    #
    # if args.options == "makedatabase":
    #     logging.info("Running makedatabase")
    #     DatabaseBuilder(
    #         database_path=args.database_path,
    #         database_name=args.database_name,
    #         input_fasta_file=args.input,
    #         database_type=args.database_type
    #     )
    #
    # elif args.options == "query" and file_type:
    #     runner = QueryRunner(
    #         input_file_type=file_type,
    #         input_file=args.single if file_type == "FASTA" else args.paired,
    #         database_path=args.database_path,
    #         database_name=args.database_name,
    #         output_file=args.output)
    #     runner.run()
