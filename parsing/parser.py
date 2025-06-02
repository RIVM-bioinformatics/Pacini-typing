#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

This script is the main implementation of the strategy pattern.
This script is therefore delegating the reading, filtering
and writing of the found hits to the specific strategy.
An incoming parameter is used to define the strategy.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-11-08"
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
        file_type: str = "",
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
        self.file_type = file_type
        self.data_frame = pd.DataFrame()
        self.filters: list[Filter] = []
        self.output_report: pd.DataFrame = pd.DataFrame()

    def add_filter(self, filter_pattern: Filter) -> None:
        """
        Function to add a filter to the list of filters
        the list of filters is present as class variable
        The incoming object is an implementation of the Filter class
        ----------
        Input:
            - filter: Filter object to add to the list of filters
        ----------
        """
        logging.debug("Adding filter: %s", filter_pattern.__class__.__name__)
        self.filters.append(filter_pattern)

    def apply_filters(self) -> None:
        """
        Function that applies all filters to the DataFrame
        It loops over the list of filters and applies them.
        The implementation of the filters is done in the Filter class.
        """
        logging.debug("Applying filters to the data frame...")
        for filter_pattern in self.filters:
            self.data_frame = filter_pattern.apply(self.data_frame)

    def read_run_output(self) -> None:
        """
        Function that handles the reading the run output of the query.
        It's not actually being read here, but the strategy pattern
        is used to read the output file.
        """
        self.data_frame = self.strategy.read_output(self.query_run_filename)

    def construct_report_record(
        self,
        index: int,
        item: pd.Series,
        columns: dict[str, Any],
        significance_type: str,
        value_column: str,
    ) -> dict[str, Any]:
        """
        Function that constructs a record for the output report
        Every line in the output report is a dictionary
        This function constructs the dictionary.
        In the create_output_report function, the dictionary is
        appended to a list of all records.
        ----------
        Input:
            - index: id of the record
            - item: incoming item from the dataframe
            - columns: columns of the DataFrame
            - significance_type: type of significance value
            - value_column: value of the significance
        Output:
            - dictionary with the record
        ----------
        """
        return {
            "ID": index,
            "Input": self.input_sequence_sample,
            "Configuration": self.config_options["metadata"]["filename"],
            "Type/Genes": self.config_options["metadata"]["type"],
            "Mode": "Gene",
            "Hits": item.iloc[columns.index("hit")].split(":")[0],
            "Percentage Identity": round(
                item.iloc[columns.index("percentage identity")], 3
            ),
            "Percentage Coverage": (
                round(item["coverage_pct"], 3)
                if self.file_type == "FASTA"
                else item.iloc[columns.index("percentage coverage")]
            ),
            significance_type: item.iloc[value_column],
        }

    def create_output_report(self) -> pd.DataFrame:
        """
        Function that creates a filtered output report
        This report holds the information to check the results.
        Output example:
        ID,Input,Configuration,Type/Genes,Hits,Percentage Identity,Percentage Coverage
        1,SAMPLE123,O1-scheme.yaml,V. cholerae O1 related genes,rfbV,100.0,1.0
        2,SAMPLE123,O1-scheme.yaml,V. cholerae O1 related genes,ctxA,100.0,1.0
        3,SAMPLE123,O1-scheme.yaml,V. cholerae O1 related genes,ctxB,100.0,1.0
        ----------
        Output:
            - output report to write to a csv file
        --------
        """
        logging.debug("Creating the output report...")
        output_records: list[dict[str, Any]] = []
        columns, significance_type, value_column = (
            self.strategy.get_hits_report_info()
        )

        for index, (_, item) in enumerate(self.data_frame.iterrows(), start=1):
            output_records.append(
                self.construct_report_record(
                    index, item, columns, significance_type, value_column
                )
            )

        return pd.DataFrame(output_records)

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
            - The list of genes after filtering
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
        logging.info("--fasta-out options selected, writing FASTA output...")
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
            self.output_report = self.create_output_report()
            if self.config_options.get("fasta_out", False):
                self.write_fasta_out()
        else:
            logging.warning(
                "There were no hits left after filtering, no reports were created..."
            )
