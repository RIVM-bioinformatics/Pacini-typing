#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

#TODO : To be filed in later...
"""

__author__ = "Mark van de Streek"
__data__ = "2024-11-22"
__all__ = ["GeneNameFilter"]

from filter import Filter
import pandas as pd


class GeneNameFilter(Filter):
    """
    #TODO : To be filed in later...
    """

    def __init__(self, gene_names: list[str], parse_type: str):
        """
        #TODO : To be filed in later...
        """
        self.gene_names = gene_names
        self.parse_type = parse_type

    def apply(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """
        #TODO : To be filed in later...
        """
        pattern = "|".join(self.gene_names)
        if self.parse_type == "FASTA":
            return data_frame[
                data_frame["sseqid"].str.contains(
                    pattern, case=False, na=False
                )
            ]
        return data_frame[
            data_frame["Template_Name"].str.contains(
                pattern, case=False, na=False
            )
        ]
