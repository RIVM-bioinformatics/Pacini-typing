#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Module that handles all the parsing of the query results.
The results are read from the output file of the BLAST or KMA run.
The results are stored in a pandas dataframe.
After filtering, the results are written to multiple output files.
"""

__author__ = "Mark van de Streek"
__data__ = "2024-11-22"
__all__ = ["Parser"]

import logging
from typing import Any

import pandas as pd

from parsing.filter_pattern import Filter

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

BLAST_COLUMNS = {
    "qseqid": "query ID",
    "sseqid": "hit",
    "pident": "percentage identity",
    "length": "align. length",
    "mismatch": "number of mismatches",
    "gapopen": "number of gap openings",
    "qstart": "start of alignment in query",
    "qend": "end of alignment in query",
    "sstart": "start of alignment in hit",
    "send": "end of alignment in hit",
    "evalue": "e-value",
    "bitscore": "bit score",
    "qcovs": "percentage coverage",
}


class Parser:
    """
    Parser class that is responsible for the parsing
    ----------
    Methods:
        - __init__: Constructor
        - add_filter: Function to add a filter to the list of filters
        - read_run_output: Function that reads the run output file
        - set_fasta_options: Set the options for parsing FASTA files
        - set_fastq_options: Set the options for parsing FASTQ files
        - construct_report_record: Function that constructs a record for the output report
        - create_output_report: Function that creates a filtered output report
        - write_output_report: Function that writes the filtered pandas dataframe to a csv file
        - parse: Main method to parse the file
    ----------
    """

    def __init__(
        self,
        config_options: dict[str, Any],
        query_run_filename: str,
        parse_type: str,
        input_sequence_sample: str = "",
    ) -> None:
        """
        Constructor for the Parser class
        The incoming variables are stored as class variables
        and other variables are initialized here.
        ----------
        Input:
            - config_options: options from the configuration file
            - query_run_filename: str (filename of the query results)
            - parse_type: str (FASTA or FASTQ)
            - input_sequence_sample: sample name of the input sequence
        ----------
        """
        self.config_options = config_options
        self.query_run_filename = query_run_filename
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
        Function that reads the run output of the query.
        The file is read into a pandas dataframe.
        Based on the type of the run, the options are either
        being set for FASTA or FASTQ files.
        """
        if self.parse_type == "FASTA":
            self.data_frame = pd.read_csv(
                self.query_run_filename + ".tsv",
                sep="\t",
                header=None,
            )
            self.set_fasta_options()
        else:
            self.data_frame = pd.read_csv(
                self.query_run_filename + ".res",
                sep="\t",
                header=0,
            )
            self.set_fastq_options()

    def set_fasta_options(self):
        """
        Function that sets the specific options
        for parsing FASTA files.
        This means that the columns are set and
        the columns that should be converted to float
        are converted.
        """
        self.data_frame.columns = list(BLAST_COLUMNS.keys())
        self.data_frame["pident"] = self.data_frame["pident"].astype(float)
        self.data_frame["qcovs"] = self.data_frame["qcovs"].astype(float)

    def set_fastq_options(self):
        """
        Function that sets the specific options
        for parsing FASTQ files.
        This means that the columns are set and
        the columns that should be converted to float
        """
        self.data_frame.columns = list(KMA_COLUMNS.keys())
        self.data_frame["Template_Identity"] = self.data_frame[
            "Template_Identity"
        ].astype(float)
        self.data_frame["Template_Coverage"] = self.data_frame[
            "Template_Coverage"
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
            - report_id: int: id of the record
            - item: str: incoming item from the dataframe
        Output:
            - dict[str, Any]: dictionary with the record
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
        This report holds the most important information
        to quickly check the results.
        > No specific values are stored in the report,
        > only the hits after filtering.
        Output example:
        ID,Input,Configuration,Type/Genes,Hits,
        1,SAMPLE123,O1-scheme.yaml,V. cholerae O1 related genes,rfbV
        2,SAMPLE123,O1-scheme.yaml,V. cholerae O1 related genes,ctxA
        3,SAMPLE123,O1-scheme.yaml,V. cholerae O1 related genes,ctxB
        ----------
        Output:
            - pd.DataFrame: output report
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
        Function that writes the created
        output report to a csv file.
        The filename is based on the input sequence sample.
        """
        logging.debug("Writing the output report...")
        self.create_output_report().to_csv(
            f"{self.input_sequence_sample}_report.csv",
            sep=",",
            index=False,
        )
        logging.info("Successfully craeted the output report")

    def construct_hit_csv_record(
        self,
        columns: dict[str, Any],
        significance_type: str,
        value_column: str,
        report_id: int,
        item: list[str],
    ) -> dict[str, Any]:
        """
        # TODO: Add docstring
        """
        return {
            "ID": report_id + 1,
            "hit": item.iloc[columns.index("hit")].split(":")[0],
            "percentage Identity": item.iloc[
                columns.index("percentage identity")
            ],
            "percentage Coverage": item.iloc[
                columns.index("percentage coverage")
            ],
            significance_type: item.iloc[value_column],
        }

    def create_hits_report(self):
        """
        Function that creates a csv file with
        all information about the hits.
        Where the report only holds the hit names,
        this report holds all information about the hits.
        """
        output_records: list[dict[str, Any]] = []
        if self.parse_type == "FASTA":
            columns = list(BLAST_COLUMNS.values())
            significance_type = "e-value"
            value_column = columns.index(significance_type)
        else:
            columns = list(KMA_COLUMNS.values())
            significance_type = "p-value"
            value_column = columns.index(significance_type)

        for report_id, item in self.data_frame.iterrows():
            output_records.append(
                self.construct_hit_csv_record(
                    columns, significance_type, value_column, report_id, item
                )
            )
        return pd.DataFrame(output_records)

    def write_hits_report(self):
        """
        Function that writes the created
        hits report to a csv file.
        ...
        """
        logging.debug("Writing the hits report...")
        self.create_hits_report().to_csv(
            f"{self.input_sequence_sample}_hits_report.csv",
            sep=",",
            index=False,
        )
        logging.info("Successfully craeted the hits report")

    def parse(self):
        """
        Main method of the parsing class
        This method is called after initializing all
        the variables and filters.
        The reading is placed within a try-except block,
        this because the file might be empty (no variants found).
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
        if self.data_frame.empty:
            logging.warning(
                "Data frame is empty after filtering, no report created"
            )
        else:
            self.write_output_report()
            self.write_hits_report()
