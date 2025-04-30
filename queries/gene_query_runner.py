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
__all__ = ["GeneQueryRunner"]

import logging
import re
from typing import Any

from queries.blast_runner import BLASTn
from queries.kma_runner import KMA
from queries.base_query_runner import BaseQueryRunner


class GeneQueryRunner(BaseQueryRunner):
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
        Constructor of the GeneQueryRunner class,
        the super class is used to initialize the shared variables.
        The query is prepared by the respective runner (BLASTn or KMA)
        with some logic to determine which one to use.
        Also, the preparation of the version command is delegated.
        ----------
        Input:
            - run_options: dictionary with the input files,
                database, and output file
        ----------
        """
        super().__init__(run_options)
        if self.run_options["file_type"] == "FASTA":
            self.query = BLASTn.get_query(option=self.run_options)
            logging.info("Getting the BLAST version...")
            self.version_command = BLASTn.get_version_command()
        elif self.run_options["file_type"] == "FASTQ":
            self.query = KMA.get_query(option=self.run_options)
            logging.info("Getting the KMA version...")
            self.version_command = KMA.get_version_command()
        self.log_tool_version()

    def extract_version_number(self, stdout: str) -> str | None:
        """
        Implementation of the abstract method from the base class.
        The method gets an output string from the command and
        simply extract the version using regex.
        ----------
        Input:
            - stdout: the output of the version command
        Output:
            - str: the version number of the tool or
                None if not found
        ----------
        """
        version_pattern = r"(\d+\.\d+\.\d+)"
        match = re.search(version_pattern, stdout)

        return match.group(1) if match else None
