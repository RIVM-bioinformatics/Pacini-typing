#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Enum class to store all BLAST-related options and flags.
This class is used to create the right query for the BLAST run.

The get_query() method prepares the query for the BLAST run
and returns it to the (main) QueryRunner class.
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["BLASTn"]

from enum import Enum
from typing import Any


class BLASTn(Enum):
    """
    Enum class to store BLAST options and flags.
    With this Enum class, the options are stored in a more structured way
    and could be changed very easily.
    Another output format could be added, for example:
    - "7 sseqid bitscore evalue slen pident qcovs"
    ----------
    RUN_OPTION: string that is used in the subprocess.run() method
    OUTPUT_FORMAT: flag for the output format
    IDENTITY: flag for the minimum identity percentage
    ----------
    """
    RUN_OPTION = "blastn"
    QUERY_OPTION = "-query"
    DATABASE_OPTION = "-db"
    OUTPUT_OPTION = "-out"
    OUTPUT_FORMAT_OPTION = "-outfmt"
    OUTPUT_FORMAT = "6"
    # TODO - Move the output format to config file with explanation of the format

    @staticmethod
    def get_query(option: dict[str, Any]) -> list[str]:
        """
        Simple method that prepares the query for the BLAST run.
        This query is passed to the super class QueryRunner.
        The script-constants are used to set the run option and output format.
        ----------
        Input:
            - dictionary with the input files,
                database, and output file
        Output:
            - list with the query to run BLAST
        ----------
        """
        return [
            BLASTn.RUN_OPTION.value,
            BLASTn.QUERY_OPTION.value,
            option["input_file_list"][0],
            BLASTn.DATABASE_OPTION.value,
            option["database_path"] + option["database_name"],
            BLASTn.OUTPUT_OPTION.value,
            option["output"] + ".tsv",
            BLASTn.OUTPUT_FORMAT_OPTION.value,
            BLASTn.OUTPUT_FORMAT.value,
        ]
