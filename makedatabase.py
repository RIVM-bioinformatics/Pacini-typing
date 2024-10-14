#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Python script that contains the DatabaseBuilder class.
This class is responsible for building a database using either KMA or BLAST.
For both methods, a subprocess.run command is used to execute the command in the terminal.
See the methods for more information.
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["DatabaseBuilder"]

import os
import subprocess
import logging
from decorators import decorators


class DatabaseBuilder:
    """
    Class that contains the methods to build a database using either KMA or BLAST.
    ----------
    Methods:
        - __init__: Constructor for the DatabaseBuilder class
        - build_database: Generic function to build a database using either KMA or BLAST
        - create_kma_database: Method that creates a KMA database
        - create_blast_database: Method that creates a BLAST database
    ----------
    """

    def __init__(self, arg_options):
        """
        Constructor for the DatabaseBuilder class.
        The constructor initializes the class attributes.
        These methods come from the input arguments dictionary / self option
        ----------
        Input used:
            - database_path: str
            - database_name: str
            - input_fasta_file: str
            - database_type: str
        """
        self.full_database_path = None
        self.database_path = arg_options["database_path"]
        self.database_name = arg_options["database_name"]
        self.input_fasta_file = arg_options["makedatabase"]["input"]
        self.database_type = arg_options["makedatabase"]["type"]
        self.build_database()

    def build_database(self) -> None:
        """
        Generic function to build a database using either KMA or BLAST.
        ----------
        Input:
            - database_path: str
            - database_name: str
            - input_fasta_file: str
            - database_type: str
        Output:
            - Database in the specified path
        ----------
        """
        self.full_database_path = os.path.join(self.database_path, self.database_name)
        if not os.path.exists(self.full_database_path):
            if self.database_type == "kma":
                if not os.path.exists(self.database_path):
                    logging.debug("Database path for KMA does not exist, creating path")
                    os.mkdir(self.database_path)
                self.create_kma_database()
            else:
                self.create_blast_database()
        else:
            logging.info("Database already exists in the specified path")

    @decorators.log
    def create_kma_database(self) -> subprocess.CompletedProcess:
        """
        kma_index -i input_fasta_file -o path + name
        ----------
        Input:
            - full_database_path: str
            - input_fasta_file: str
        Output:
            - Result of the subprocess.run
        ----------
        """
        logging.debug("Creating KMA database")
        result = subprocess.run([
                "kma_index",
                "-i", os.path.join(self.input_fasta_file),
                "-o", self.full_database_path
            ],
            capture_output=True,
            text=True,
            check=True)

        return result

    @decorators.log
    def create_blast_database(self) -> subprocess.CompletedProcess:
        """
        Method that creates a BLAST database using the makeblastdb command.
        The subprocess.run command is used to execute the command in the terminal.
        This object contains the return code, stdout and stderr and is being returned.
        makeblastdb -in input_fasta_file -dbtype nucl -out path + name
        ----------
        Input:
            - full_database_path: str
            - input_fasta_file: str
        Output:
            - Result of the subprocess.run
        ----------
        """
        logging.debug("Creating BLAST database")
        result = subprocess.run([
                "makeblastdb",
                "-in", os.path.join(self.input_fasta_file),
                "-dbtype", "nucl",
                "-out", self.full_database_path
            ],
            capture_output=True,
            text=True,
            check=True)

        return result
