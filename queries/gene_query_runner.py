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

from queries.base_query_runner import BaseQueryRunner
from queries.blast_runner import BLASTn
from queries.kma_runner import KMA


class GeneQueryRunner(BaseQueryRunner):
    """
    Concrete implementation of the QueryRunner class
    for running Gene related queries (BLASTn or KMA).

    The class follows a command pattern, since the gene and
    SNP queries are following the same recipe, but only the
    some (small) parts are different.
    ----------
    Methods:
        - __init__: Constructor of the GeneQueryRunner class
        - extract_version_number: Method to extract the version number
            from the output of the version command
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
