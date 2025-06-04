#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

This module is responsible for running the SNP query against the
reference database. PointFinder is called to run the SNP query,
using the BaseQueryRunner class as a base. The query is prepared
by the PointFinder runner and is then executed by the command invoker.
"""


__author__ = "Mark van de Streek"
__date__ = "2025-05-12"
__all__ = ["SNPQueryRunner"]

import json
import logging
import os

from command_utils import CommandInvoker, ShellCommand
from queries.base_query_runner import BaseQueryRunner
from queries.pointfinder_runner import PointFinder


class SNPQueryRunner(BaseQueryRunner):
    """
    Concrete implementation of the QueryRunner class
    for running SNP related queries (PointFinder).

    The class follows a command pattern, since the gene and
    SNP queries are following the same recipe, but only the
    some (small) parts are different.
    ----------
    Methods:
        - __init__: Constructor of the SNPQueryRunner class
        - extract_version_number: Method to extract the version number
            from the output of the version command
    ----------
    """

    def __init__(self, run_options: dict[str, str]) -> None:
        """
        Constructor class of the SNPQueryRunner class.
        This class is responsible for initializing the class.
        The checking of the PointFinder existence is additionally
        to the BaseQueryRunner abstract class and is only required
        for the SNP-related operations.

        In addition to the GeneQueryRunner, this class also has
        a method to download the PointFinder script.
        ----------
        Input:
            - run_options: dictionary with the input files,
                database, and output file
        ----------
        """
        super().__init__(run_options)
        self.check_pointfinder_existence(
            self.run_options["pointfinder_script_path"]
        )
        self.query = PointFinder.get_query(option=self.run_options)
        self.version_command = PointFinder.get_version_command()
        self.log_tool_version()

    def extract_version_number(self, stdout: str) -> str | None:
        """
        Function that extracts the version number
        of the incoming PointFinder output.
        PointFinder doesn't have a version command,
        so the version number is extracted from a request
        to the version history of the PointFinder API.
        ----------
        Input:
            - stdout: the output of the version command (json structure)
        Output:
            - str: the version number of the tool or
                Not available if the version number couldn't be extracted
        ----------
        """
        try:
            data = json.loads(stdout)
            return data["values"][0]["commit"]["date"]
        except Exception:
            logging.error(
                "Error extracting version number from PointFinder,"
                " returning 'Not available'..."
            )
            # The program should not crash if a version number could not
            # be extracted, but the error should be logged.
            return "Not available"

    def check_pointfinder_existence(self, path: str) -> None:
        """
        Function that checks if the PointFinder script exists
        and downloads if not present.
        Because the script is not available via Conda/PIP, this
        check is required to download the script.
        ----------
        Input:
            - path: Path to the PointFinder script
        ----------
        """
        if not os.path.isfile(path):
            logging.info("PointFinder script not found, downloading...")
            CommandInvoker(
                ShellCommand(
                    cmd=[
                        "wget",
                        "-O",
                        path,
                        "https://bitbucket.org/genomicepidemiology/pointfinder/raw/master/PointFinder.py",
                    ],
                    capture=True,
                )
            ).execute()
        else:
            logging.debug(
                "PointFinder script already exists, skipping download..."
            )
