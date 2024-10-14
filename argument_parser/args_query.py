#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

This script is used to build the query subcommand for the parser.
This subcommand is added to the main parsing object in the build_parser script.
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["build_query_command"]


def build_query_command(subparsers):
    """
    Script that builds the query subcommand for the parser
    ----------
    Input:
        - subparsers: subparsers object that is used to add the subcommand
    ----------
    """
    query = subparsers.add_parser(
        "query",
        help="Run query against reference database",
    )

    query.add_argument(
        "-p",
        "--paired",
        required=False,
        metavar=("file1", "file2"),
        nargs=2,
        help="Paired-end reads to be used for query. "
             "Specify two files separated by a space: -p file1 file2",
    )

    query.add_argument(
        "-s",
        "--single",
        required=False,
        type=str,
        metavar="File",
        help="Single-end reads to be used for query. Specify one file: -s file",
    )

    query.add_argument(
        "-db_name",
        "--database_name",
        type=str,
        required=True,
        metavar="name",
        help="Specify the name of the database",
    )
    query.add_argument(
        "-db_path",
        "--database_path",
        type=str,
        required=True,
        metavar="location",
        help="Specify the location of the database, ending with /",
    )

    query.add_argument(
        "-o",
        "--output",
        required=True,
        type=str,
        metavar="Output",
        help="Output file to store the results. Specify an output file: -o output",
    )

    query.add_argument(
        "-id",
        "--identity",
        required=False,
        type=str,
        metavar="Min. identity",
        help="Minimum identity percentage for the query",
        default="95",
    )
