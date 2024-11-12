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
        - retrieve_body: Method that retrieves the body of the input file
        - check_valid_sequence: Method that checks if the sequence is valid
        - compare_types: Method that compares the types of input files
        - get_file_type: Method that returns the file type
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
        self.retrieve_body()
        self.determine_file_type()
        if len(self.type) == 2:
            self.compare_types()

    def determine_file_type(self) -> None:
        """
        Main logic function of the class that does the checking.
        With the body of the file, the function determines if the file is a FASTA or FASTQ file.
        The function first checks if the sequence is valid,
        then it checks the header and quality score line.
        If the file is valid, the type is determined and stored in the type dictionary.
        Example:
            - {
            file1: "FASTA",
            file2: "FASTQ"
            }
        ----------
        Input:
            - self.input_files: list with the input files
            - self.body: dictionary with the file name and the first 5 lines
        Output:
            - self.type: dictionary with the file name and the type (FASTA or FASTQ)
        ----------
        """
        logging.debug("Determining the file type of the input files...")
        for file in self.input_files:
            if self.check_valid_sequence(file):
                if (
                    self.body[file][0].startswith(">")
                    and not self.body[file][1].startswith("+")
                ) and not self.body[file][2].startswith("@"):
                    self.type[file] = "FASTA"
                elif (
                    self.body[file][0].startswith("@")
                    and self.body[file][2].startswith("+")
                    and len(self.body[file][1]) == len(self.body[file][3])
                ) and self.body[file][4].startswith("@"):
                    self.type[file] = "FASTQ"
                else:
                    logging.error("Invalid FASTA or FASTQ file provided. Exiting...")
                    raise InvalidFastaOrFastqError(file)

    def retrieve_body(self) -> None:
        """
        Method that retrieves the body of the input file.
        The first 5 lines of the file are retrieved and stored in a dictionary.
        The dictionary has the file name as key and the first 5 lines as values.
        Example:
            - {
            file1: [line1, line2, line3, line4, line5],
            file2: [line1, line2, line3, line4, line5]
            }
        ----------
        Input:
            - self.input_files: list with the input files
        Output:
            - self.body: dictionary with the file name and the first 5 lines
        ----------
        """
        logging.debug("Retrieving the body of the input files...")
        for file in self.input_files:
            with open(file, "r", encoding="utf-8") as f:
                self.body[file] = [f.readline().strip() for _ in range(5)]
                # self.body[file] = [line.strip() for line in f.readlines()]

    def check_valid_sequence(self, file: str) -> bool:
        """
        Simple method to check if the sequence is valid.
        It simply checks if the sequence is a valid DNA sequence,
        i.e., only contains A, C, T, or G. With the input name,
        the right sequence is retrieved from the body dictionary.
        ----------
        Input:
            - file: string with the file name
        Output:
            - True: if the sequence is valid
            - False: if the sequence is not valid
        ----------
        """
        logging.debug("Checking if the sequence is valid...")
        if re.fullmatch(r"[ACTGN]+", self.body[file][1]):
            return True
        logging.error("Invalid sequence provided. Exiting...")
        raise InvalidSequenceError(self.body[file][1], file)

        # TODO: Thinks about reading in batches of 4 lines?

        # TODO: Is it necessary to check the entire file?
        #  It's probably better, but how to efficiently do it?
        # for index, lines in enumerate(self.body[file]):
        #     line = lines.strip()
        #     if line and index % 4 == 1:
        #         if not re.fullmatch(r"[ACTG]+", line):
        #             logging.error("The sequence is not valid.")
        #             sys.exit(1)

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
            logging.debug("All files are valid and the same type, continuing...")
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
