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

from make_gene_database import GeneDatabaseBuilder
from make_snp_database import SNPDatabaseBuilder
from parsing.read_config_pattern import ReadConfigPattern
from preprocessing.exceptions.validate_database_exceptions import (
    InvalidDatabaseError,
    InvalidSNPDatabaseError,
)
from preprocessing.validation.validate_database import check_for_database_path
from preprocessing.validation.validate_pointfinder_database import (
    PointFinderReferenceChecker,
)
from queries.query_runners import run_gene_query, run_snp_query


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
        self.file_type: str = self.pattern.creation_dict["file_type"]

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
        The DatabaseBuilder of the make_gene_database.py is called.
        ----------
        Input:
            - database_creation_args: Dictionary with all necessary information
        ----------
        """
        logging.info("Creating the reference database...")
        GeneDatabaseBuilder(database_creation_args)

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
            database_builder["path_snps"] + "/" + database_builder["species"]
        )
        return checker.validate()

    def validate_or_create_SNP_database(self) -> None:
        """
        Small function that checks if the database exists,
        creates it if it does not exist and checks if it was created
        successfully. If the database was not created successfully,
        an error is raised.
        ----------
        Raises:
            - InvalidSNPDatabaseError: If the SNP database was not created
                successfully or does not exist.
        ----------
        """
        logging.debug(
            "Checking if the SNP database exists"
            "and trying to create it if it does not exist..."
        )
        if not self.check_valid_SNP_database(self.pattern.creation_dict):
            SNPDatabaseBuilder(self.pattern.creation_dict)
        if not self.check_valid_SNP_database(self.pattern.creation_dict):
            # Check again if the SNP database was created, and raise an
            # error if it was not created successfully.
            logging.error(
                "SNP database not valid, "
                "already tried to create it, exiting..."
            )
            raise InvalidSNPDatabaseError(
                self.pattern.creation_dict["path_snps"]
                + "/"
                + self.pattern.creation_dict["species"]
            )

    def handle_fastq_snp_query(self) -> None:
        """
        Function that handles the SNP query especially for FASTQ files.
        This option requires an additional GENE database check and/or creation.
        Therefore, the functionality is separated
        from the handle_snp_search_mode.
        KMA requires a indexed gene database to search for SNPs in FASTQ files,
        this is why we need to check if the gene database exists here.
        Blastn can directly search for SNPs in FASTA files.
        """
        custom_database_builder: dict[str, Any] = {
            "database_path": self.pattern.creation_dict["path_snps"]
            + "/"
            + self.pattern.creation_dict["species"],
            "database_name": self.pattern.creation_dict["species"],
            "file_type": self.file_type,
        }
        logging.debug(
            "Checking if the gene database exists for the FASTQ file type..."
        )
        if self.check_valid_gene_database_path(custom_database_builder):
            run_snp_query(self.pattern.creation_dict)
        else:
            logging.warning(
                "Gene database does not exist inside SNP database, "
                "trying to create it..."
            )
            self.create_genes_database(custom_database_builder)
            if not self.check_valid_gene_database_path(
                custom_database_builder
            ):
                raise InvalidDatabaseError(
                    custom_database_builder["database_name"],
                    custom_database_builder["file_type"],
                )
            else:
                run_snp_query(self.pattern.creation_dict)

    def create_genes_database(
        self, custom_database_builder: dict[str, Any]
    ) -> None:
        """
        Little helper function that creates the gene database
        for the SNP database. it's confusing, but the PointFinder database
        requires a gene database only when the file type is FASTQ.
        The developed class is used for this purpose, with different params.
        ----------
        Input:
            - custom_database_builder: Dictionary with necessary information
        ----------
        """
        custom_database_builder["input_fasta_file"] = (
            f"{self.pattern.creation_dict['path_snps']}/"
            f"{self.pattern.creation_dict['species']}/genes.fasta"
        )
        custom_database_builder["database_type"] = "FASTQ"
        GeneDatabaseBuilder(custom_database_builder)

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
        """
        self.validate_or_create_SNP_database()
        logging.info("SNP database exists, starting the query operation...")
        if self.file_type == "FASTQ":
            logging.info(
                "File type is FASTQ, starting additional validation steps..."
            )
            # File type is FASTQ, PointFinder requires again a indexed
            # database, so we can reuse our own creation class to achieve
            # this. The database is created in the same directory as the
            # SNP database, but with the name of the species (as required)
            self.handle_fastq_snp_query()
        else:
            logging.info(
                "File type is FASTA, starting the SNP query operation..."
            )
            run_snp_query(self.pattern.creation_dict)

    def handle(self) -> None:
        """
        Function that handles the calling of all the config
        related operations. The function simply checks which
        search mode is selected and calls the right function(s).
        """
        logging.info("Handling search modes...")
        if self.search_mode in ["genes", "both"]:
            logging.debug(
                "Search mode is set to 'genes' or 'both', "
                "handling gene search mode..."
            )
            self.handle_gene_search_mode()
        if self.search_mode in ["snps", "both"]:
            logging.debug(
                "Search mode is set to 'snps' or 'both', "
                "handling SNP search mode..."
            )
            self.handle_snp_search_mode()
