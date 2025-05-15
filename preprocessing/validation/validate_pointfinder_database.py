#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Script that checks the structure and vadidity of the PointFinder reference database.
The existence of the database is checked, as well as the contents of some files
and the matching of genes in all required files.
"""

__author__ = "Mark van de Streek"
__date__ = "2025-04-29"
__all__ = ["PointFinderReferenceChecker"]

import logging
import os

import pandas as pd


class PointFinderReferenceChecker:
    """
    Checking class that is responsible for validating the reference
    database of PointFinder. The class checks the following:
        - Path to the database
        - Existence of the required files
        - Presence of all required gene sequences
    """

    def __init__(self, path_to_database: str) -> None:
        """
        Constructor method of the class that initializes the
        incoming path to the database and sets the required
        parameters for the class.
        ----------
        Input:
            - path_to_database: Path to the reference database
        ----------
        """
        self.unique_genes_resistens_overview: list[str] = []
        self.path: str = path_to_database
        self.resistance_overview: str = self.path + "/resistens-overview.txt"

    def check_path_directory(self) -> bool:
        """
        Little helper function to check if the database
        path exists and is a directory.
        ----------
        Output:
            - True if the path exists and is a directory
            - False if the path does not exist or is not a directory
        ----------
        """
        if os.path.exists(self.path):
            if os.path.isdir(self.path):
                return True
            else:
                logging.debug(
                    "Path: %s exists but is not a directory.", self.path
                )
                return False
        else:
            logging.debug("Path: %s does not exist.", self.path)
            return False

    def check_folder_structure(self) -> bool:
        """
        Function that checks the folder structure of the
        reference database directory and checks if the
        required files are present.
        This function does not check the contents of the files
        and assumes the existence of the folder is already checked.
        The function checks if the following files are present:
            - genes.fasta
            - genes.txt
            - resistens-overview.txt
            - RNA_genes.txt
        ----------
        Output:
            - True if all files are present
            - False if any file is missing
        ----------
        """
        required_files: list[str] = [
            "genes.fasta",
            "genes.txt",
            "resistens-overview.txt",
            "RNA_genes.txt",
        ]
        for file in required_files:
            if not os.path.isfile(os.path.join(self.path, file)):
                logging.debug("Missing required file: %s", file)
                return False
        logging.debug(
            "Database folder seems to be correct, checking files next..."
        )
        return True

    def check_resistens_overview_file(self) -> bool:
        """
        Function that checks the content of the
        resistens-overview.txt file of the reference database.
        This file is the most important file and holds the required
        information about the mutation.
        Required fields:
            - Gene_ID
            - Gene_name
            - Codon_pos
            - Ref_nuc
            - Ref_codon
            - Res_codon
            - Resistance
            - PMID
        *Note: self.unique_genes_resistens_overview is also set in this
        function, since for all genes present in the resistens-overview.txt
        file, a sequence is required and this list is used
        to check the genes later on.
        ----------
        Output:
            - True if the file is correct
            - False if the file is not correct
        ----------
        """
        required_fields: list[str] = [
            "#Gene_ID",
            "Gene_name",
            "Codon_pos",
            "Ref_nuc",
            "Ref_codon",
            "Res_codon",
            "Resistance",
            "PMID",
        ]
        logging.debug(self.resistance_overview)
        df: pd.DataFrame = pd.read_csv(
            self.resistance_overview, sep="\t", encoding="utf-8"
        )
        self.unique_genes_resistens_overview = df["#Gene_ID"].unique().tolist()
        if not all(field in df.columns for field in required_fields):
            missing_fields = [
                field for field in required_fields if field not in df.columns
            ]
            logging.debug("Missing required fields: %s", missing_fields)
            return False
        rows = len(df)
        if rows < 1:
            logging.info(
                "resistens-overview.txt does not contain any data rows."
            )
            return False
        logging.debug(
            "resistens-overview.txt contains the required fields, "
            "amount of rows in the file: %s",
            rows,
        )
        return True

    def get_gene_names(self) -> list[str]:
        """
        Helper function to extract the gene names from the
        genes.txt file of the reference database.
        The gene names must match the headers of the genes.fasta file
        and are therefore extracted.
        ----------
        Output:
            - genes_list: list of gene names
        ----------
        """
        with open(
            self.path + "/genes.txt", "r", encoding="utf-8"
        ) as genes_txt_file:
            return [line.strip() for line in genes_txt_file if line.strip()]

    def get_fasta_headers(self, filename: str) -> list[str]:
        """
        Helper function to extract headers from a fasta file.
        The function is general, so could be used for other
        fasta files as well.
        ----------
        Input:
            - filename: Path to the fasta file
                (i.e., home/secret_folder/genes.fasta)
        Output:
            - fasta_headers: list of fasta headers excluding the '>'
        ----------
        """
        with open(
            os.path.join(filename), "r", encoding="utf-8"
        ) as genes_fasta_file:
            return [
                line[1:].strip()
                for line in genes_fasta_file
                if line.startswith(">")
            ]

    def create_missing_genes_list(
        self, target_genes: list[str], available_genes: list[str]
    ) -> list[str] | None:
        """
        Little helper function to create a list of missing genes
        from the genes that are not present in the to be checked list.
        If no missing genes are found, the function returns None.
        ----------
        Input:
            - genes_list: list of genes to be checked
            - checking_list: list of genes to check against
        Output:
            - missing_genes: list of missing genes
        ----------
        """
        missing_genes: list[str] = [
            gene for gene in target_genes if gene not in available_genes
        ]
        return missing_genes if missing_genes else None

    def check_missing_genes(self, checks: dict[str, list[str] | None]) -> bool:
        """
        Function that walks over the dictionary of checks
        and checks if any of the values are not None.
        If any list in the dictionary is not None, this means
        some genes are missing in one combination.
        ----------
        Input:
            - checks: dictionary -> "file name" : [missing genes]
        Output:
            - True if any of the lists are not None
                (i.e., some genes are missing)
            - False if all lists are None
        ----------
        """
        has_missing_genes = False
        for file_name, missing_genes in checks.items():
            if missing_genes:
                logging.debug(
                    "The following genes are missing in %s: %s",
                    file_name,
                    missing_genes,
                )
                has_missing_genes = True

        return has_missing_genes

    def check_matching_genes_file(self) -> bool:
        """
        Function that checks if the genes listed in
        `genes.txt` are present in the `genes.fasta` file,
        if the headers are correct (starting with >) and
        if the genes present in the `resistens-overview.txt` file
        are also present in the `genes.fasta` file.
        ----------
        Output:
            - True if all genes are present
            - False if any gene is missing
        ----------
        """
        genes_list: list[str] = self.get_gene_names()
        fasta_headers = self.get_fasta_headers(self.path + "/genes.fasta")
        # Perform the checks for missing genes and
        # assign the result to the dictionary of all checks
        checks: dict[str, list[str] | None] = {
            "resistens-overview.txt": self.create_missing_genes_list(
                target_genes=self.unique_genes_resistens_overview,
                available_genes=genes_list,
            ),
            "genes.fasta": self.create_missing_genes_list(
                target_genes=self.unique_genes_resistens_overview,
                available_genes=fasta_headers,
            ),
            "genes.txt": self.create_missing_genes_list(
                target_genes=genes_list, available_genes=fasta_headers
            ),
        }
        # Check if any of the lists in the dictionary
        # are not None and log the missing genes
        has_missing_genes = self.check_missing_genes(checks)

        return not has_missing_genes

    def validate(self) -> bool:
        """
        Main function to run the validation of PointFinder's
        reference database. The function delegates the checks to
        other functions of this class. Finally, the function returns
        True if all checks passed and False if any check failed.
        ----------
        Output:
            - True if all checks passed
            - False if any check failed
        ----------
        """
        if (
            not self.check_path_directory()
            and not self.check_folder_structure()
        ):
            logging.warning(
                "Path to the reference database does not exists or"
                "does not have the correct structure"
            )
            return False
        if not self.check_resistens_overview_file():
            logging.warning("resistens-overview.txt file is not correct")
            return False
        if not self.check_matching_genes_file():
            logging.error("Error in the matching genes file")
            return False
        return True


if __name__ == "__main__":
    checker: PointFinderReferenceChecker = PointFinderReferenceChecker(
        "/Users/mvandestreek/Desktop/salm-simulation/pointfinder_db/Salmonella"
    )
    if checker.validate():
        logging.info("All checks passed. Database is ready to use...")
