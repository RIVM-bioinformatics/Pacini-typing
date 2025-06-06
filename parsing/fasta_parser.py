#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Implementation of the FASTA parsing strategy for the parsing module.
This module is responsible for parsing the output of the BLAST search.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-12-17"
__all__ = ["FASTAParser"]

import logging
from typing import Any, Optional

import pandas as pd

from parsing.alignment_extractor import AlignmentExtractor
from parsing.parsing_strategy import ParserStrategy
from preprocessing.exceptions.parsing_exceptions import EmptySequenceError

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
    "qseq": "alignment sequence in query",
    "slen": "subject length",
    "gaps": "number of gaps",
}


class FASTAParser(ParserStrategy):
    """
    Concrete implementation of the ParserStrategy interface
    for parsing the output of the BLAST search.
    This class holds all the methods essential for parsing.
    ----------
    Methods:
        - read_output: Method to read the output of the BLAST search
        - extract_gene_list: Method to extract the gene list from the data frame
        - get_hits_report_info: Method to get the hits report information
        - get_gene_column_name: Method to get the gene column name
        - requires_dataframe: Method to determine if the parser requires a data frame
        - write_fasta_out: Method to write the hits to a FASTA output file
    ----------
    """

    def read_output(self, filename: str) -> pd.DataFrame:
        """
        Function that is responsible for reading the output of
        the BLAST search and placing the results in a pandas data frame.
        The data frame is also formatted with the right column names.
        Finally, an additional column is added to the data frame
        that contains the percentage coverage
            (since blast does not output this by default).
        ----------
        Input:
            - filename: the name of the file to read
        Output:
            - data_frame: the data frame with the BLAST results
        ----------
        """
        logging.debug("Reading BLAST output file: %s...", filename)
        data_frame = pd.read_csv(filename + ".tsv", sep="\t", header=None)
        data_frame.columns = list(BLAST_COLUMNS.keys())
        data_frame["pident"] = data_frame["pident"].astype(float)
        data_frame["coverage_pct"] = (
            100
            * (data_frame["length"] - data_frame["gaps"])
            / data_frame["slen"]
        )

        return data_frame

    def extract_gene_list(self, data_frame: pd.DataFrame) -> list[str]:
        """
        This function is responsible for extracting the gene list
        out of the dataframe.
        The genes are simply split so that id's or codes are removed.
        ----------
        Input:
            - data_frame: the data frame with the BLAST results
        Output:
            - list with gene names
        ----------
        """
        return [
            gene.split(":")[0] for gene in data_frame["sseqid"].values.tolist()
        ]

    def get_hits_report_info(self) -> tuple[list[str], str, Any]:
        """
        Function that returns the columns, significance type, and value column
        for the hits report.
        These values differ between the different parsing strategies.
        Therefore, this function is implemented in the concrete classes.
        ----------
        Output:
            - columns: list with column names
            - significance_type: the type of significance
            - value_column: the value column
        ----------
        """
        columns = list(BLAST_COLUMNS.values())
        significance_type = "e-value"
        return columns, significance_type, columns.index(significance_type)

    def get_gene_column_name(self) -> str:
        """
        Basic getter function that returns the gene column name.
        This is used for creating the report.
        ----------
        Output:
            - the gene column name
        ----------
        """
        return "sseqid"

    def requires_dataframe(self) -> bool:
        """
        Helper function to determine if the parser requires a data frame.
        The BLAST/FASTA parser does require a data frame.
        For more specific information, see the ParserStrategy class.
        ----------
        Output:
            - bool True
        ----------
        """
        return True

    def write_fasta_out(
        self,
        config_options: dict[str, Any],
        input_sequence_sample: str,
        list_of_genes: list[str],
        data_frame: Optional[pd.DataFrame] = None,
    ) -> None:
        """
        Function that writes the hits to a FASTA output
        file for further analysis.
        ----------
        Input:
            - config_options: dict[str, Any]: the configuration options
            - input_sequence_sample: str: the input sequence sample
            - list_of_genes: list[str]: the list of genes
            - data_frame: pd.DataFrame: the data frame with the BLAST results
        ----------
        """
        logging.debug("Extracting sequences from BLAST output...")
        if data_frame is not None:
            query_sequences: dict[str, str] = {
                row["sseqid"]: row["qseq"] for _, row in data_frame.iterrows()
            }
        else:
            logging.error("No data frame found in FASTA parser, exiting...")
            raise EmptySequenceError()
        output_file = f"{input_sequence_sample}_sequences.fasta"
        if query_sequences:
            logging.debug("Sequences have been extracted, writing to file...")
            AlignmentExtractor.write_fasta(
                output_file=output_file,
                query_sequences=query_sequences,
            )
        logging.info("FASTA output successfully written to %s", output_file)
