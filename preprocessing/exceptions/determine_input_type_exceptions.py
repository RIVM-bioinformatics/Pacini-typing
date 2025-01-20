#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Module that contains custom exceptions for the determine_input_type module.
These exceptions are raised when invalid input is provided to the module.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-10-28"
__all__ = [
    "InvalidFastaOrFastqError",
    "InvalidSequenceError",
    "InvalidSequencingTypesError",
]


class InvalidFastaOrFastqError(Exception):
    """
    Raised when an invalid FASTA or FASTQ file is provided.
    """

    def __init__(self, file: str) -> None:
        """
        Initialize the exception with the file path.
        ----------
        Input:
            - file: path to the invalid FASTA or FASTQ file
        ----------
        """
        self.file = file

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: Invalid FASTA or FASTQ file provided
        ---------------------------------------------------
        The following file is not a valid FASTA or FASTQ file:
            - {self.file}
        ---------------------------------------------------
        SUGGESTION:
            - Make sure the file is in FASTA or FASTQ format
            - Check the file extension
            - If the file is FASTA, make sure it contains:
                >Header
                Sequence
            - If the file is FASTQ, make sure it contains:
                @Header
                Sequence
                +
                Quality Scores
        ----------------------------------------------------
                """


class InvalidSequenceError(Exception):
    """
    Raised when an invalid sequence is provided.
    """

    def __init__(self, sequence: str, file: str) -> None:
        """
        Initialize the exception with the invalid sequence and file path.
        ----------
        Input:
            - sequence: invalid sequence
            - file: path to the file containing the invalid sequence
        ----------
        """
        self.sequence = sequence
        self.file = file

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: Invalid sequence provided in {self.file}
        ---------------------------------------------------
        The following invalid sequence was found:
            - {self.sequence}
        ---------------------------------------------------
        SUGGESTION:
            - Make sure the sequence contains only:
                A, T, C, G or N characters
        ----------------------------------------------------
                """


class InvalidSequencingTypesError(Exception):
    """
    Raised when invalid sequencing types are provided.
    """

    def __init__(self, files: list[str]) -> None:
        """
        Initialize the exception with the list of files.
        ----------
        Input:
            - files: list of files with different sequencing types
        ----------
        """
        self.files = files

    def __str__(self) -> str:
        files_list: str = "\n\t\t- ".join(self.files)
        return f"""
        ---------------------------------------------------
        ERROR: Wrong sequencing types detected
        ---------------------------------------------------
        The following files cannot be used together
            due to different sequencing types:
            - {files_list}
        ---------------------------------------------------
        SUGGESTION: Make sure you provide:
            - TWO fastq files
            - Or ONE fasta file
        ----------------------------------------------------
                """
