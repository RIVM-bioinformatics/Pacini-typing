#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Building parser script that contains a main function that parses the arguments.
See the main method for specific information.
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["main"]

import argparse

import argsparse.args_makedatabase
import argsparse.args_query


def main() -> argparse.Namespace:
    """
    main and only function of this script that will be used to
    create a parser object and return the arguments in a parsed object.
    The build_makedatabase_command function is used to build sub argument parser,
    this subparser is added to the main parser object.
    ----------
    Output:
        - args: parsed object with the arguments
    ----------
    """
    parser = argparse.ArgumentParser(
        prog="Pacini",
        description="Bacterial Genotyping Tool for RIVM IDS-Bioinformatics",
        epilog="See github.com/RIVM-Bioinformatics for more information",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=0,
        help="Increase output verbosity",
    )

    subparsers = parser.add_subparsers(
        title="operations",
        description="For more information on a specific command, type: Pacini.py <command> -h",
        dest="options",
    )

    argsparse.args_makedatabase.build_makedatabase_command(subparsers)
    argsparse.args_query.build_query_command(subparsers)

    return parser.parse_args()
