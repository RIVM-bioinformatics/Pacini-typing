#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

To be filed in later...
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["prepare_query"]

RUN_OPTION = "blastn"
OUTPUT_FORMAT = "6"

# TODO: This file was first a class, but quite overkill for the purpose,
#  maybe additional information could be added to this script in the future.
#  This way, blast operations parameters could easily be changed or extended.


def prepare_query(input_file, database, output_file):
    """
    Simple method that prepares the query for the BLAST run.
    This query is passed to the super class QueryRunner.
    The script-constants are used to set the run option and output format.
    ----------
    Input:
        - input_file: str
        - database: str
        - output_file: str
    Output:
        - list with the query to run BLAST
    ----------
    """
    return [
        RUN_OPTION,
        "-query", input_file,
        "-db", database,
        "-out", output_file,
        "-outfmt", OUTPUT_FORMAT
    ]
