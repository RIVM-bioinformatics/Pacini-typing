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

The query is prepared by the respective runner
(BLASTn or KMA) and is then run by the QueryRunner
class.
The actual shell code will be executed by the
execute function of the command_utils.py module.
"""

from __future__ import annotations

__author__ = "Mark van de Streek"
__date__ = "2024-10-02"
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
        - check_output_dir: Method that checks if the output directory exists
        - extract_version_number: Method that extracts the version number from the tool output
        - log_tool_version: Method that logs the version of the tool used
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
        Input:
            - run_options: dictionary with the input files,
                database, and output file
        ----------
        """
        self.run_options = run_options
        self.version_command: list[str] = []
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
    def extract_version_number(stdout: str) -> str | None:
        """
        Method that extracts the version number from the tool output.
        The method uses a regular expression to extract the version number.
        ----------
        Input:
            - stdout: str: the output of the tool
        Output:
            - str: the version number of the tool or
                None if not found
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
        logging.info("Version tool: %s", self.extract_version_number(stdout))

    def run(self) -> None:
        """
        The query is already prepared in the constructor.
        This function runs the query.
        The runtime is started and stopped to calculate the runtime.
        (calculation is done in the get_runtime method)
        """
        logging.debug("Starting the query operation...")
        self.start_time = time.time()
        CommandInvoker(ShellCommand(cmd=self.query, capture=True)).execute()
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
