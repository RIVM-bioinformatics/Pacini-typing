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

__author__ = "Mark van de Streek"
__date__ = "2024-09-27"
__all__ = ["main"]

import argparse
from argparse import RawTextHelpFormatter

import pkg_resources

from preprocessing.argsparse.args_makedatabase import (
    build_makedatabase_command,
)
from preprocessing.argsparse.args_query import build_query_command


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
        prog="Pacini-typing",
        description=(
            "Bacterial Genotyping Tool for RIVM IDS-Bioinformatics\n\n"
            "Either pick a subcommand to manually run the tool or\n"
            "provide a predefined configuration file and your input file(s) (FASTA/FASTQ)\n"
            "and let Pacini-typing do the work for you.\n\n"
            "If using a configuration file, both the\n"
            "--config and --input arguments are required.\n\n"
        ),
        formatter_class=RawTextHelpFormatter,
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

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        required=False,
        metavar="File",
        help="Path to predefined configuration file",
    )

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        nargs="+",
        required=False,
        metavar="File",
        help="Path to input file(s). Accepts 1 fasta file or 2 fastq files",
    )

    parser.add_argument(
        "--save-intermediates",
        action="store_true",
        default=False,
        help="Save intermediate files of the run",
    )

    parser.add_argument(
        "--log-file",
        action="store_true",
        default=False,
        help="Save log file of the run",
    )

    parser.add_argument(
        "-t",
        "--threads",
        required=False,
        default=1,
        type=lambda x: int(float(x)),
        metavar="Threads",
        help="Number of threads to use (rounded to the nearest integer)",
    )

    parser.add_argument(
        "-f",
        "--fasta-out",
        action="store_true",
        default=False,
        help="Write found sequences to a FASTA output file",
    )

    parser.add_argument(
        "-m",
        "--search_mode",
        type=str,
        choices=["SNPs", "genes", "both"],
        default="genes",
        help=(
            "Search mode to use. SNPs, genes or both.\n" "Default is genes.\n"
        ),
    )

    subparsers = parser.add_subparsers(
        title="operations",
        description="For more information on a specific command, type: pacini_typing <command> -h",
        dest="options",
    )

    build_makedatabase_command(subparsers)
    build_query_command(subparsers)

    args = parser.parse_args(givenargs)

    # Some first level argument checks
    # to ensure that the user has provided the correct arguments

    if args.fasta_out and args.search_mode == "SNPs":
        parser.error(
            "--fasta-out cannot be used with --search_mode SNPs. "
            "Please use this option only when searching for genes."
        )

    if not args.options:
        if not args.config or not args.input:
            parser.error(
                "Both --config and --input must be provided if no subcommand is specified."
            )
    else:
        if args.config or args.input:
            parser.error(
                "--config or --input cannot be used with subcommands."
            )
        if args.fasta_out or args.save_intermediates:
            parser.error(
                "--fasta-out and --save-intermediates cannot be used with subcommands."
            )

    return args
