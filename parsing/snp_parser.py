#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Module that contains the SNPParser class. This class is responsible
for reading, parsing and creating the output report for the SNPs.

*Please note this class is not following the strategy pattern like
the other parsers. This is due the bigger differences in the parsing.
"""

__author__ = "Mark van de Streek"
__date__ = "2025-05-13"
__all__ = ["SNPParser"]


import logging
from typing import Any

import pandas as pd
from pandas.core.api import DataFrame as DataFrame

from preprocessing.exceptions.snp_detection_exceptions import (
    PointFinderScriptError,
)


class SNPParser:
    """
    SNPParser class that is responsible for parsing the
    SNP related data from PointFinder.
    ----------
    Methods:
        - __init__: Constructor of the class
        - read_run_output: Reads the output data from PointFinder
        - get_sequence_change: Helper function to extract reference and alternative characters
        - get_mutation_position: Helper function to extract mutation position
        - construct_report_record: Constructs a record for the output report
        - create_output_report: Creates a filtered output report
        - parse: Main method to parse the file
    ----------
    """

    def __init__(
        self,
        config_options: dict[str, Any],
        input_sequence_sample: str,
        file_type: str,
        pointfinder_output_filename: str,
    ) -> None:
        """
        Constructor for the SNPParser class.
        The config options and input sequence sample are stored. The
        data frame is used to store the results of the PointFinder run.
        The output report is used to store the final output report.
        ----------
        Input:
            - config_options: The configuration options for the parser
            - input_sequence_sample: The input sequence sample
        ----------
        """
        self.config_options: dict[str, Any] = config_options
        self.input_sequence_sample: str = input_sequence_sample
        self.file_type: str = file_type
        self.pointfinder_output_filename: str = pointfinder_output_filename
        self.data_frame: DataFrame = pd.DataFrame()

    def read_run_output(self, filename: str) -> None:
        """
        Function that is responsible for reading the output of
        the PointFinder search and placing the results in a pandas data frame.
        The data frame is also formatted with the right column names.
        ----------
        Input:
            - filename: The name of the file to be read
        Output:
            - DataFrame: The data frame containing the results
        """
        logging.debug("Reading SNP run output from %s...", filename)
        self.data_frame = pd.read_csv(filename, sep="\t", header=0)

    def get_sequence_change(self, codon_output: str) -> tuple[str, str]:
        """
        Little helper function that extracts the reference and alternative
        characters from the codon output of PointFinder. The input of the
        function can be as followed:
        ACT -> CGT
        P -> R
        - -> GAT
        T -> C
        delA

        *named characters, since both nucleotides and amino acids can be
        passed to this function.
        ----------
        Input:
            - codon_output: The character(s) change output of PointFinder
        Output:
            - tuple: A tuple containing the reference and alternative
        """
        # Handle special cases first
        if codon_output == "frameshift":
            return "frameshift", "frameshift"

        # Handle all other cases
        if "->" in codon_output:
            ref, alt = codon_output.split("->")
        elif "-" in codon_output and not codon_output.startswith("del"):
            ref, alt = codon_output.split("-", 1)
        elif "del" in codon_output:
            parts = codon_output.split("del", 1)
            ref = parts[1] if len(parts) > 1 and parts[0] == "" else parts[0]
            alt = "-"
        else:
            # Default
            ref, alt = codon_output, codon_output

        return ref.strip(), alt.strip()

    def get_mutation_position(self, mutation: str) -> str:
        """
        Help function that extracts the mutation position
        from the mutation string.
        The input of the function can be as followed:
        folP p.P64R
        rpoB p.L533L
        gyrA p.S83F
        The positions should then be extracted:
        folP p.P64R -> 64
        rpoB p.L533L -> 533
        gyrA p.S83F -> 83
        ----------
        Input:
            - mutation: The mutation string / description
        Output:
            - str: The mutation position
        ----------
        """
        parts = mutation.split()
        if len(parts) < 2 or "." not in parts[1]:
            return ""
        # Get the part after the dot (e.g., "P64R")
        after_dot = parts[1].split(".")[1]
        # Extract digits from the string and return
        return "".join(char for char in after_dot if char.isdigit())

    def construct_report_record(
        self, index: int, item: pd.Series
    ) -> dict[str, Any]:
        """
        Function that constructs a single record for the output report.
        The incoming item is a row and the corresponding values are
        extracted from the data frame and helper functions are used.
        ----------
        Input:
            - index: The index of the record
            - item: The incoming item (row) from the data frame
        Output:
            - dict: A dictionary containing the record
        ----------
        """
        ref_nucl, alt_nucl = self.get_sequence_change(
            item["Nucleotide change"]
        )
        ref_aa, alt_aa = self.get_sequence_change(item["Amino acid change"])
        pos = self.get_mutation_position(item["Mutation"])
        return {
            "ID": index,
            "Input": self.input_sequence_sample,
            "Configuration": self.config_options["metadata"]["filename"],
            "Type/Genes": self.config_options["metadata"]["type"],
            "Mode": "SNP",
            "Hits": item["Mutation"].split(" ")[1],
            "Reference nucleotide": ref_nucl,
            "Alternative nucleotide": alt_nucl,
            "Position": pos,
            "Amino acid change": f"{ref_aa}{pos}{alt_aa}",
        }

    def create_output_report(self):
        """
        Function that creates the content for the output report.
        For every line in PointFinder's output, a record is created
        in the construct_report_record function. All the content is
        finally added to a list and converted to a pandas data frame
        in this function.
        ----------
        Output:
            - DataFrame: The output report as a pandas data frame
        ----------
        """
        logging.debug("Creating the output report...")
        output_records: list[dict[str, Any]] = []
        for index, (_, item) in enumerate(self.data_frame.iterrows(), start=1):
            output_records.append(self.construct_report_record(index, item))

        return pd.DataFrame(output_records)

    def parse(self):
        """
        Main parse function for the SNPParser class.
        The incoming file is passed to the read_run_output function and
        the output report creation is delegated.
        """
        logging.info("Parsing the SNP results...")
        try:
            self.read_run_output(self.pointfinder_output_filename)
        except FileNotFoundError as e:
            logging.error(
                "PointFinder's report not found: %s",
                self.pointfinder_output_filename,
            )
            raise PointFinderScriptError(
                self.pointfinder_output_filename
            ) from e
        except pd.errors.EmptyDataError:
            logging.warning(
                "No content in the query file, found no hits "
                "in the input files"
            )
        if not self.data_frame.empty:
            self.output_report = self.create_output_report()
