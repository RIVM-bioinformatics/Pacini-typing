#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

# TODO - Fill in later...
"""

__author__ = "Mark Van de Streek"
__date__ = "2024-10-28"


class InvalidDatabaseError(Exception):
    """
    Raised when an invalid database is provided.
    """

    def __init__(self, database_path: str, database_name: str) -> None:
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
