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
import makedatabase
import argument_parser.build_parser
import validating.validating_input_arguments
from validating.determine_input_type import FileValidator

LOGGER = logging.getLogger(__name__)


if __name__ == "__main__":
    # Retrieve the args object, arguments have been parsed at this point
    args = argument_parser.build_parser.main()

    # Configure the logging
    logging.basicConfig(
        level=args.verbose and logging.DEBUG or logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info("Starting the program...")
    logging.debug("Arguments have been parsed, validating them...")

    if validating.validating_input_arguments.main(args):
        logging.debug("Input arguments have been validated")

    # Check if the options are available
    if args.options == "makedatabase":
        logging.info("Running makedatabase")
        makedatabase.main(args)

    elif args.options == "query":
        if hasattr(args, "single") and args.single:
            file_type = FileValidator(args.paired).get_file_type()
            logging.debug("File type for single input: %s", file_type)
        elif hasattr(args, "paired") and args.paired:
            file_type = FileValidator(args.paired).get_file_type()
            logging.debug("File type for paired input: %s", file_type)
