#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Module that contains custom exceptions for the validate_database module.
These exceptions are raised when invalid database is provided or not found.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-10-28"
__all__ = ["InvalidDatabaseError"]


class InvalidDatabaseError(Exception):
    """
    Raised when an invalid database is provided.
    """

    def __init__(self, database_path: str, database_name: str) -> None:
        """
        Initialize the exception with the database path and name.
        ----------
        Input:
            - database_path: path to the database
            - database_name: name of the database
        ----------
        """
        self.database_path = database_path
        self.database_name = database_name

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: Database invalid or not found
        ---------------------------------------------------
        The following provided database is not valid:
            - Path: {self.database_path}
            - Name: {self.database_name}
        ---------------------------------------------------
        SUGGESTION:
            - Make sure the database path is correct
            - Make sure all database files are present:
                - For fasta/blast database:
                    - *.ndb, *.nhr, *.nin, *.njs,
                    - *.not, *.nsq, *.ntf, *.nto
                - For fastq/kma database:
                    - *.comp.b, *.length.b, *.name, *.seq.b
            - Make a new reference database, help:
            - python3 pacini_typing.py makedatabase -h
        ----------------------------------------------------
                """


class InvalidSNPDatabaseError(Exception):
    """
    Raised when an invalid SNP database is provided.
    """

    def __init__(self, database_path: str) -> None:
        """
        Initialize the exception with the database path.
        ----------
        Input:
            - database_path: path to the database
        ----------
        """
        self.database_path = database_path

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: SNP database invalid or not found
        ---------------------------------------------------
        The following provided SNP database is not valid:
            - Path: {self.database_path}
        ---------------------------------------------------
        SUGGESTION:
            - Make sure the SNP database path is correct
            - Make sure all required files are present
            - Make sure the SNP database is in the correct format
        -----------------------------------------------------
        """
