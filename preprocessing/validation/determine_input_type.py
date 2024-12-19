#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

This script is responsible for determining the input file type.
Additionally, it checks if the input files are valid FASTA or FASTQ.
The type is also checked if the input files are of the same type.

Example FASTA File:
    >MY Sequence
    ATCGTACGATCGATCGATCGATCGATCGATCG

Example FASTQ File:
    @My Sequence
    ATCGTACGATCGATCGATCGATCGATCGATCG
    +
    B@@FDFFFHHGHHJIJJIIJJJJIJIJIIJJI
"""

__author__ = "Mark Van de Streek"
__date__ = "2024-09-24"
__all__ = ["InputFileInspector"]

import logging
import re
from typing import TextIO

from preprocessing.exceptions.determine_input_type_exceptions import (
    InvalidFastaOrFastqError,
    InvalidSequenceError,
    InvalidSequencingTypesError,
)


class InputFileInspector:
    """
    Class that is responsible for determining and
    validating the input file.
    It takes a file as input and checks if the
    file is a valid FASTA or FASTQ file.
    The determined file is returned by the class.
    ----------
    Methods:
        - __init__: Constructor for the InputFileInspector class
        - determine_file_type: Method that determines the file type
        - validate_fasta: Method that validates the FASTA file
        - validate_fastq: Method that validates the FASTQ file
        - validate_sequence_length: Method that validates the sequence length
        - validate_plus_line: Method that validates the '+' line in FASTQ
        - validate_sequence: Method that validates the sequence
        - compare_types: Method that compares the types of the input files
        - get_file_type: Getter method to retrieve the file type
    ----------
    """

    def __init__(self, input_files: list[str]) -> None:
        """
        Constructor of the class. It initializes the class with the input files.
        Additionally, it initializes the body and type dictionaries.
        It calls the retrieve_body and determine_file_type functions.
        And with paired files, it calls the compare_types function.
        ----------
        Input:
            - input_files: list with the input files
        ----------
        """
        self.input_files = input_files
        self.body: dict[str, list[str]] = {}
        self.type: dict[str, str] = {}
        self.determine_file_type()
        if len(self.type) == 2:
            self.compare_types()

    def determine_file_type(self) -> None:
        """
        Main logic function of the class that does the checking.
        The function first checks the first line of the file.
        If the line starts with '>', the type is set to FASTA,
        and the file is validated further assuming it is a FASTA file.
        If the line starts with '@', the type is set to FASTQ,
        and the file is validated further assuming it is a FASTQ file.
        If during the validation of the rest of the file,
        an invalid structure is found, both the FASTA and FASTQ
        validation functions raise an error.
        ----------
        Raises:
            - InvalidFastaOrFastqError: If the file is not a valid
        ----------
        """
        logging.debug("Walking through input filename(s) and reading them...")
        for file in self.input_files:
            with open(file, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if first_line.startswith(">"):
                    # FASTA file validation
                    self.type[file] = "FASTA"
                    f.seek(0)
                    self.validate_fasta(f, file)
                elif first_line.startswith("@"):
                    # FASTQ file validation
                    self.type[file] = "FASTQ"
                    f.seek(0)
                    self.validate_fastq(f, file)
                else:
                    logging.error("Invalid file format found. Exiting...")
                    raise InvalidFastaOrFastqError(file)

    def validate_fasta(self, file_handle: TextIO, file: str) -> None:
        """
        Function that validates the FASTA file format.
        The function assumes the file is a FASTA file
        and is designed to validate this type of file.
        ----------
        Input:
            - file_handle: open file handle
        ----------
        """
        sequence: list[str] = []
        has_header = False  # Track if any header is found

        for line in file_handle:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                has_header = True
                # If we had a previous sequence, validate it
                if sequence:
                    self.validate_sequence("".join(sequence), file)
                    sequence = []
            else:
                sequence.append(line)

        if not has_header:
            logging.error("No headers found in FASTA file: %s", file)
            raise InvalidFastaOrFastqError(
                f"No headers found in FASTA file: {file}"
            )

        # Validate the last sequence
        if sequence:
            self.validate_sequence("".join(sequence), file)

    def validate_fastq(self, file_handle: TextIO, file: str) -> None:
        """
        Function that validates the FASTQ file format.
        The function assumes the file is a FASTQ file
        and is designed to validate this type of file.
        The function reads the file line by line and validates
        the structure of the file.
        The function raises an error if the file is invalid.
        ----------
        Input:
            - file_handle (file): Open file handle
            - file (str): Filename for error reporting
        Raises:
            - InvalidFastaOrFastqError: If the FASTQ file is invalid
        ----------
        """
        file_handle.seek(0)
        while True:
            header_line = file_handle.readline().strip()
            if not header_line:
                break
            seq_line = file_handle.readline().strip()
            plus_line = file_handle.readline().strip()
            qual_line = file_handle.readline().strip()

            self.validate_plus_line(file, plus_line)
            self.validate_sequence(seq_line, file)
            self.validate_sequence_length(file, seq_line, qual_line)

    def validate_sequence_length(
        self, file: str, seq_line: str, qual_line: str
    ):
        """
        Simple function that validates the length of the
        sequence and quality scores.
        If the length of the sequence and quality scores
        do not match, an error is raised.
        ----------
        Input:
            - file (str): Filename for error reporting
            - seq_line (str): Sequence line
            - qual_line (str): Quality scores line
        Raises:
            - InvalidFastaOrFastqError: If an invalid length is found
        """
        if len(seq_line) != len(qual_line):
            logging.error(
                "Sequence and quality scores length mismatch, exiting..."
            )
            raise InvalidFastaOrFastqError(
                f"Sequence and quality scores length mismatch in FASTQ file: {file}"
            )

    def validate_plus_line(self, file: str, plus_line: str):
        """
        Function that validates the '+' line in the FASTQ file.
        The function checks if the line starts with a '+' character.
        If the line does not start with a '+', an error is raised.
        ----------
        Input:
            - file (str): Filename for error reporting
            - plus_line (str): Line to validate
        Raises:
            - InvalidFastaOrFastqError: If the line is invalid
        ----------
        """
        if not plus_line.startswith("+"):
            logging.error("Missing '+' line in FASTQ file, exiting...")
            raise InvalidFastaOrFastqError(
                f"Missing '+' line in FASTQ file: {file}"
            )

    def validate_sequence(self, sequence: str, file: str) -> None:
        """
        Basic validation function for the sequence.
        The function checks if the sequence contains only valid characters.
        If an invalid character is found, the function raises an error.
        ----------
        Input:
            sequence (str): Sequence to validate
            file (str): Filename for error reporting
        Raises:
            InvalidFastaOrFastqError: If the sequence is invalid
        ----------
        """
        sequence = sequence.replace(" ", "")
        if not re.fullmatch(r"[ACTGN]+", sequence, re.IGNORECASE):
            logging.error("Invalid sequence found, exiting...")
            raise InvalidSequenceError(sequence, file)

    def compare_types(self) -> None:
        """
        Compare the types of input files
        This function makes sure the user is not mixing FASTA and FASTQ files
        It basically checks if all files are of the same type.
        ----------
        Input:
            - type: dictionary with the file name and type (FASTA or FASTQ)
        Output:
            - logging.debug: if all files are of the same type
            - logging.error: if the files are not of the same type, sys.exit(1)
        ----------
        """
        logging.debug("Comparing the types of the input files...")
        file_types = set(self.type.values())
        if len(file_types) == 1:
            if "FASTA" in file_types and len(self.type) == 2:
                logging.error("Error while comparing the types. Exiting...")
                raise InvalidSequencingTypesError(self.input_files)
            logging.debug("Input files are of the same type, continuing...")
        else:
            logging.error("Error while comparing the types. Exiting...")
            raise InvalidSequencingTypesError(self.input_files)

    def get_file_type(self) -> str:
        """
        Simple getter function to retrieve the file type in string format
        ----------
        Output:
            - string: file type
        ----------
        """
        logging.debug("Getting the file type...")
        return next(iter(self.type.values()))
