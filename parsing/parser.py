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
from parsing.parsing_strategy import ParserStrategy


class Parser:
    """
    Parser class that is responsible for the parsing
    The class is using a strategy pattern to read and
    process the data.
    ----------
    Methods:
        - __init__: Constructor of the class
        - add_filter: Function to add a filter to the list of filters
        - apply_filters: Applies all filters to the DataFrame
        - read_run_output: Reads the output data using the strategy
        - construct_report_record: Constructs a record for the output report
        - create_output_report: Creates a filtered output report
        - write_report: Writes the report to a csv file
        - construct_list_of_genes: Constructs the list of genes/templates from the DataFrame
        - write_FASTA_out: Writes the FASTA output
        - parse: Main method to parse the file
    ----------
    """

    def __init__(
        self,
        config_options: dict[str, Any],
        strategy: ParserStrategy,
        query_run_filename: str,
        input_sequence_sample: str = "",
    ):
        """
        Constructor for the Parser class
        The incoming variables are stored as class variables
        and other variables are initialized here.
        ----------
        Input:
            - config_options: options from the configuration file
            - strategy: ParserStrategy object
            - query_run_filename: str (filename of the query results)
            - input_sequence_sample: sample name of the input sequence
        ----------
        """
        self.config_options = config_options
        self.strategy = strategy
        self.query_run_filename = query_run_filename
        self.input_sequence_sample = input_sequence_sample
        self.data_frame = pd.DataFrame()
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

    def apply_filters(self):
        """
        Function that applies all filters to the DataFrame
        It loops over the list of filters and applies them.
        The implementation of the filters is done in the Filter class.
        """
        for filter_pattern in self.filters:
            self.data_frame = filter_pattern.apply(self.data_frame)

    def read_run_output(self):
        """
        Function that handles the reading the run output of the query.
        It's not acutually being read here, but the strategy pattern
        is used to read the output file.
        """
        self.data_frame = self.strategy.read_output(self.query_run_filename)
        logging.info("Run output read successfully.")

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
                self.strategy.get_gene_column_name()
            ].values.tolist()
        ):
            output_records.append(
                self.construct_report_record(report_id, item)
            )
        return pd.DataFrame(output_records)

    def construct_hit_csv_record(
        self,
        columns: dict[str, Any],
        significance_type: str,
        value_column: str,
        report_id: int,
        item: list[str],
    ) -> dict[str, Any]:
        """
        Function that constructs a record for the hits report
        Every line in the hits report is a dictionary
        This function constructs the dictionary.
        In the create_hits_report function, the dictionary is
        appended to a list of all records.
        ----------
        Input:
            - columns: dict[str, Any]: columns of the DataFrame
            - significance_type: str: type of significance value
            - value_column: str: value of the significance
            - report_id: int: id of the record
            - item: list[str]: incoming item from the dataframe
        Output:
            - dict[str, Any]: dictionary with the record
        ----------
        """
        return {
            "ID": report_id + 1,
            "hit": item.iloc[columns.index("hit")].split(":")[0],
            "percentage identity": item.iloc[
                columns.index("percentage identity")
            ],
            "percentage coverage": item.iloc[
                columns.index("percentage coverage")
            ],
            significance_type: item.iloc[value_column],
        }

    def create_hits_report(self) -> pd.DataFrame:
        """
        Function that creates a csv file with
        all information about the hits.
        Where the report only holds the hit names,
        this report holds all information about the hits.
        Output example:
        ID,hit,percentage identity,percentage coverage,e/p-value
        1,rfbV,100.0,100.0,0.0
        2,ctxA,99.3,99.0,0.0
        3,ctxB,96.3,87.0,0.05
        ----------
        Output:
            - pd.DataFrame: hits report
        --------
        """
        output_records: list[dict[str, Any]] = []
        columns, significance_type, value_column = (
            self.strategy.get_hits_report_info()
        )
        for report_id, item in self.data_frame.iterrows():
            output_records.append(
                self.construct_hit_csv_record(
                    columns, significance_type, value_column, report_id, item
                )
            )
        return pd.DataFrame(output_records)

    def write_report(self, report: pd.DataFrame, suffix: str):
        """
        Function that writes a given DataFrame to a csv file.
        The pandas DataFrame is created by other methods,
        and passed to this method to write it to a file.
        ----------
        Input:
            - report: the DataFrame to write
            - suffix: suffix to add to the filename
        ----------
        """
        logging.debug("Writing the %s...", suffix)
        report.to_csv(
            f"{self.input_sequence_sample}_{suffix}.csv",
            sep=",",
            index=False,
        )
        logging.info("Successfully wrote the report")

    def construct_list_of_genes(self) -> list[str]:
        """
        Function that constructs the list of genes
        from the filtered DataFrame.
        This option is used to write the FASTA output.
        The list of genes is used to extract the sequence from
        alignment file of KMA.
        ! This function is not returning a list of genes
        that are searched for, but the actual hits !
        ----------
        Output:
            - list[str]: The list of genes after filtering
        --------
        """
        return self.strategy.extract_gene_list(self.data_frame)

    def write_fasta_out(self) -> None:
        """
        Function that is being called if the --fasta-out option
        is set to true by the user.
        The function is using the strategy pattern to write the
        found sequences to a FASTA file.
        """
        self.strategy.write_fasta_out(
            config_options=self.config_options,
            input_sequence_sample=self.input_sequence_sample,
            list_of_genes=self.construct_list_of_genes(),
            data_frame=(
                self.data_frame if self.strategy.requires_dataframe() else None
            ),
        )

    def parse(self) -> None:
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
        if not self.data_frame.empty:
            self.apply_filters()

        if not self.data_frame.empty:
            self.write_report(self.create_output_report(), "report")
            self.write_report(self.create_hits_report(), "hits_report")

            if self.config_options.get("fasta_out", False):
                self.write_fasta_out()
        else:
            logging.warning(
                "Data frame is empty after filtering, no report created"
            )
