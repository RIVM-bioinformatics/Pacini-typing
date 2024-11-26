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
__all__ = ["EValueFilter"]

import pandas as pd

from parsing.filter_pattern import Filter


class EValueFilter(Filter):
    """
    #TODO : To be filed in later...
    """

    def __init__(self, e_value: float, parse_type: str):
        """
        #TODO : To be filed in later...
        """
        self.e_vlaue = e_value

    def apply(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """
        #TODO : To be filed in later...
        """
        if self.parse_type == "FASTA":
            return data_frame[data_frame["evalue"] <= self.e_value]
        return data_frame[data_frame["e_value"] <= self.e_value]
