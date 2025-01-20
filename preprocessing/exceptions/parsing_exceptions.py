#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Module that contains custom exceptions for the parsing module.
Mostly these exceptions are raised when an error occurs during
the reading of the configuration file.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-11-06"
__all__ = ["YAMLLoadingError", "YAMLStructureError", "EmptySequenceError"]


class YAMLLoadingError(Exception):
    """
    Raised when an error occurs while loading a YAML file.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the exception with the file path.
        ----------
        Input:
            - file_path: path to the YAML file
        ----------
        """
        self.file_path = file_path

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: Loading YAML file failed
        ---------------------------------------------------
        The following YAML file could not be loaded:
            - Path: {self.file_path}
        ---------------------------------------------------
        SUGGESTION:
            - Make sure the file is a valid YAML file
            - Look at the example YAML files for guidance
            - Error most likely to be an indentation or
                '-' misplacement issue
        ---------------------------------------------------
                """


class YAMLStructureError(Exception):
    """
    Raised when an error occurs in the structure of a YAML file.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the exception with the file path.
        ----------
        Input:
            - file_path: path to the YAML file
        ----------
        """
        self.file_path = file_path

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: YAML file structure is incorrect
        ---------------------------------------------------
        The following YAML file has an incorrect structure:
            - Path: {self.file_path}
        ---------------------------------------------------
        SUGGESTION:
            - Check the structure of the YAML file
            - Ensure the indentation is correct
            - Make sure the keys are correctly aligned
        ---------------------------------------------------
                """


class EmptySequenceError(Exception):
    """
    Raised when an empty sequence is found in the data frame.
    """

    def __str__(self) -> str:
        return """
        ---------------------------------------------------
        ERROR: Empty sequence found in filtered data frame
        ---------------------------------------------------
        There were no sequences found in the data frame
        after filtering the found hits.
        Probably caused by the extraction of the sequences
        out of the filtered data frame.
        ---------------------------------------------------
        SUGGESTION:
            - Make sure the BLAST output format has 'qseq'
                column included at last index.
            - Check the extraction method for errors
        ---------------------------------------------------
                """
