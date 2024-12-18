#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Script that defines the Filter class, which is an abstract class that defines the
interface for all filters that can be applied to a pandas DataFrame.
The class only has one method, apply, which takes a pandas DataFrame as input and
returns a pandas DataFrame as output.

This interface can be widely used to define different filters that can be applied
to a pandas DataFrame.
The implemented filters can then all be applied in the same way,
by calling the apply method on the filter object.
It is very easy to add new filters in the future.
"""

__author__ = "Mark van de Streek"
__data__ = "2024-11-22"
__all__ = ["Filter"]

from abc import ABC, abstractmethod

import pandas as pd


class Filter(ABC):
    """
    Abstract class that defines the interface for
    all filters that can be applied to a pandas DataFrame.
    --------
    Methods:
        - apply: Applies the filter to the input DataFrame.
    --------
    """

    @abstractmethod
    def apply(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """
        Abstract method that holds the logic of the filtering.
        This method is implemented by the subclasses of the
        Filter class. All filters MUST implement this method.
        --------
        Input:
            - data_frame: pandas DataFrame unfiltered
        Output:
            - pandas DataFrame filtered
        --------
        > The apply is not implemented in this class itself,
        > but the above comments are added to explain the interface.
        """
        pass
