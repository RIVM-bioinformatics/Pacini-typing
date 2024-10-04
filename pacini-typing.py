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
from makedatabase import DatabaseBuilder
import argument_parser.build_parser
import validating.validating_input_arguments
import validating.validate_database as db
from validating.determine_input_type import FileValidator
from run_queries.query_runner import QueryRunner


if __name__ == "__main__":
    # Retrieve the args object, arguments have been parsed at this point
    args = argument_parser.build_parser.main()

    logging.basicConfig(
        level=args.verbose and logging.DEBUG or logging.INFO,
        format="%(asctime)s %(levelname)-5s %(process)d : %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )

    logging.info("Starting the application...")

    if validating.validating_input_arguments.main(args):
        logging.info("Input arguments have been validated, found no issues.")

    # Check if the options are available
    if args.options == "makedatabase":
        logging.info("Running makedatabase")
        DatabaseBuilder(
            database_path=args.database_path,
            database_name=args.database_name,
            input_fasta_file=args.input,
            database_type=args.database_type
        )

    elif args.options == "query":
        logging.info("Option query was selected, retrieving the file type...")
        file_validator = (FileValidator(
            [args.single] if hasattr(args, "single") and args.single else args.paired))
        file_type = file_validator.get_file_type()
        logging.info("File type for input: %s", file_type)

        # With the filetype determined,
        # check is paired mode doesn't have two fasta file and vice versa
        logging.debug("Checking if the input files are valid for the selected mode...")
        file_validator.check_single_file(file_type, args)

        # Check if database exists before running the query
        logging.debug("Checking if the database exists and is complete...")
        db.check_for_database_path(args, file_type)

        if file_type:
            logging.info("File type has been retrieved, running query...")
            runner = QueryRunner(
                input_file_type=file_type,
                input_file=args.single if file_type == "FASTA" else args.paired,
                database_path=args.database_path,
                database_name=args.database_name,
                output_file=args.output
            )
            runner.run()
            logging.debug("Query runtime: %s seconds", round(runner.get_runtime(), 2))
