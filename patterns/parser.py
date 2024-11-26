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

from patterns.filter_pattern import Filter
from patterns.identity_filter import PercentageIdentityFilter
from patterns.name_filter import GeneNameFilter

# FIXME: Add the right import statements in sub-files of filtering

# TODO - Check for empty data_frame before creating the output report


KMA_COLUMNS = [
    "Template",
    "Score",
    "Expected",
    "Template_length",
    "Template_Identity",
    "Template_Coverage",
    "Query_Identity",
    "Query_Coverage",
    "Depth",
    "q_value",
    "p_value",
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
        input_sequence_sample: str = "",
    ) -> None:
        """
        Constructor
        Fill in later...
        """
        self.config_options = config_options
        self.run_output_filename = run_output_filename
        self.parse_type = parse_type
        self.input_sequence_sample = input_sequence_sample
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
        if self.parse_type == "FASTA":
            self.data_frame = pd.read_csv(
                self.run_output_filename + ".tsv",
                sep="\t",
                header=None,
            )
            self.set_fasta_options()
        else:
            self.data_frame = pd.read_csv(
                self.run_output_filename + ".res",
                sep="\t",
                header=0,
            )
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

    def create_output_report(self):
        """
        Function that creates a filtered output report
        Fill in later...
        """
        lines_in_output_report = []
        for report_id, item in enumerate(
            self.data_frame[
                "sseqid" if self.parse_type == "FASTA" else "Template"
            ].values.tolist()
        ):
            line = {
                "ID": report_id + 1,
                "Input": self.input_sequence_sample,
                "Configuration": self.config_options["metadata"]["filename"],
                "Type/Genes": self.config_options["metadata"]["type"],
                "Hits": item.split(":")[0],
            }
            lines_in_output_report.append(line)

        return pd.DataFrame(lines_in_output_report)

    def write_output_report(self):
        """
        Function that writes the filtered pandas dataframe
        to a csv file. Not the whole dataframe is written,
        only: "ID", "Input", "Schema", "Template", "Hits".
        """
        self.create_output_report().to_csv(
            f"{self.input_sequence_sample}_report.csv",
            sep=",",
            index=False,
        )

    def parse(self):
        """
        Parse the file
        Fill in later...
        """
        self.read_run_output()
        for filtering in self.filters:
            self.data_frame = filtering.apply(self.data_frame)
        self.write_output_report()


def main():
    """
    Test the read_run_output method
    """
    # file = "/Users/mvandestreek/Desktop/PaciniTestRun/MYRESULTS.res"
    file2 = "/Users/mvandestreek/Desktop/PaciniTestRun/output/FASTA_results.tsv.tsv"

    config_options: dict[str, Any] = {
        "metadata": {
            "filename": "O1.yaml",
            "id": "VIB-O1",
            "type": "V. cholerae O1 Genes",
            "description": "Genetic pattern run config file for Vibrio cholerae O1 serogroup",
            "date_created": "2024-11-06",
        },
        "database": {
            "name": "VIB-O1",
            "path": "databases",
            "matching_seq_file": "patterns/VIB-O1.fasta",
            "run_output": "output/",
        },
        "pattern": {
            "perc_ident": 95,
            "perc_cov": 90,
            "e_value": 0,
            "p_value": 0.05,
            "genes": [
                {
                    "gene_name": "rfbV",
                    "presence": True,
                    "pident": 98,
                    "pcoverage": 95,
                }
            ],
            "snps": None,
        },
    }
    TYPE = "FASTA"
    parser = Parser(config_options, file2, TYPE, "EA545")
    parser.add_filter(PercentageIdentityFilter(99, TYPE))
    parser.add_filter(GeneNameFilter(["rfbV_O1", "fimA"], TYPE))
    parser.parse()


if __name__ == "__main__":
    main()
