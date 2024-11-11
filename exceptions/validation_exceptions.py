#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

# TODO - Fill in later...
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-10-22"


class InvalidPairedError(Exception):
    """
    Raised when the paired names provided are invalid.
    """

    def __init__(self, file1: str, file2: str) -> None:
        self.file1 = file1
        self.file2 = file2

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: Invalid paired names provided
        ---------------------------------------------------
        The following files were not paired correctly:
            - {self.file1}
            - {self.file2}
        ---------------------------------------------------
        SUGGESTION: follow the format below:
            - Make sure the files names are not the same
            - Make sure the contents are not the same
            - Filenames must contain either R1/R2 or _1/_2
        ----------------------------------------------------
                """


class InvalidFileExtensionError(Exception):
    """
    Raised when an invalid file extension is provided.
    """

    def __init__(self, file: str, all_valid_extensions: str) -> None:
        self.file = file
        self.all_valid_extensions = all_valid_extensions

    def __str__(self) -> str:
        formatted_extensions: str = "\n\t\t- ".join(self.all_valid_extensions)
        return f"""
        ---------------------------------------------------
        ERROR: Invalid file extension provided
        ---------------------------------------------------
        The following file has an invalid extension:
            - {self.file}
        ---------------------------------------------------
        SUGGESTION:
            - Make sure the file extension is valid
            - Valid extensions include:
                - {formatted_extensions}
            - All extensions can be found/changed at:
                -/config/accept_arguments.yaml
        ----------------------------------------------------
                """


class FileNotExistsError(Exception):
    """
    Raised when a file does not exist.
    """

    def __init__(self, file: str) -> None:
        self.file = file

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: File does not exist
        ---------------------------------------------------
        The following file does not exist:
            - {self.file}
        ---------------------------------------------------
        SUGGESTION:
            - Check the file path
            - Make sure the file exists
        ----------------------------------------------------
                """


class InvalidFilterOptionsError(Exception):
    """
    Raised when an invalid filter option is provided.
    """

    def __init__(self, filter_option: str) -> None:
        self.filter_option = filter_option

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: Invalid filter option provided
        ---------------------------------------------------
        The following filter value is invalid:
            - {self.filter_option}
        ---------------------------------------------------
        SUGGESTION:
            - Make sure the filter option is valid
            - Provide plausible filter options (i.e., id between 0-100)
        ----------------------------------------------------
                """


class ValidationError(Exception):
    """
    Raised when a validation error occurs.
    """

    def __init__(self) -> None:
        self.message = "validating_input_arguments.py raised a general error"

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: Validation Error with the provided arguments
        ---------------------------------------------------
        {self.message}
        ----------------------------------------------------
        SUGGESTION:
            - Debug the error message
            - Python3 pacini_typing.py -h for help
        ----------------------------------------------------
                """
