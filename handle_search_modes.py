#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Module that is responsible for handling the search modes,
this includes: checking for the existence of certain databases
and calling the right query related operations to the runner classes.

The functions run_gene_query and run_snp_query are imported, since
they are placed in a different module (for reusability reasons)
"""

__author__ = "Mark van de Streek"
__date__ = "2025-05-07"
__all__ = ["HandleSearchModes"]

import logging
from typing import Any

from makedatabase import DatabaseBuilder
from parsing.read_config_pattern import ReadConfigPattern
from preprocessing.exceptions.validate_database_exceptions import (
    InvalidDatabaseError,
    InvalidSNPDatabaseError,
)
from preprocessing.validation.validate_database import check_for_database_path
from queries.query_runners import run_gene_query, run_snp_query
from validate_pointfinder_database import PointFinderReferenceChecker
import sys


class HandleSearchModes:
    """
    Class responsible for handling different search modes of
    Pacini-typing. These search modes are:
    - genes
    - SNPs
    - both
    The class only handles configuration file related operations.
    ----------
    Methods:
        - check_valid_gene_database_path: Checks if the gene database exists
        - run_makedatabase: Runs the makedatabase operation
            (if the database does not exist)
        - check_valid_SNP_database: Checks if the SNP database exists
        - handle_gene_search_mode: Handles the gene search mode
        - handle_snp_search_mode: Handles the SNP search mode
        - handle: determines which search modes to run (both, genes, SNPs)
    ----------
    """

    def __init__(
        self,
        pattern: ReadConfigPattern,
        option: dict[str, Any],
    ) -> None:
        """
        Constructor for the HandleSearchModes class,
        the pattern and option variables are set. The search mode
        is extracted from the incoming option dictionary.
        ----------
        Input:
            - pattern: ReadConfigPattern object (config file)
            - option: Dictionary with all necessary information
        ----------
        """
        self.pattern: ReadConfigPattern = pattern
        self.option: dict[str, Any] = option
        self.search_mode: str = self.option["config"]["search_mode"].lower()

    def check_valid_gene_database_path(
        self, database_builder: dict[str, Any]
    ) -> bool:
        """
        Function that calls the validation operation for the database.
        This function is responsible for checking if the database exists.
        See the check_for_database_path function for more detailed information
        about the validation process.
        ----------
        Input:
            - database_builder: Dictionary with all necessary information
        Output:
            - True: If the database exists
            - False: If the database does not exist
        ----------
        """
        logging.debug("Checking if the database exists...")
        return check_for_database_path(database_builder)

    def run_makedatabase(self, database_creation_args: dict[str, Any]) -> None:
        """
        Function that runs the makedatonabase operation for the
        gene database. This function simply creates a new reference
        database.
        The DatabaseBuilder of the makedatabase.py is called.
        ----------
        Input:
            - database_creation_args: Dictionary with all necessary information
        ----------
        """
        logging.info("Creating the reference database...")
        DatabaseBuilder(database_creation_args)

    def check_valid_SNP_database(
        self, database_builder: dict[str, Any]
    ) -> bool:
        """
        Function that delegates the validating process of the
        SNP database. This validation process is done by the
        PointFinderReferenceChecker class before running the query.
        ----------
        Input:
            - database_builder: Dictionary with all necessary information
        ----------
        """
        checker: PointFinderReferenceChecker = PointFinderReferenceChecker(
            database_builder["SNP_database_path"]
            + "/"
            + database_builder["species"]
        )
        return checker.validate()

    def handle_gene_search_mode(self) -> None:
        """
        Main function that handles the gene related search mode,
        this function is called when the search mode is set to
        "genes" or "both".
        The function checks if the gene database exists, handles the
        creating of a new database if it does not exist and finally
        calls the query operation to the right runner class.
        """
        if not self.check_valid_gene_database_path(self.pattern.creation_dict):
            logging.debug("Database does not exist, creating the database...")
            self.run_makedatabase(self.pattern.creation_dict)
        logging.debug("Checking if the database was successfully created...")
        if not self.check_valid_gene_database_path(self.pattern.creation_dict):
            raise InvalidDatabaseError(
                self.pattern.creation_dict["database_name"],
                self.pattern.creation_dict["file_type"],
            )
        else:
            logging.debug("Database exists, starting the query operation...")
            run_gene_query(self.pattern.creation_dict)

    def handle_snp_search_mode(self) -> None:
        """
        Main function that handles the SNP related search mode,
        this function is called when the search mode is set to
        "SNPs" or "both".
        The function checks if the SNP database exists, handles the
        creating of a new database if it does not exist and calls the query
        related operations, just like the gene search mode.

        Helpful information:
        {'database_path': 'databases/VIB-O1',
        'database_name': 'VIB-O1',
        'input_fasta_file': '/Users/mvandestreek/Developer/pacini_typing/config/VIB-O1.fasta',
        'database_type': 'FASTA',
        'file_type': 'FASTA',
        'SNP_database_path': '/path/to/snp_database',
        'species': 'Yersinia',
        'method': 'blastn',
        'method_path': '/opt/homebrew/bin/blastn',
        'input_file_list': ['test_data/VIB_EA5348AA_AS.fasta'],
        'output': 'output/VIB_EA5348AA_AS', 'threads': 1}
        """
        logging.info(self.pattern.creation_dict)
        if not self.check_valid_SNP_database(self.pattern.creation_dict):
            logging.error(
                "SNP database not exist, creating still has to be implemented"
            )
            sys.exit(1)
        if not self.check_valid_SNP_database(self.pattern.creation_dict):
            raise InvalidSNPDatabaseError(
                self.pattern.creation_dict["SNP_database_path"]
                + "/"
                + self.pattern.creation_dict["species"]
            )
        else:
            logging.info(
                "SNP database exists, starting the query operation..."
            )
            run_snp_query(self.pattern.creation_dict)

    def handle(self) -> None:
        """
        Function that handles the calling of all the config
        related operations. The function simply checks which
        search mode is selected and calls the right function(s).
        """
        if self.search_mode in ["genes", "both"]:
            self.handle_gene_search_mode()
        if self.search_mode in ["snps", "both"]:
            self.handle_snp_search_mode()
