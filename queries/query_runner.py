#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

To be filed in later...
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["QueryRunner"]

import logging
import os
import sys
import time
from typing import Tuple, Any

from queries.blast_runner import BLASTn
from queries.kma_runner import KMA

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from command_utils import execute


class QueryRunner:
    """
    Main class that runs the input query against the reference database.
    The query is prepared by the prepare_query method from the respective runner.
    ----------
    Methods:
        - __init__: Constructor for the QueryRunner class
        - run: Method that runs the query
        - get_runtime: Method that returns the runtime of the query
    ----------
    """

    def __init__(self, run_options: dict[str, Any]) -> None:
        """
        Constructor of the QueryRunner class.
        The constructor calls the prepare_query method based on
        the input type (FASTA/FASTQ).
        The arguments are coming from the input dictionary.
        ----------
        Input used:
            - input_file_type: str
            - input_file: str
            - database_path: str
            - database_name: str
            - output_file: str
        ----------
        """
        self.run_options = run_options
        self.start_time = 0.0
        self.stop_time = 0.0

        logging.debug("Preparing the query...")
        if self.run_options["file_type"] == "FASTA":
            self.query = BLASTn.get_query(option=self.run_options)
        elif self.run_options["file_type"] == "FASTQ":
            self.query = KMA.get_query(option=self.run_options)

    def __str__(self) -> str:
        """
        Readable representation of the class.
        This function is called when the class is printed.
        """
        return f"QueryRunner(query={self.query})"

    def run(self) -> Tuple[str, str] | bool:
        """
        The query is already prepared in the constructor. This function runs the query.
        The runtime is started and stopped to calculate the runtime.
        The decorated log function logs the query command,
            see the ./decorators/decorators.py file for more information.
            This decorator also checks if the query was successful.
        ----------
        Output:
            - Result of the subprocess.run
        ----------
        """
        logging.debug("Running query...")
        self.start_time = time.time()
        # Use the execute function from command_utils
        result = execute(self.query, capture=True)
        self.stop_time = time.time()

        return result

    def get_runtime(self) -> float:
        """
        Simple method that returns the runtime of the query.
        The function is called in a logging event in the
        main script (pacini_typing.py).
        ----------
        - Output:
            - float: with the runtime in seconds
        ----------
        """
        logging.debug("Getting the runtime of the query...")
        return round((self.stop_time - self.start_time), 2)
