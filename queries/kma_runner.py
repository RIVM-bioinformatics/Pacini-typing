#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Enum class to store all KMA-related options and flags.
This class is used to create the right query for the KMA run.

The get_query() method prepares the query for the KMA run
and returns it to the (main) QueryRunner class.
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["KMA"]

from enum import Enum
from typing import Any


class KMA(Enum):
    """
    Enum class to store K-mer alignment options and flags.
    With this Enum class, the options are stored in a more structured way
    and could be changed very easily.
    ----------
    RUN_OPTION: string that is used in the subprocess.run() method
    PAIRED_OPTION: option for paired-end reads
    OUTPUT_FORMAT: flag for the output format
    MIN_IDENTITY: flag for the minimum identity percentage
    ----------
    """

    RUN_OPTION = "kma"
    PAIRED_OPTION = "-ipe"

    @staticmethod
    def get_query(option: dict[str, Any]) -> list[str]:
        """
        Simple method that prepares the query for the KMA run.
        This query is passed to the super class QueryRunner
        ----------
        Input:
            - dictionary with the input files,
                database, and output file
        Output:
            - list with the query to run KMA
        ----------
        """
        return [
            KMA.RUN_OPTION.value,
            KMA.PAIRED_OPTION.value,
            option["input_file_list"][0],
            option["input_file_list"][1],
            "-t_db",
            option["database_path"] + option["database_name"],
            "-o",
            option["output"],
            "-t",
            str(option["threads"]),
        ]
