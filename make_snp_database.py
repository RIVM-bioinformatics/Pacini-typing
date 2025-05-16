#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Module that is responsible for creating PointFinder's SNP database.
This operation is done using multiple functions and consists of a couple
key steps:
1. Create the output directory for the SNP database
2. Validate the input genes file containing the gene sequences
    in which the mutation is present
3. Create the genes.txt file containing the gene IDs of the genes file
4. For each gene, create a separate file containing the gene sequence,
    names as the gene ID (e.g. "rpoB.fsa").
5. Create the resistens-overview.txt file containing the mutations
6. Create the RNA_genes.txt file (required by PointFinder)

The validation of the input genes file is done using the
earlier developed InputFileInspector class, which
is also used to validate the input FASTA sequence files.
"""

__author__ = "Mark van de Streek"
__date__ = "2025-05-15"
__all__ = ["SNPDatabaseBuilder"]

# Define the headers for the resistens-overview.txt file
RESISTENS_OVERVIEW_HEADERS = [
    "#Gene_ID",  # Gene ID
    "Gene_name",  # Gene name
    "Codon_pos",  # Mutation position (integer)
    "Ref_nuc",  # Reference codon
    "Ref_codon",  # Reference amino acid
    "Res_codon",  # Alternative amino acid(s) (comma-separated if multiple)
    "Resistance",  # Resistance drug(s) (comma-separated if multiple)
    "PMID",  # PMID(s) (comma-separated if multiple)
]

import os
from typing import Any

from codon_table_enum import CodonTable
from preprocessing.validation.determine_input_type import InputFileInspector


class SNPDatabaseBuilder:
    """
    Class that contains the methods to build a database for
    PointFinder using the input arguments.
    ----------
    Methods:
        - __init__: Constructor of the class
        - check_and_create_directory: Check if the output directory exists
            and create it if it does not.
        - _get_snp_database_path: Get the SNP database path
        - _write_gene_headers: Write the gene headers to the genes.txt file
        - _create_individual_gene_files: Create the individual gene files
            required for the PointFinder database (*.fsa)
        - build_gene_database: Delegates the gene-related operations
            to the helper functions.
        - construct_resistens_overview_record: Construct a single record
            for the resistens-overview.txt file
        - generate_resistens_overview_lines: Generate the content for the
            resistens-overview.txt file
        - create_resistens_overview_file: Delegate the creation of the
            resistens-overview.txt file to the helper functions.
        - create_RNA_file: Create the RNA_genes.txt file
    ----------
    """

    def __init__(self, arg_options: dict[str, Any]) -> None:
        """
        Constructor for the DatabaseBuilder class.
        The constructor initializes the class attributes
        and calls the methods to create the database.
        ----------
        Input:
            - arg_options: dictionary with the input arguments
                for the database builder.
        ----------
        """
        self.pointfinder_genes_file: str = arg_options[
            "pointfinder_genes_file"
        ]
        self.SNP_database_path: str = arg_options["SNP_database_path"]
        self.SNP_database_path = self._get_snp_database_path()
        self.species: str = arg_options["species"]
        self.SNP_list: list[dict[str, str]] = arg_options["SNP_list"]
        # Use the InputFileInspector class to check
        # the validity of the pointfinder_genes_file
        InputFileInspector([self.pointfinder_genes_file])
        # Start the database creation process
        self.check_and_create_directory()
        self.build_gene_database()
        self.create_resistens_overview_file()
        self.create_RNA_file()

    def check_and_create_directory(self) -> None:
        """
        Function that creates the output directory
        for the SNP database if it does not exist.
        otherwise, it will just return.
        """
        if not os.path.exists(f"{self.SNP_database_path}/{self.species}"):
            os.makedirs(
                f"{self.SNP_database_path}/{self.species}", exist_ok=True
            )

    def _get_snp_database_path(self) -> str:
        """
        Function that constructs the right path for the SNP database.
        The path is constructed by removing the trailing
        slash from the SNP_database_path if it exists.
        ----------
        Output:
            - str: The SNP database path without the trailing slash
        ----------
        """
        if self.SNP_database_path.endswith("/"):
            return self.SNP_database_path[:-1]
        else:
            return self.SNP_database_path

    def _write_gene_headers(self, headers: list[str]) -> None:
        """
        Function that writes the gene headers to the
        genes.txt file.
        PointFinder requires every gene to be listed in this file
        and corresponding to the gene ID given in the
        resistens-overview.txt file.
        ----------
        Input:
            - headers: list of gene IDs (headers) to be written
                to the genes.txt file.
        ----------
        """
        with open(
            f"{self.SNP_database_path}/{self.species}/genes.txt",
            "w",
            encoding="utf-8",
        ) as txt_file:
            for header in headers:
                txt_file.write(f"{header.lstrip(">")}\n")

    def _create_individual_gene_files(self, gene_info: dict[str, str]) -> None:
        """
        Function that creates the individual gene files
        required for the PointFinder database.
        Every file will be named after the gene ID
        (e.g. "rpoB.fsa") and will contain the
        corresponding gene sequence.
        ----------
        Input:
            - gene_info: dictionary with the gene ID as key
            and the gene sequence as value.
        ----------
        """
        for header, sequence in gene_info.items():
            gene_id: str = header.lstrip(">")
            with open(
                f"{self.SNP_database_path}/{self.species}/{gene_id}.fsa",
                "w",
                encoding="utf-8",
            ) as gene_file:
                gene_file.write(f">{gene_id}\n")
                for i in range(0, len(sequence), 70):
                    gene_file.write(sequence[i : i + 70] + "\n")

    def build_gene_database(self) -> None:
        """
        Function that opens the pointfinder_genes_file and performs two
        operations:
            1. Constructs a dictionary with the gene ID (header) as key and the
                gene sequence as value.
            2. Delegates the writing of the gene headers to `genes.txt`
            3. Delegates the creation of the individual gene files
                ending with `.fsa`
        ----------
        """
        gene_info: dict[str, str] = {}
        with open(self.pointfinder_genes_file, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith(">"):
                    header = line.strip()
                    gene_info[header] = ""
                else:
                    gene_info[header] += line.strip()

        self._write_gene_headers(list(gene_info.keys()))
        self._create_individual_gene_files(gene_info)

    def construct_resistens_overview_record(
        self, mutation: dict[str, str]
    ) -> dict[str, str]:
        """
        Basic function that constructs a single record for the
        resistens-overview.txt file given the mutation information.
        The corresponding values are extracted and added to the record.
        * The function uses the CodonTable class to get the
            reference amino acid for the reference nucleotide.
        * Resistance is set to "Custom" and the PMID is set to "-",
            this are VERY IMPORTANT fields for finding custom
            mutations in the database.
        ----------
        Input:
            - mutation: The mutation information as a dictionary
                containing the SNP, position, reference nucleotide,
                and alternative nucleotide.
        Output:
            - dict: A dictionary containing the record for the
                resistens-overview.txt file
        ----------
        """
        return {
            "Gene_ID": mutation["SNP"],
            "Gene_name": mutation["SNP"],
            "Codon_pos": mutation["pos"],
            "Ref_nuc": mutation["ref"],
            "Ref_codon": CodonTable.get_amino_acid(mutation["ref"]),
            "Res_codon": mutation["alt"],
            "Resistance": "Custom",
            "PMID": "-",
        }

    def generate_resistens_overview_lines(self):
        """
        Function that is responsible for creating the content
        of the resistens-overview.txt file.
        The construct_resistens_overview_record function is used to
        create a single record for the resistens-overview.txt file.
        The records are then added to a list and the list is
        returned back to the main resistens-overview creator function.
        ----------
        Output:
            - list: List with the content of the resistens-overview.txt file
        ----------
        """
        lines: list[str] = ["\t".join(RESISTENS_OVERVIEW_HEADERS) + "\n"]
        for mutation in self.SNP_list:
            record = self.construct_resistens_overview_record(mutation)
            lines.append(
                "\t".join(
                    str(record[key.lstrip("#")])
                    for key in RESISTENS_OVERVIEW_HEADERS
                )
                + "\n"
            )

        return lines

    def create_resistens_overview_file(self) -> None:
        """
        Function that create the resistens-overview.txt file
        inside the database path folder.
        This is the key file for PointFinder's reference database
        and holds the information for all mutations.
        """
        with open(
            f"{self.SNP_database_path}/{self.species}/resistens-overview.txt",
            "w",
            encoding="utf-8",
        ) as file:
            file.writelines(self.generate_resistens_overview_lines())

    def create_RNA_file(self) -> None:
        """
        Function that creates a required RNA file for the
        PointFinder database.
        * This file is not actually used, but it is required
        to have it in the database. PointFinder will raise an
        error if it is not present.
        """
        open(
            f"{self.SNP_database_path}/{self.species}/RNA_genes.txt",
            "w",
            encoding="utf-8",
        ).close()
