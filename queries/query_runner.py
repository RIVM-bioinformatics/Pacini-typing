#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

This module is responsible for running the
right query against the reference database.

First, the query is prepared by the respective runner
(BLASTn or KMA). The query is then run by the QueryRunner
class. The runtime of the query is calculated and the result
is returned to the main script (pacini_typing.py).

The actual shell code will be executed by the
execute function of the command_utils.py module.
"""

from __future__ import annotations

__author__ = "Mark van de Streek"
__date__ = "2024-09-24"
__all__ = ["QueryRunner"]

import logging
import os
import re
import time
from typing import Any

from command_utils import CommandInvoker, ShellCommand
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
        self.version_command: str = ""
        self.start_time: float = 0.0
        self.stop_time: float = 0.0
        self.check_output_dir()
        if self.run_options["file_type"] == "FASTA":
            self.query = BLASTn.get_query(option=self.run_options)
            logging.info("Getting the BLAST version...")
            self.version_command = BLASTn.get_version_command()
        elif self.run_options["file_type"] == "FASTQ":
            self.query = KMA.get_query(option=self.run_options)
            logging.info("Getting the KMA version...")
            self.version_command = KMA.get_version_command()
        self.log_tool_version()

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
        if output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                logging.debug("New output directory created: %s", output_dir)
                return False
        logging.debug("Output directory exists...")
        return True

    @staticmethod
    def extract_version_number(stdout: str) -> str:
        """
        Method that extracts the version number from the tool output.
        The method uses a regular expression to extract the version number.
        ----------
        Input:
            - stdout: str: the output of the tool
        Output:
            - str: the version number of the tool
        ----------
        """
        version_pattern = r"(\d+\.\d+\.\d+)"
        match = re.search(version_pattern, stdout)

        return match.group(1) if match else None

    def log_tool_version(self) -> None:
        """
        Method that logs the version of the tool used.
        The method calls the get_version_command method
        from the respective runner.
        This logging functionality was developed at RIVM's request
        """
        stdout, stderr = CommandInvoker(
            ShellCommand(cmd=self.version_command, capture=True)
        ).execute()
        version = self.extract_version_number(stdout)
        logging.info("Version tool: %s", version)

    def run(self) -> None:
        """
        The query is already prepared in the constructor.
        This function runs the query.
        The runtime is started and stopped to calculate the runtime.
        (calculation is done in the get_runtime method)
        The decorated log function logs the query command,
            see the ./decorators/decorators.py file for more information.
            This decorator also checks if the query was successful.
        """
        logging.debug("Starting the query operation...")
        self.start_time = time.time()
        # Use the execute function of command_utils
        command = ShellCommand(cmd=self.query, capture=True)
        CommandInvoker(command).execute()
        self.stop_time = time.time()

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
