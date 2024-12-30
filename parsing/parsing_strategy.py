#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Strategy pattern implementation for the parsing module.
This module is responsible for defining the parsing strategy interface.
This is done because of the different file formats that need to be parsed.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-12-17"
__all__ = ["ParserStrategy"]

from abc import ABC, abstractmethod
from typing import Any, Optional

import pandas as pd


class ParserStrategy(ABC):
    """
    Interface for the parsing strategy.
    This class defines the methods that need to be implemented
    by the concrete parsing strategy classes.
    ----------
    Methods:
        - read_output: Method to read the output of the search
        - extract_gene_list: Method to extract the gene list from the data frame
        - get_hits_report_info: Method to get the hits report information
        - get_gene_column_name: Method to get the gene column name
        - write_fasta_out: Method to write the FASTA output
    ----------
    """

    @abstractmethod
    def read_output(self, filename: str) -> pd.DataFrame:
        """
        Abstract method that should read the output of the query run
        and place the results in a pandas data frame.
        ----------
        Input:
            - filename: The name of the file to be read.
        Output:
            - data_frame: The data frame containing the results
        ----------
        """
        pass

    @abstractmethod
    def extract_gene_list(self, data_frame: pd.DataFrame) -> list[str]:
        """
        Function that should extract the gene list from the data frame.
        ----------
        Input:
            - data_frame: The data frame containing the results
        Output:
            - gene_list: The list of genes
        ----------
        """
        pass

    @abstractmethod
    def get_hits_report_info(self) -> tuple[list[str], str, Any]:
        """
        Function that should return the hits report information.
        ----------
        Output:
            - hits_report: The hits report
            - gene_column_name: The gene column name
            - config_options: The configuration options
        ----------
        """
        pass

    @abstractmethod
    def get_gene_column_name(self) -> str:
        """
        Function that should return the column name
        where the gene names are stored in the frame.
        ----------
        Output:
            - gene_column_name: The gene column name
        ----------
        """
        pass

    @abstractmethod
    def requires_dataframe(self) -> bool:
        """
        Helper method to determine if the parser requires a data frame.
        The write_fasta_out method is quite different between the parsers.
        And to not make the code too duplicate in the main Parser class,
        this methods helps to determine if a data frame is required to send
        to the write_fasta_out method.
        ----------
        Output:
            - bool: True if a data frame is required, False otherwise
        ----------
        """
        pass

    @abstractmethod
    def write_fasta_out(
        self,
        config_options: dict[str, Any],
        input_sequence_sample: str,
        list_of_genes: list[str],
        data_frame: Optional[pd.DataFrame] = None,
    ) -> None:
        """
        Function that should be responsible for writing the found
        gene sequences to a FASTA file. (the --fasta-out option)
        ----------
        Input:
            - config_options: The configuration options
            - input_sequence_sample: The input sequence sample
            - list_of_genes: The list of genes
            - data_frame: The data frame containing the results
        ----------
        """
        pass
