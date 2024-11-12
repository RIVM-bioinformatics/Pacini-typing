#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

This module is responsible for building the makedatabase subcommand for the parser.
The subcommand is used to create a new reference database.
The subcommand is added to the main parsing object in the build_parser script.
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["build_makedatabase_command"]


from argparse import _SubParsersAction


def build_makedatabase_command(subparsers: _SubParsersAction) -> None:
    """
    Function that builds the makedatabase subcommand for the parser
    This function is called from the build_parser script
    ----------
    Input:
        - subparsers: subparsers object that is used to add the subcommand
    ----------
    """
    makedatabase = subparsers.add_parser(
        "makedatabase",
        help="Create a new reference database",
    )
    makedatabase.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        metavar="File",
        help="Input file with genes that are being used for building reference database",
    )
    makedatabase.add_argument(
        "-db_type",
        "--database_type",
        type=lambda x: x.lower(),
        required=True,
        metavar="fastq/fasta",
        choices=["fastq", "fasta"],
        help="Specify the database type that is being used",
    )
    makedatabase.add_argument(
        "-db_name",
        "--database_name",
        type=str,
        required=True,
        metavar="name",
        help="Specify the name of the database",
    )
    makedatabase.add_argument(
        "-db_path",
        "--database_path",
        type=str,
        required=True,
        metavar="path",
        help="Specify the path of the database",
    )
