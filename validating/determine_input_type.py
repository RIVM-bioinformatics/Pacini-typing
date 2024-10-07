#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

To be filed in later...

Check the input files:
    - What information is needed?
    - What information is available in the header?
    - Is there a quality score line available?
        - Is there a line with a "+"? between the header and the quality score line?
    - Does the header line start with a ">"?
    - Does the header line start with a "@"?
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["FileValidator"]

import logging
import re
import sys


class FileValidator:
    """
    Class that is responsible for validating the input file.
    It takes a file as input and checks if the file is a valid FASTA or FASTQ file.
    The determined file is returned by the class.
    """

    def __init__(self, input_files):
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
        self.body = {}
        self.type = {}
        self.retrieve_body()
        self.determine_file_type()
        if len(self.type) == 2:
            self.compare_types()
        self.get_file_type()

    def determine_file_type(self):
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
        for file in self.input_files:
            if self.check_valid_sequence(file):
                if ((self.body[file][0].startswith(">")
                        and not self.body[file][1].startswith("+"))
                        and not self.body[file][2].startswith("@")):
                    self.type[file] = "FASTA"
                elif ((self.body[file][0].startswith("@")
                       and self.body[file][2].startswith("+")
                       and len(self.body[file][1]) == len(self.body[file][3]))
                      and self.body[file][4].startswith("@")):
                    self.type[file] = "FASTQ"
                else:
                    logging.error("The file is not a valid FASTA or FASTQ file.")
                    sys.exit(1)

    def retrieve_body(self):
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
        for file in self.input_files:
            with open(file, "r", encoding="utf-8") as f:
                self.body[file] = [f.readline().strip() for _ in range(5)]
        # TODO: Think about checking the whole file for valid sequences and not just the first 5 lines
        #   if so, maybe combine it with hash function in validating input arguments script
        #   to not read the whole file twice

    def check_valid_sequence(self, file):
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
        if re.fullmatch(r"[ACTG]+", self.body[file][1]):
            return True
        logging.error("%s is not a valid FASTA or FASTQ file, "
                      "the sequence is not valid.", file)
        sys.exit(1)

    def compare_types(self):
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
        file_types = set(self.type.values())
        if len(file_types) == 1:
            if "FASTA" in file_types and len(self.type) == 2:
                logging.error("Two input FASTA files are not allowed. Exiting...")
                sys.exit(1)
            logging.debug("All files are valid and the same type, continuing...")
        else:
            logging.error("The input files are not of the same type: %s Exiting...", self.type)
            sys.exit(1)

    def get_file_type(self):
        """
        Simple getter function to retrieve the file type in string format
        ----------
        Output:
            - string: with the file type
        ----------
        """
        return next(iter(self.type.values()))
