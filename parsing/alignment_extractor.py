#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

This module is responsible for extracting sequences from an alignment file.
KMA is outputting an alignment file with the following format:

# rfbV_O1:1:AE003852
template: 	ATGCCATGGAAGACCTACTCACGGAACTTGATGTATGCTGTCATAACTTTGATGTTGAAT
            ||||||||||||||||||||||||||||||_|||||||||||||||||||||||||||||
query:      ATGCCATGGAAGACCTACTCACGGAACTTGGTGTATGCTGTCATAACTTTGATGTTGAAT

# wbfZ_O139:1:AB012956
template: 	ATGTACTCAGGAGTGGAAAACAACATGGAAGTGGTTCATCACGGAGGGAAGGCGAGTGTC
            ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
query:    	ATGTACTCAGGAGTGGAAAACAACATGGAAGTGGTTCATCACGGAGGGAAGGCGAGTGTC

The above file found a hit for the gene rfbV_O1 and wbfZ_O139.
The sequences are aligned and the differences are shown.

The goal of is module is to provide a class that can extract sequences.
Not the alignment or search sequences, but the actual sequences that are found.

The above example would be extracted as:

>ctxA
TCATAATTCATCCTTAATTCTATTATGTGTATCAATATCAGATTGATAGCCTGAAAATAT

> Note: This class is only applicable for KMA output files,
blast outputs the found sequences in a column.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-12-17"
__all__ = ["AlignmentExtractor"]

import logging
import os

from preprocessing.exceptions.alignment_exceptions import (
    AlignmentFileNotFoundError,
)
from preprocessing.exceptions.parsing_exceptions import EmptySequenceError


class AlignmentExtractor:
    """
    Class that contains the methods to extract sequences
    from an alignment file. For an example extraction,
    see the top module docstring.
    ----------
    Methods:
        - __init__: Constructor for the AlignmentExtractor class
        - check_alignment_file: Method that checks if the alignment file exists
        - parse_alignment_file: Method that parses the alignment file
        - update_query_sequences: Method that updates the query sequences
        - get_gene_match: Method that matches the gene in the line
        - filter_genes: Method that filters the extracted genes
        - write_fasta: Method that writes the sequences to a fasta file
        - run: Method that runs the extraction
    ----------
    """

    def __init__(
        self, alignment_file: str, genes_list: list[str], output_file: str
    ) -> None:
        """
        Constructor method that accepts the file to extract from
        and the list of genes to extract.
        ----------
        Input:
            - alignment_file: Path to the alignment file
            - genes_list: list of genes to extract
            - output_file: Path to the output file
        ----------
        """
        self.alignment_file = alignment_file
        self.check_alignment_file()
        self.genes_list = genes_list
        self.output_file = output_file
        self.query_sequences: dict[str, str] = {}

    def check_alignment_file(self) -> None:
        """
        Method that checks if the alignment file exists.
        ----------
        Raises:
            - AlignmentFileNotFoundError: If the alignment file is not found
        --------
        """
        if not os.path.exists(self.alignment_file):
            logging.error(
                "Alignment file not found: %s, exiting...", self.alignment_file
            )
            raise AlignmentFileNotFoundError(self.alignment_file)

    def parse_alignment_file(self) -> None:
        """
        Method that parses the alignment file.
        The file is read line by line and the sequences
        are extracted by other methods. This method
        delegates the extraction to other methods.
        """
        logging.info("Parsing alignment file...")
        current_query_sequence: list[str] = []
        current_gene = None
        with open(self.alignment_file, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("#"):
                    current_gene, current_query_sequence = (
                        self.update_query_sequences(
                            line, current_query_sequence, current_gene
                        )
                    )
                elif line.startswith("query:"):
                    query_seq = line.split()[1]
                    query_seq = query_seq.replace("-", "").upper()
                    current_query_sequence.append(query_seq)
        # Save the last gene's sequence
        if current_gene and current_query_sequence:
            self.query_sequences[current_gene] = "".join(
                current_query_sequence
            )

    def update_query_sequences(
        self,
        line: str,
        current_query_sequence: list[str],
        current_gene: str | None,
    ) -> tuple[str | None, list[str]]:
        """
        Method that updates the query sequences.
        If the current gene and sequence are not None,
        the gene and sequence are saved.
        ----------
        Input:
            - line: current line from the alignment file
            - current_query_sequence: current query sequence list
            - current_gene: current gene
        Output:
            - tuple of the current gene and query sequence
        ----------
        """
        if current_gene and current_query_sequence:
            self.query_sequences[current_gene] = "".join(
                current_query_sequence
            )
        current_gene, current_query_sequence = self.get_gene_match(line)

        return current_gene, current_query_sequence

    def get_gene_match(self, line: str) -> tuple[str | None, list[str]]:
        """
        Function that matches the gene in the line
        and returns the gene and the current query sequence.
        ----------
        Input:
            - line: line from the alignment file
        Output:
            - tuple of the gene and the current query sequence
        ----------
        """
        current_query_sequence: list[str] = []
        current_gene = None
        line = line.split()[1]

        if line in self.genes_list:
            current_gene = line
            current_query_sequence = []

        return current_gene, current_query_sequence

    def filter_genes(self) -> None:
        """
        Basic method that filters the extracted genes.
        If the gene is not in the genes list, it is removed.
        Only the genes that are in the genes list are kept
        and then saved to a file later on.
        """
        self.query_sequences = {
            gene: seq
            for gene, seq in self.query_sequences.items()
            if gene in self.genes_list
        }

    @staticmethod
    def write_fasta(output_file: str, query_sequences: dict[str, str]) -> None:
        """
        Method that writes the sequences to a fasta file
        with a max line length of 70.
        Multiple sequences are written to the same file.
        ----------
        Input:
            - output_file: file path
            - query_sequences: sequences to write to the file
        ----------
        """
        logging.info("Writing found sequences to fasta file...")
        with open(output_file, "w", encoding="utf-8") as fasta_out:
            for gene, sequence in query_sequences.items():
                fasta_out.write(f">{gene}\n")
                for i in range(0, len(sequence), 70):
                    fasta_out.write(sequence[i : i + 70] + "\n")

    def run(self) -> None:
        """
        Run method of the file that is being called
        after the class is instantiated. This method
        calls all the other methods to extract the sequences.
        """
        self.parse_alignment_file()
        self.filter_genes()
        if self.query_sequences:
            self.write_fasta(self.output_file, self.query_sequences)
        else:
            logging.error("No sequences found in alignment file, exiting...")
            raise EmptySequenceError()
