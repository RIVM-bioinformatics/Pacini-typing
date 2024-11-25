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

__author__ = "Mark van de Streek"
__data__ = "2024-11-22"
__all__ = ["Parser"]

from typing import Any

import pandas as pd
from filter import Filter
from identity_filter import PercentageIdentityFilter
from name_filter import GeneNameFilter

# FIXME: Add the right import statements in sub-files of filtering


KMA_COLUMNS = [
    "Template_Name",
    "Template_Length",
    "Template_Identity",
    "Template_Coverage",
    "Template_Depth",
    "Query_Identity",
    "Query_Coverage",
    "Query_Depth",
    "Read_Count_Map",
    "Read_Count_Aln",
    "Score",
    "Expected",
    "q_value",
    "p_value",
    "ConClave_Score",
    "ConClave_Quality",
]

BLAST_COLUMNS = [
    "qseqid",
    "sseqid",
    "pident",
    "length",
    "mismatch",
    "gapopen",
    "qstart",
    "qend",
    "sstart",
    "send",
    "evalue",
    "bitscore",
]


class Parser:
    """
    Class for parsing files
    """

    def __init__(
        self,
        config_options: dict[str, Any],
        run_output_filename: str,
        parse_type: str,
    ) -> None:
        """
        Constructor
        Fill in later...
        """
        self.config_options = config_options
        self.run_output_filename = run_output_filename
        self.parse_type = parse_type
        self.data_frame: pd.DataFrame = pd.DataFrame()
        self.filters: list[Filter] = []

    def add_filter(self, filter: Filter) -> None:
        """
        Function to add a filter to the list of filters
        the list of filters is present as class variable
        The incoming object is an implementation of the Filter class
        ----------
        Input:
            - filter: Filter object
        ----------
        """
        self.filters.append(filter)

    def read_run_output(self):
        """
        Function that reads the run output file.
        Every line is stored as a dictionary in the pre_parse_results list.
        Format as follows:
        [
            {
                "0": "column 1 value",
                "1": "column 2 value",
                "2": "column 3 value",
                ...
            },
            {
                "0": "column 1 value",
                "1": "column 2 value",
                "2": "column 3 value",
                ...
            },]
        ----------
        """
        self.data_frame = pd.read_csv(
            self.run_output_filename,
            sep="\t",
            header=None if self.parse_type == "FASTA" else 0,
        )
        if self.parse_type == "FASTA":
            self.set_fasta_options()
        else:
            self.set_fastq_options()

    def set_fasta_options(self):
        """
        Set the options for parsing FASTA files
        Fill in later...
        """
        self.data_frame.columns = BLAST_COLUMNS
        self.data_frame["pident"] = self.data_frame["pident"].astype(float)

    def set_fastq_options(self):
        """
        Set the options for parsing FASTQ files
        Fill in later...
        """
        self.data_frame.columns = KMA_COLUMNS
        # Convert columns to float
        self.data_frame["Template_Identity"] = self.data_frame[
            "Template_Identity"
        ].astype(float)

    def parse(self):
        """
        Parse the file
        Fill in later...
        """
        self.read_run_output()
        for filtering in self.filters:
            self.data_frame = filtering.apply(self.data_frame)
        print(self.data_frame)
        # Go further from here....


def main():
    """
    Test the read_run_output method
    """
    file = "/Users/mvandestreek/Desktop/PaciniTestRun/output/FASTA_results.tsv.tsv"
    parser = Parser({"config": "config", "options": "options"}, file, "FASTA")

    parser.add_filter(PercentageIdentityFilter(99, "FASTA"))
    parser.add_filter(GeneNameFilter(["rfbV_O1", "fimA"], "FASTA"))
    parser.parse()


if __name__ == "__main__":
    main()
