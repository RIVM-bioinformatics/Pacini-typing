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
__all__ = ["PercentageIdentityFilter"]

import pandas as pd
from filter import Filter


class PercentageIdentityFilter(Filter):
    """
    #TODO : To be filed in later...
    """

    def __init__(self, threshold: float, parse_type: str):
        """
        #TODO : To be filed in later...
        """
        self.threshold = threshold
        self.parse_type = parse_type

    def apply(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """
        #TODO : To be filed in later...
        """
        if self.parse_type == "FASTA":
            return data_frame[data_frame["pident"] > 99]
        return data_frame[data_frame["Template_Identity"] > 99]
