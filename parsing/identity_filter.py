#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Implementation of a filter for the percentage identity of the query results.
This filter is implementing the Filter interface.
See the filter_pattern.py file for more information about the Filter interface.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-11-22"
__all__ = ["PercentageIdentityFilter"]

import pandas as pd

from parsing.filter_pattern import Filter


class PercentageIdentityFilter(Filter):
    """
    CoverageFilter class that implements the Filter interface.
    The implementation is especially for the percentage identity
    of the query results. This means, dataframe is filtered
    only for the identity column.
    ----------
    Methods:
        - __init__: Constructor to initialize the threshold and parse type
        - apply: Method that holds the logic to filter the dataframe
    ----------
    """

    def __init__(self, threshold: float, parse_type: str):
        """
        Constructor to initialize the threshold and parse type.
        ----------
        Input:
            - threshold: float: the minimum identity percentage
            - parse_type: str: the type of the parser (FASTA or FASTQ)
        ----------
        """
        self.threshold = threshold
        self.parse_type = parse_type

    def apply(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """
        Method that holds the logic to filter the dataframe.
        The identity column is checked for the minimum identity percentage.
        Values above the threshold are returned.
        ----------
        Input:
            - data_frame: the dataframe that needs to be filtered
        Output:
            - the filtered dataframe
        ----------
        """
        if self.parse_type == "FASTA":
            return data_frame[data_frame["pident"] >= self.threshold]
        return data_frame[data_frame["Template_Identity"] >= self.threshold]
