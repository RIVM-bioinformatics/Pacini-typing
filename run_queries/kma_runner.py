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

RUN_OPTION = "kma"
PAIRED_OPTION = "-ipe"
OUTPUT_FORMAT = "-tsv"

# TODO: This file was first a class, but quite overkill for the purpose,
#  maybe additional information could be added to this script in the future.
#  This way, blast operations parameters could easily be changed or extended.


def prepare_query(input_file, database, output_file, filter_args):
    """
    Simple method that prepares the query for the KMA run.
    This query is passed to the super class QueryRunner
    ----------
    Input:
        - input_file: list with the input files
        - database: str
        - output_file: str
    Output:
        - list with the query to run KMA
    ----------
    """
    return [
        RUN_OPTION,
        PAIRED_OPTION, input_file[0], input_file[1],
        "-t_db", database,
        "-o", output_file,
        "-ID", filter_args["identity"],
        "-mrc", "0.7",
        "-pm", "p",
        OUTPUT_FORMAT
    ]
