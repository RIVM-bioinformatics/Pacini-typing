#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Abstract base class for the different query runners.
Both runners (genes and SNPs) are quite similar, but
differ in the preparing and extracting of version number.
This class defines the shared methods and variables and also
defines the abstract methods that require custom implementation.
"""

__author__ = "Mark van de Streek"
__date__ = "2025-04-30"
__all__ = ["BaseQueryRunner"]

import logging
import os
import time
from abc import ABC, abstractmethod

from command_utils import CommandInvoker, ShellCommand


class BaseQueryRunner(ABC):
    """
    Abstract base class for the different query runners.
    Both runners (genes and SNPs) share the same recipe,
    and therefore this class is used to counteract duplicate code.
    The code that is shared between the two runners is placed here.
    ----------
    Methods:
        - __init__: Constructor for the QueryRunner class (with shared variables)
        - check_output_dir: Method that checks if the output directory exists
        - (ABSTRACT) extract_version_number: Method that extracts the version number
            from the tool output
        - log_tool_version: Method that logs the version of the tool used
        - run: Method that runs the query
        - get_runtime: Method that returns the runtime of the query
    ----------
    """

    def __init__(self, run_options: dict[str, str]) -> None:
        """
        Constructor of the base class.
        The shared variables are initialized here and
        the arguments are coming from the input dictionary.
        The output directory is checked for existence.
        ----------
        Input:
            - run_options: dictionary with the input files,
                database, and output file
        ----------
        """
        self.run_options = run_options
        self.start_time: float = 0.0
        self.stop_time: float = 0.0
        self.query: list[str] = []
        self.version_command: list[str] = []
        self.check_output_dir()

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

    @abstractmethod
    def extract_version_number(self, stdout: str) -> str | None:
        """
        Abstract method that extracts the version number
        from the tool output.
        ----------
        Input:
            - stdout: the output of the version command
        Output:
            - str: the version number of the tool or
                None if not found
        ----------
        """
        pass

    def log_tool_version(self) -> None:
        """
        Method that logs the version of the tool used.
        The method calls the get_version_command method
        from the respective runner.
        This logging functionality was developed at RIVM's request

        *The extraction of the version number is a abstract method
        """
        stdout, stderr = CommandInvoker(
            ShellCommand(cmd=self.version_command, capture=True)
        ).execute()
        if stdout:
            logging.info(
                "Version tool: %s", self.extract_version_number(stdout)
            )

    def run(self) -> None:
        """
        The query is already prepared and this
        function runs the query. The runtime is started
        and stopped to calculate the runtime.
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
