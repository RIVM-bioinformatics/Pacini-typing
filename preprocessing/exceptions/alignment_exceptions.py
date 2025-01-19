#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Module that contains the exceptions for the extraction of
sequences from an alignment file (AlignmentExtractor).
"""

__author__ = "Mark van de Streek"
__date__ = "2024-12-17"
__all__ = ["AlignmentFileNotFoundError"]


class AlignmentFileNotFoundError(Exception):
    """
    Raised when the alignment file is not found.
    """

    def __init__(self, file: str) -> None:
        self.file = file

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: Alignment file not found
        ---------------------------------------------------
        The alignment file was not found:
            - {self.file}
        ---------------------------------------------------
        SUGGESTION:
            - Check the file path and try again
        ----------------------------------------------------
                """
