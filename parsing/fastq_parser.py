#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Implementation of the FASTQ parsing strategy for the parsing module.
This module is responsible for parsing the output of the KMA search.
"""

__author__ = "Mark van de Streek"
__data__ = "2024-12-17"
__all__ = ["FASTQParser"]

from typing import Any, Optional

import pandas as pd

from parsing.alignment_extractor import AlignmentExtractor
from parsing.parsing_strategy import ParserStrategy

KMA_COLUMNS = {
    "Template": "hit",
    "Score": "score",
    "Expected": "expected",
    "Template_length: ": "align. length",
    "Template_Identity": "percentage identity",
    "Template_Coverage": "percentage coverage",
    "Query_Identity": "query identity",
    "Query_Coverage": "query coverage",
    "Depth": "depth",
    "q_value": "q-value",
    "p_value": "p-value",
}


class FASTQParser(ParserStrategy):
    """
    Concrete implementation of the ParserStrategy interface
    for parsing the output of the KMA search.
    ----------
    Methods:
        - read_output: Method to read the output of the KMA search
        - extract_gene_list: Method to extract the gene list from the data frame
        - get_hits_report_info: Method to get the hits report information
        - get_gene_column_name: Method to get the gene column name
        - write_fasta_out: Method to write the FASTA output
    ----------
    """

    def read_output(self, filename: str) -> pd.DataFrame:
        """
        Function that his responsible for reading the output of
        the KMA search and placing the results in a pandas data frame.
        The data frame is also formatted with the right column names.
        ----------
        Input:
            - filename: The name of the file to be read.
        Output:
            - data_frame: data frame with the results of the KMA search.
        ----------
        """
        data_frame = pd.read_csv(filename + ".res", sep="\t", header=0)
        data_frame.columns = list(KMA_COLUMNS.keys())
        data_frame["Template_Identity"] = data_frame[
            "Template_Identity"
        ].astype(float)
        data_frame["Template_Coverage"] = data_frame[
            "Template_Coverage"
        ].astype(float)
        return data_frame

    def extract_gene_list(self, data_frame: pd.DataFrame) -> list[str]:
        """
        Function responsible for extracting the gene list
        from the data frame. Samples are split by the colon
        and the first part is taken as the gene name.
        (e.g. "gene:sample" -> "gene")
        ----------
        Input:
            - data_frame: The data frame with the KMA results.
        Output:
            - list[str]: List with gene names.
        """
        return [
            gene.split(":")[0]
            for gene in data_frame["Template"].values.tolist()
        ]

    def get_hits_report_info(self) -> tuple[list[str], str, Any]:
        """
        Basic function that returns the columns,
        significance type, and value column for the hits report.
        These values differ between the different parsing strategies.
        ----------
        Output:
            - columns: List with column names.
            - significance_type: The type of significance.
            - value_column: The value column.
        ----------
        """
        columns = list(KMA_COLUMNS.values())
        significance_type = "p-value"
        return columns, significance_type, columns.index(significance_type)

    def get_gene_column_name(self) -> str:
        """
        Getter function that returns the gene column name.
        This is used for creating the report.
        ----------
        Output:
            - str: The gene column name.
        ----------
        """
        return "Template"

    def requires_dataframe(self) -> bool:
        """
        Helper function to determine if the parser requires a data frame.
        The KMA/FASTQ parser does not require a data frame.
        For more specific information, see the ParserStrategy class.
        ----------
        Output:
            - bool: False
        ----------
        """
        return False

    def write_fasta_out(
        self,
        config_options: dict[str, Any],
        input_sequence_sample: str,
        list_of_genes: list[str],
        data_frame: Optional[pd.DataFrame] = None,
    ) -> None:
        """
        Function that writes the hits sequences to a FASTA file.
        The sequences are extracted from the alignment file
        using the AlignmentExtractor class.
        For methods and attributes, see the AlignmentExtractor class.
        ----------
        Input:
            - config_options: dict[str, Any]: The configuration options.
            - input_sequence_sample: str: The input sequence sample.
            - list_of_genes: list[str]: The list of genes.
        ----------
        """
        extractor = AlignmentExtractor(
            alignment_file=f"{config_options["database"]["run_output"]}{input_sequence_sample}.aln",
            genes_list=list_of_genes,
            output_file=f"{input_sequence_sample}_sequences.fasta",
        )
        extractor.run()
