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
and returns it to the (main) GeneQueryRunner class.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-10-02"
__all__ = ["BLASTn"]

import logging
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
    QUERY_OPTION: option for the query file
    DATABASE_OPTION: option for the database
    OUTPUT_OPTION: option for the output file
    OUTPUT_FORMAT_OPTION: flag for the output format
    OUTPUT_FORMAT: flag for the output format
    FORMATS: list of all the formats that are used
    ----------
    """

    RUN_OPTION = "blastn"
    QUERY_OPTION = "-query"
    DATABASE_OPTION = "-db"
    OUTPUT_OPTION = "-out"
    OUTPUT_FORMAT_OPTION = "-outfmt"
    OUTPUT_FORMAT = "6"
    FORMATS = [
        "qseqid",  # query or source (gene) sequence id
        "sseqid",  # subject or target (reference genome) sequence id
        "pident",  # percentage of identical positions
        "length",  # alignment length (sequence overlap)
        "mismatch",  # number of mismatches
        "gapopen",  # number of gap openings
        "qstart",  # start of alignment in query
        "qend",  # end of alignment in query
        "sstart",  # start of alignment in subject
        "send",  # end of alignment in subject
        "evalue",  # expect value
        "bitscore",  # bit score
        "qcovhsp",  # query coverage per HSP
        "qseq",  # aligned part of query sequence
        "slen",  # length of the subject sequence
        "gaps",  # number of gaps
    ]

    @staticmethod
    def get_query(option: dict[str, Any]) -> list[str]:
        """
        Simple method that prepares the query for the BLAST run.
        This query is passed to the main class QueryRunner.
        The script-constants are used to set the run option and output format.
        ----------
        Input:
            - dictionary with the input files,
                database, and output file
        Output:
            - list with the query to run BLAST
        ----------
        """
        logging.debug("Preparing BLAST query...")
        return [
            BLASTn.RUN_OPTION.value,
            BLASTn.QUERY_OPTION.value,
            option["input_file_list"][0],
            BLASTn.DATABASE_OPTION.value,
            option["database_path"] + option["database_name"],
            BLASTn.OUTPUT_OPTION.value,
            option["output"] + ".tsv",
            BLASTn.OUTPUT_FORMAT_OPTION.value,
            f"'{BLASTn.OUTPUT_FORMAT.value} {" ".join(BLASTn.FORMATS.value)}'",
            "-num_threads",
            str(option["threads"]),
        ]

    @staticmethod
    def get_version_command() -> list[str]:
        """
        Method to get the command to check the BLAST version.
        The method returns a string which could then be used later.
        ----------
        Output:
            - list with the command to check the BLAST version
        ----------
        """
        return [BLASTn.RUN_OPTION.value, "-version"]
