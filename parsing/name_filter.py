#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Implementation of a filter for the gene names of the query results.
This filter is implementing the Filter interface.
See the filter_pattern.py file for more information about the Filter interface.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-11-22"
__all__ = ["GeneNameFilter"]

import pandas as pd

from parsing.filter_pattern import Filter


class GeneNameFilter(Filter):
    """
    GeneNameFilter class that implements the Filter interface.
    The implementation is especially for the gene names of the query results.
    This means, dataframe is filtered only for the found gene names.
    """

    def __init__(self, gene_names: list[str], parse_type: str):
        """
        Constructor to initialize the gene names and parse type.
        ----------
        Input:
            - gene_names: list[str]: the list of gene names to filter for
            - parse_type: str: the type of the parser (FASTA or FASTQ)
        ----------
        """
        self.gene_names = gene_names
        self.parse_type = parse_type

    def apply(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """
        Method that holds the logic to filter the dataframe.
        The gene names are placed in a pattern and checked for the
        presence in the dataframe.
        ----------
        Input:
            - data_frame: the dataframe that needs to be filtered
        Output:
            - the filtered dataframe
        ----------
        """
        pattern = "|".join(self.gene_names)
        if self.parse_type == "FASTA":
            return data_frame[
                data_frame["sseqid"].str.contains(
                    pattern, case=False, na=False
                )
            ]
        return data_frame[
            data_frame["Template"].str.contains(pattern, case=False, na=False)
        ]
