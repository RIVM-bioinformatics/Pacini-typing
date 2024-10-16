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
__data__ = "2024-09-24"
__all__ = ["ArgsValidator"]

import hashlib
import logging
import os
import re
import sys

import yaml


class ArgsValidator:
    """
    Class responsible for validating the input arguments.
    ----------
    Methods:
        - __init__: Constructor for the ArgsValidator class
        - validate_file_extensions: Function that validates the file extensions
        - get_file_extension: Function that retrieves the file extension from a file name
        - get_config_input: Function that retrieves the configuration file
        - check_file_existence: Function that checks if a given file exists and is a file
        - compare_paired_files: Function that checks if the input files are not exactly the same
        - create_sha_hash: Function that creates a SHA256 hash for a given file
        - check_for_same_name: Function that checks if the input files are not exactly the same
        - check_paired_names: Function that checks if the input files are paired
        - validate_filter_arguments: Function that validates the filter arguments
        - run_file_checks: Method runs checks on the input files
        - validate: Main validate function that is used to validate the input files
    ----------
    """

    def __init__(self, option):
        """
        Constructor for the ArgsValidator class.
        The main option dictionary is passed to
        this class and initialized as a class attribute here.
        Additionally, the input file list is stored as a class attribute.
        """
        self.option = option
        self.config = None
        self.config = None
        self.input_file_list = self.option["input_file_list"]

    def validate_file_extensions(self, file):
        """
        Main function that is used to validate the input file extensions.
        Other functions are used to retrieve the configuration file and extract extensions.
        With these information, this function checks if extension is in the accepted list.
        If not, the program will exit with an error message.
        ----------
        Input:
            - file: string with the file path
        Output:
            - True: if the extension is in the accepted list
            - False: if the extension is not in the accepted list
        ----------
        """
        logging.debug("Validating file extension for file: %s...", file)
        self.get_config_input()
        file_name = os.path.basename(file)
        ext = self.get_file_extension(file_name.split(".")).lower()
        if ext in self.config["accepted_input_extensions"]:
            return True
        logging.error("File %s is not accepted", file)
        logging.error(
            "Accepted file extensions are: %s", self.config["accepted_input_extensions"]
        )
        return False

    @staticmethod
    def get_file_extension(file_extension):
        """
        Function that retrieves the file extension from a file name.
        It handles both single and double file extensions.
        For example: file.fastq.gz -> .fastq.gz
        ----------
        Input:
            - file_extension: list with filenames split by (".").
        Output:
            - ext: string with the valid file extension
        ----------
        """
        logging.debug("Retrieving file extension...")
        if not len(file_extension) > 2:
            ext = f".{file_extension[-1]}"
        else:
            ext = f".{file_extension[-2]}.{file_extension[-1]}"
        return ext

    def get_config_input(self):
        """
        Simple function that retrieves the configuration file and loads it into a dictionary.
        The method gets the run path from the input arguments to make sure
        the path is found from external runs.
        See ./configuration/accept_arguments.yaml for the configuration file.
        The config variable is placed in a class attribute.
        """
        logging.debug("Retrieving configuration file...")
        config_path = os.path.join(
            os.path.dirname(self.option["run_path"]),
            "configuration",
            "accept_arguments.yaml",
        )
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

    @staticmethod
    def check_file_existence(file):
        """
        Function that checks if a given file exists and is a file.
        If not exists, the program will exit and the error will be logged.
        ----------
        Input:
            - file: string with the file path
        Output:
            - True: if the file exists
            - False: if the file does not
        ----------
        """
        logging.debug("Checking if file %s exists...", file)
        if os.path.exists(file) and os.path.isfile(file):
            return True
        logging.error("File %s does not exist", file)
        return False

    def compare_paired_files(self):
        """
        Function that checks if the input files are not exactly the same.
        For this operation, a SHA256 hash is created for both files,
        this is done in the create_sha_hash function.
        The hash is then compared, if they are the same,
        the program will exit with an error message.
        """
        logging.debug("Comparing paired input files using hash...")
        if self.create_sha_hash(self.input_file_list[0]) == self.create_sha_hash(
            self.input_file_list[1]
        ):
            logging.error(
                "Input files: %s and %s are the same, exiting...",
                self.input_file_list[0],
                self.input_file_list[1],
            )
            sys.exit(1)
        logging.debug("Input files are not the same, continuing...")

    @staticmethod
    def create_sha_hash(file):
        """
        Method that creates a SHA256 hash for a given file.
        The file is read in chunks of 4096 bytes and the hash is updated.
        The Hash is then returned as a hexadecimal string for comparison.
        ----------
        Input:
            - file: string with the file path
        Output:
            - hash_obj.hexdigest(): string with the SHA256 hash
        ----------
        """
        logging.debug("Creating SHA256 hash for file: %s", file)
        hash_obj = hashlib.sha256()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)

        return hash_obj.hexdigest()

    def check_for_same_name(self):
        """
        Function that checks if the input files are not exactly the same.
        This check is done right before the paired file check.
        Therefore, no big operations are done before this check,
        because the program will exit with an error message.
        """
        logging.debug("Checking if the input file names are not the same...")
        if self.option["input_file_list"][0] == self.option["input_file_list"][1]:
            logging.error("The input filenames are the same, exiting...")
            sys.exit(1)

    def check_paired_names(self):
        """
        Function that checks if the input files are paired.
        This means, 1 and 2 are in the file names, or something similar.
        An error message will be logged and the program will exit if the names are not paired.
        """
        logging.debug("Checking if the paired input contains valid names...")
        pattern1 = re.compile(r".+(_1|R1).+")
        pattern2 = re.compile(r".+(_2|R2).+")
        if not (
            pattern1.search(self.option["input_file_list"][0])
            and pattern2.search(self.option["input_file_list"][1])
        ):
            logging.error(
                "Paired mode requires '_1' and '_2' or "
                "'R1' and 'R2' in the file names, exiting..."
            )
            sys.exit(1)

    def validate_filter_arguments(self):
        """
        Method that validates the filter arguments.
        For example, the identity should be between 0 and 100.
        This method makes sure the program can continue with the correct arguments.
        Errors will be logged and the program will exit.
        """
        logging.debug("Validating filter arguments...")
        if self.option["query"]:
            if (
                self.option["query"]["filters"]["identity"] < 0
                or self.option["query"]["filters"]["identity"] > 100
            ):
                logging.error(
                    "Identity should be between 0 and 100, "
                    "current value: %s, exiting...",
                    self.option["query"]["filters"]["identity"],
                )
                sys.exit(1)

    def run_file_checks(self, file):
        """
        Method runs checks on the input files.
        If these checks pass, the method returns True.
        The following checks are done:
            - Validate the file extensions: check if the extension is in the accepted list
            - Check if the file exists: check if the file exists and is a file
        If not, the program will exit with an error message.
        ----------
        Input:
            - file: string with the file path that needs to be checked
        Output:
            - True: if the checks pass
            - sys.exit(1): if the checks do not pass
        ----------
        """
        logging.debug(
            "Checking file existence and" "valid extension for file: %s...", file
        )
        if self.check_file_existence(file) and self.validate_file_extensions(file):
            return True
        sys.exit(1)

    def validate(self):
        """
        Main validate function that is used to validate the input files.
        It first checks if the input is paired, single or input for creating database.
        The files are then passed to the run_file_checks method.
        ----------
        Output:
            - True: if the files are valid
            - False: if the files are not valid
        ----------
        """
        self.validate_filter_arguments()
        if len(self.input_file_list) == 2:
            if all(self.run_file_checks(file) for file in self.input_file_list):
                self.check_for_same_name()
                self.compare_paired_files()
                self.check_paired_names()
                return True
            return False
        if len(self.input_file_list) == 1:
            return self.run_file_checks(self.input_file_list[0])
        return False
