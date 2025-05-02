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
__all__ = ["FileContentError"]


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


class FileContentError(Exception):
    """
    Raised when the content of a file is not as expected.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the exception with the file path.
        ----------
        Input:
            - file_path: path to the file
        ----------
        """
        self.file_path = file_path

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: File content error
        ---------------------------------------------------
        The following file has unexpected content:
            - Path: {self.file_path}
        ---------------------------------------------------
        SUGGESTION:
            - Check the file content for correctness
            - Ensure the file format is as expected
        ----------------------------------------------------
        """


class IncorrectStructureError(Exception):
    """
    Raised when the structure of a directory is not as expected.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the exception with the file path.
        ----------
        Input:
            - file_path: path to the file
        ----------
        """
        self.file_path = file_path

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: Incorrect structure error
        ---------------------------------------------------
        The following directory has an incorrect structure
            or does not exists:
            - Path: {self.file_path}
        ---------------------------------------------------
        SUGGESTION:
            - Check the directory structure for correctness
            - Ensure the directory contains the expected files
        ----------------------------------------------------
        """


class MissingGenesError(Exception):
    """
    Raised when the genes are missing from the database.
    For example, the `resistens-overview.txt` file contains
    genes for which no header is present in the fasta reference.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize the exception with the file path.
        ----------
        Input:
            - file_path: path to the file
        ----------
        """
        self.file_path = file_path

    def __str__(self) -> str:
        return f"""
        ---------------------------------------------------
        ERROR: Missing genes error
        ---------------------------------------------------
        The following reference database path is missing genes:
            - Path: {self.file_path}
        ---------------------------------------------------
        CAUSE:
            - `genes.txt` file contains genes for which no header
                is present in the fasta reference.
            - `restistens-overview.txt` file contains genes for which
                no header is present in the fasta reference.
        ----------------------------------------------------
        SUGGESTION:
            - Check the above error message for the missing genes
            - Check the reference database for missing genes
            - Ensure the reference database is complete
        ----------------------------------------------------
        """
