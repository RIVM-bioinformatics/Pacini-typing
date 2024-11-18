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

__author__ = "Mark Van de Streek"
__data__ = "2024-10-30"
__all__ = ["Parser"]

from typing import Any

import pandas as pd

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
        self.pre_parse_results: list[dict[str, Any]] = []
        self.data_frame: pd.DataFrame = pd.DataFrame()

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
            self.set_FASTA_options()
        else:
            self.set_FASTQ_options()

    def set_FASTA_options(self):
        """
        Set the options for parsing FASTA files
        Fill in later...
        """
        self.data_frame.columns = BLAST_COLUMNS
        self.data_frame["pident"] = self.data_frame["pident"].astype(float)

    def set_FASTQ_options(self):
        """
        Set the options for parsing FASTQ files
        Fill in later...
        """
        self.data_frame.columns = KMA_COLUMNS
        # Convert columns to float
        self.data_frame["Template_Identity"] = self.data_frame[
            "Template_Identity"
        ].astype(float)

    def rule_perc_identity(self) -> pd.DataFrame:
        """
        Rule to filter the results based on the percentage identity
        Fill in later...
        """
        if self.parse_type == "FASTA":
            return self.data_frame["pident"] > 99
        return self.data_frame["Template_Identity"] > 99

    def rule_gene_filter(self, gene_name: str) -> pd.DataFrame:
        """
        Rule to filter the results based on the gene name
        """
        if self.parse_type == "FASTA":
            # Filter op basis van 'sseqid'
            return self.data_frame["sseqid"].str.contains(
                gene_name, case=False, na=False
            )
        return self.data_frame["Template_Name"].str.contains(
            gene_name, case=False, na=False
        )

    def parse(self):
        """
        Parse the file
        Fill in later...
        """
        self.read_run_output()
        print(
            self.data_frame[
                (self.rule_perc_identity())
                & (self.rule_gene_filter("rfbV_O1"))
            ]
        )


def main():
    """
    Test the read_run_output method
    """
    file = "/Users/mvandestreek/Desktop/PaciniTestRun/output/FASTA_results.tsv.tsv"

    parser = Parser({"config": "config", "options": "options"}, file, "FASTA")
    parser.parse()

    file2 = "/Users/mvandestreek/Desktop/PaciniTestRun/output/FASTQ_results.tsv.tsv"

    parser2 = Parser(
        {"config": "config", "options": "options"}, file2, "FASTQ"
    )
    parser2.parse()


if __name__ == "__main__":
    main()
