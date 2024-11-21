#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Module that is responsible for running the
right query against the reference database.

First, the query is prepared by the respective runner
(BLASTn or KMA). The query is then run by the QueryRunner
class. The runtime of the query is calculated and the result
is returned to the main script (pacini_typing.py).

The actual shell code will be executed by the
execute function of the command_utils.py module.
"""

from __future__ import annotations

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["QueryRunner"]

import logging
import os
import time
from typing import Any, Tuple

from command_utils import execute
from queries.blast_runner import BLASTn
from queries.kma_runner import KMA


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
        self.check_output_dir()
        logging.debug("Preparing the query...")
        if self.run_options["file_type"] == "FASTA":
            self.query = BLASTn.get_query(option=self.run_options)
        elif self.run_options["file_type"] == "FASTQ":
            self.query = KMA.get_query(option=self.run_options)

    def check_output_dir(self) -> bool:
        """
        Method that checks if the output directory exists.
        If the directory does not exist, it will be created.
        ----------
        Output:
            - bool: True if the directory exists, False otherwise
        ----------
        """
        logging.debug("Checking if the output directory exists...")
        output_dir = os.path.dirname(self.run_options["output"])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            return False
        return True

    def run(self) -> Tuple[str, str] | bool:
        """
        The query is already prepared in the constructor.
        This function runs the query.
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


# Implement of a possible QueryRunnerBuilder class
# This class is not used in the current implementation
# class QueryRunnerBuilder:
#     """
#     # TODO - Fill in later...
#     """
#
#     def __init__(self):
#         """
#         Fill in later...
#         """
#         self.run_options = {}
#
#     def set_file_type(self, file_type: str) -> QueryRunnerBuilder:
#         """
#         Fill in later...
#         """
#         self.run_options["file_type"] = file_type
#         return self
#
#     def set_input_file_list(self, input_file: list[str]) -> QueryRunnerBuilder:
#         """
#         Fill in later...
#         """
#         self.run_options["input_file_list"] = input_file
#         return self
#
#     def set_database_path(self, database_path: str) -> QueryRunnerBuilder:
#         """
#         Fill in later...
#         """
#         self.run_options["database_path"] = database_path
#         return self
#
#     def set_database_name(self, database_name: str) -> QueryRunnerBuilder:
#         """
#         Fill in later...
#         """
#         self.run_options["database_name"] = database_name
#         return self
#
#     def set_output(self, output: str) -> QueryRunnerBuilder:
#         """
#         Fill in later...
#         """
#         self.run_options["output"] = output
#         return self
#
#     def build(self) -> QueryRunner:
#         """
#         Fill in later...
#         """
#         return QueryRunner(self.run_options)
