#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

# TODO: Add a docstring to this module
"""

__author__ = "Mark van de Streek"
__date__ = "2024-10-28"


class SubprocessError(Exception):
    """
    Raised when an error occurs in the subprocess module.
    """

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: Subprocess error occurred
        ---------------------------------------------------
        Subprocess couldn't successfully execute the
        given commandline command.
        Error message:
            - {self.message}
        ---------------------------------------------------
        SUGGESTION:
            - Sometimes, this occurs when a file/dir does not exist or
                has incorrect file permissions
            - The tool may not be installed or in the PATH
            - Use the --verbose option to see where the error occurred
            - In last case,
                Copy the command and run it in the terminal
        ---------------------------------------------------
                """
