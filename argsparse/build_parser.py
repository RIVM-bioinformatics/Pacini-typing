#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

This module is responsible for building the main parser object for
the Pacini-typing tool.

The parser is being set up with the necessary arguments and subcommands
The subcommands are built in separate scripts and added to the main parser object.
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["main"]

import argparse
import sys

import pkg_resources

import argsparse.args_makedatabase
import argsparse.args_query


def main(givenargs: list[str]) -> argparse.Namespace:
    """
    main and only function of this script that is used to
    create a parser object and return the arguments in a parsed object.
    The build_makedatabase_command function is used to build sub argument parser,
    this subparser is added to the main parser object.
    ----------
    Input:
        - givenargs: list of arguments that are passed to the script,
            could be sys.argv[1:] or a test list of arguments
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

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=pkg_resources.get_distribution("pacini_typing").version,
    )

    subparsers = parser.add_subparsers(
        title="operations",
        description="For more information on a specific command, type: Pacini.py <command> -h",
        dest="options",
    )

    argsparse.args_makedatabase.build_makedatabase_command(subparsers)
    argsparse.args_query.build_query_command(subparsers)

    args = parser.parse_args(givenargs)

    # A subcommand is required, if not provided, print help and exit
    # This is done to ensure that the user provides a subcommand
    if not hasattr(args, "options") or args.options is None:
        parser.print_help()
        sys.exit(1)

    return args
