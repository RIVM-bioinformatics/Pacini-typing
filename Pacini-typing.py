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
import validating.validating_input_file

LOGGER = logging.getLogger(__name__)


if __name__ == "__main__":
    # Retrieve the args object, arguments have been parsed at this point
    args = argument_parser.build_parser.main()

    # Configure the logging
    log_format = "%(filename)s - %(funcName)s: %(message)s"
    logging.basicConfig(
        level=args.verbose and logging.DEBUG or logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info("Starting the program...")
    logging.debug(f"Arguments have been parsed, validating them...")

    if validating.validating_input_arguments.main(args):
        logging.debug("Input arguments have been validated")

    # Check if the options are available
    if args.options == "makedatabase":
        logging.info("Running makedatabase")
        makedatabase.main(args)
    elif args.options == "query":
        if hasattr(args, "single") and args.single:
            validating.validating_input_file.main([args.single])
        elif hasattr(args, "paired") and args.paired:
            validating.validating_input_file.main(args.paired)
