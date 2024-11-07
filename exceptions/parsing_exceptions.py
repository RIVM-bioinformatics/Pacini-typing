#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Fill in later...
"""

__author__ = "Mark Van de Streek"
__date__ = "2024-10-28"


class YAMLLoadingError(Exception):
    """
    Raised when an error occurs while loading a YAML file.
    """

    def __init__(self, file_path: str) -> None:
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
