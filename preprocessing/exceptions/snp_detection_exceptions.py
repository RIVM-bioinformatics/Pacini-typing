#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Module that contains custom exceptions for SNP detection related code.
These exceptions are raised when Pacini-typing searches for SNPs or checks
the database of PointFinder
"""

__author__ = "Mark van de Streek"
__date__ = "2025-05-29"
__all__ = ["PointFinderScriptError", "PathError", "IncorrectSNPConfiguration"]


class PathError(Exception):
    """
    Raised when a error with the KMA/Blastn path occurs.
    """

    def __str__(self) -> str:
        return """
        ---------------------------------------------------
        ERROR: Path error
        ---------------------------------------------------
        CAUSE: Shutil probably couldn't find a path
        ---------------------------------------------------
        SUGGESTION:
            - Check the path to the KMA/Blastn tool:
                (`which kma` or `which blastn`)
            - Ensure the tool is installed and in the PATH
        """


class PointFinderScriptError(Exception):
    """
    Raised when the PointFinder script is not found or
    is wrong formatted.
    """

    def __init__(self, script_path: str) -> None:
        """
        Initialize the exception with the script path.
        ----------
        Input:
            - script_path: path to the PointFinder script
        ----------
        """
        self.script_path = script_path

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: PointFinder script not found
        ---------------------------------------------------
        The following PointFinder script could not be found:
            - Path: {self.script_path}
        ---------------------------------------------------
        SUGGESTION:
            - Make sure the script is a valid Python script
            - Check the path to the script
            - Check if the path was correctly defined in
                the config file:
                    - /path/to/PointFinder.py
        ----------------------------------------------------
                """


class IncorrectSNPConfiguration(Exception):
    """
    Raised when the SNP configuration is incorrect.
    """

    def __init__(self, config_path: str) -> None:
        """
        Initialize the exception with the config path.
        ----------
        Input:
            - config_path: path to the SNP configuration file
        ----------
        """
        self.config_path = config_path

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: Incorrect SNP cosnfiguration in config file
        ---------------------------------------------------
        The following SNP configuration file is incorrect:
            - Path: {self.config_path}
        ---------------------------------------------------
        SUGGESTION:
            - Check the SNP configuration file for correctness
            - Check the log file for more information
            - Check the "pattern" field in the config file
        ----------------------------------------------------
                """


class PointFinderReportError(Exception):
    """
    Raised when the PointFinder report is not found or
    is wrong formatted.
    """

    def __init__(self, report_path: str) -> None:
        """
        Initialize the exception with the report path.
        ----------
        Input:
            - report_path: path to the PointFinder report
        ----------
        """
        self.report_path = report_path

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: PointFinder's report not found
        ---------------------------------------------------
        The following PointFinder report could not be found:
            - Path: {self.report_path}
        ---------------------------------------------------
        SUGGESTION:
            - Read the above log message for the exact
                file name and see if the file exists
            - Most likely the PointFinder's script named
                the report file incosistently
            - Change input file name of the FASTA or FASTQ,
                without the use of any special characters
        ----------------------------------------------------
                """
