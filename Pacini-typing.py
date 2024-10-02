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
from validating.determine_input_type import FileValidator
from run_queries.blast_runner import BlastRunner
from run_queries.kma_runner import KMARunner


if __name__ == "__main__":
    # Retrieve the args object, arguments have been parsed at this point
    args = argument_parser.build_parser.main()

    logging.basicConfig(
        level=args.verbose and logging.DEBUG or logging.INFO,
        format="%(asctime)s %(levelname)-5s %(process)d : %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )

    logging.info("Starting the program...")
    logging.debug("Arguments have been parsed, validating them...")

    if validating.validating_input_arguments.main(args):
        logging.info("Input arguments have been validated, found no issues.")

    # TODO: Add a check for the database path and database name...

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
        file_type = FileValidator([args.single] if
                                  hasattr(args, "single") and args.single else args.paired).get_file_type()
        logging.info("File type for input: %s", file_type)

        if file_type:
            logging.info("File type has been retrieved, running query...")
            runner_class = BlastRunner if file_type == "FASTA" else KMARunner
            runner = runner_class(
                input_file=args.single if file_type == "FASTA" else args.paired,
                database=args.database,
                output_file=args.output
            )
            runner.run()
            logging.debug("Query runtime: %s seconds", round(runner.get_runtime(), 2))
