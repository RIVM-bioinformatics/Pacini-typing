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
__data__ = "2024-10-28"


class InvalidFastaOrFastqError(Exception):
    """
    Raised when an invalid FASTA or FASTQ file is provided.
    """

    def __init__(self, file: str) -> None:
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
        ----------------------------------------------------
                """


class InvalidSequenceError(Exception):
    """
    Raised when an invalid sequence is provided.
    """

    def __init__(self, sequence: str, file: str) -> None:
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
    Raised when two different sequencing types are provided.
    """

    def __init__(self, files: list[str]) -> None:
        self.files = files

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: Wrong sequencing types detected
        ---------------------------------------------------
        The following files cannot be used together:
            - {self.files[0]}
            - {self.files[1]}
        ---------------------------------------------------
        SUGGESTION: Make sure you provide:
            - TWO fastq files
            - Or ONE fasta file
        ----------------------------------------------------
                """
