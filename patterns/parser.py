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

import logging
from typing import Any

import pandas as pd

from patterns.filter_pattern import Filter

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

    def add_filter(self, filter_pattern: Filter) -> None:
        """
        Function to add a filter to the list of filters
        the list of filters is present as class variable
        The incoming object is an implementation of the Filter class
        ----------
        Input:
            - filter: Filter object
        ----------
        """
        logging.debug("Adding filter: %s", filter_pattern.__class__.__name__)
        self.filters.append(filter_pattern)

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

    def construct_report_record(
        self, report_id: int, item: str
    ) -> dict[str, Any]:
        """
        Function that constructs a record for the output report
        Every line in the output report is a dictionary
        This function constructs the dictionary.
        In the create_output_report function, the dictionary is
        appended to a list of all records.
        ----------
        Input:
            - report_id: int
            - item: str
        Output:
            - dict[str, Any]
        ----------
        """
        return {
            "ID": report_id + 1,
            "Input": self.input_sequence_sample,
            "Configuration": self.config_options["metadata"]["filename"],
            "Type/Genes": self.config_options["metadata"]["type"],
            "Hits": item.split(":")[0],
        }

    def create_output_report(self) -> pd.DataFrame:
        """
        Function that creates a filtered output report
        Fill in later...
        ----------
        Output:
            - pd.DataFrame
        --------
        """
        output_records = []
        for report_id, item in enumerate(
            self.data_frame[
                "sseqid" if self.parse_type == "FASTA" else "Template"
            ].values.tolist()
        ):
            output_records.append(
                self.construct_report_record(report_id, item)
            )
        return pd.DataFrame(output_records)

    def write_output_report(self):
        """
        Function that writes the filtered pandas dataframe
        to a csv file. Not the whole dataframe is written,
        only: "ID", "Input", "Schema", "Template", "Hits".
        """
        logging.debug("Writing the output report...")
        self.create_output_report().to_csv(
            f"{self.input_sequence_sample}_report.csv",
            sep=",",
            index=False,
        )
        logging.info("Successfully craeted the output report")

    def parse(self):
        """
        Parse the file
        Fill in later...
        """
        logging.info("Parsing the query results...")
        try:
            self.read_run_output()
        except FileNotFoundError:
            logging.error(
                "File containing query results not found, exiting..."
            )
        except pd.errors.EmptyDataError:
            logging.warning(
                "No content in the query file, found no hits "
                "in the input files"
            )
        logging.debug("Results were read successfully, filtering...")
        for filtering in self.filters:
            self.data_frame = filtering.apply(self.data_frame)
        if not self.data_frame.empty:
            self.write_output_report()
        else:
            logging.warning(
                "Data frame is empty after filtering, no report created"
            )
