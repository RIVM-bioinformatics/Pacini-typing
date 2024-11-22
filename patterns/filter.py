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
__all__ = ["Filter"]

import pandas as pd
from abc import ABC, abstractmethod


class Filter(ABC):
    """
    TODO : Fill in later...
    """

    @abstractmethod
    def apply(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """
        TODO : Fill in later...
        """
        pass
