#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To be filed in later...
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["main"]

import sys
import os
import subprocess


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
        help="Paired-end reads to be used for query. Specify two files separated by a space: -p file1 file2",
    )

    query.add_argument(
        "-s",
        "--single",
        required=False,
        type=str,
        metavar="File",
        help="Single-end reads to be used for query. Specify one file: -s file",
    )
