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


def prepare_query(input_file, database, output_file):
    """
    Simple class method that prepares the query for the BLAST run.
    This query is passed to the super class QueryRunner.
    """
    return [
        RUN_OPTION,
        "-query", input_file,
        "-db", database,
        "-out", output_file,
        "-outfmt", OUTPUT_FORMAT
    ]
