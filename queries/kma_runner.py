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
__all__ = ["KMA"]

from enum import Enum


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
    OUTPUT_FORMAT = "-tsv"
    IDENTITY = "-ID"

    @staticmethod
    def get_query(option: dict) -> list:
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
            KMA.RUN_OPTION.value,
            KMA.PAIRED_OPTION.value,
            option["input_file_list"][0],
            option["input_file_list"][1],
            KMA.IDENTITY.value,
            str(option["query"]["filters"]["identity"]),
            KMA.OUTPUT_FORMAT.value,
            "-t_db",
            option["database_path"] + option["database_name"],
            "-o",
            option["query"]["output"],
            "-mrc",
            "0.7",
            "-pm",
            "p",
        ]
