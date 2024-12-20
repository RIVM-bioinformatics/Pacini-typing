#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Module responsible for validating the input arguments.
The main goal of this module is to provide (basic) validation
for the input files.
See class ArgsValidator for more information about specific validation methods.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-09-24"
__all__ = ["ArgsValidator"]

import hashlib
import logging
import os
import re
from typing import Any

import yaml

from preprocessing.exceptions.validation_exceptions import (
    FileNotExistsError,
    InvalidFileExtensionError,
    InvalidPairedError,
    ValidationError,
)


class ArgsValidator:
    """
    Class responsible for validation the input arguments.
    ----------
    Methods:
        - __init__: Constructor for the ArgsValidator class
        - validate_file_extensions: Function that validates the file extensions
        - get_file_extension: Function that retrieves the file extension from a file name
        - get_config_input: Function that retrieves the config file
        - check_file_existence: Function that checks if a given file exists and is a file
        - compare_paired_files: Function that checks if the input files are not exactly the same
        - create_sha_hash: Function that creates a SHA256 hash for a given file
        - check_for_same_name: Function that checks if the input file names are not the same
        - check_paired_names: Function that checks if the input files are paired
        - validate_filter_arguments: Function that validates the filter arguments
        - run_file_checks: Method runs checks on the input files
        - validate: Main validate function that is used to validate the input files
    ----------
    """

    def __init__(self, option: dict[str, Any]) -> None:
        """
        Constructor for the ArgsValidator class.
        The main option dictionary is passed to
        this class and initialized as a class attribute here.
        Additionally, the input file list is stored as a class attribute.
        """
        self.option = option
        self.config = None
        self.config = None
        self.get_config_input()
        self.input_file_list: list[str] = self.option["input_file_list"]

    def validate_file_extensions(self, file: str) -> bool:
        """
        Main function that is used to validate the input file extensions.
        Other functions are used to retrieve the config file and extract extensions.
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
        logging.debug("Validating file extension for file: %s", file)
        file_name = os.path.basename(file)
        ext = self.get_file_extension(file_name.split(".")).lower()
        assert self.config is not None
        if ext in self.config["accepted_input_extensions"]:
            return True
        logging.error("Error in vile extension, Exiting...")
        raise InvalidFileExtensionError(
            file, self.config["accepted_input_extensions"]
        )

    @staticmethod
    def get_file_extension(file_extension: list[str]) -> str:
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
        if len(file_extension) <= 2:
            ext = f".{file_extension[-1]}"
        else:
            ext = f".{file_extension[-2]}.{file_extension[-1]}"
        return ext

    def get_config_input(self) -> None:
        """
        Simple function that retrieves the config file and loads it into a dictionary.
        The method gets the run path from the input arguments to make sure
        the path is found from external runs.
        See ./config/accept_arguments.yaml for the config file.
        The config variable is placed in a class attribute.
        """
        logging.debug("Retrieving config file...")
        config_path = os.path.join(
            os.path.dirname(self.option["run_path"]),
            "config",
            "accept_arguments.yaml",
        )
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

    @staticmethod
    def check_file_existence(file: str) -> bool:
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
        logging.debug("Checking if file %s exists", file)
        if os.path.exists(file) and os.path.isfile(file):
            return True
        logging.error("File not found, exiting...")
        raise FileNotExistsError(file)

    def compare_paired_files(self) -> None:
        """
        Function that checks if the input files are not exactly the same.
        For this operation, a SHA256 hash is created for both files,
        this is done in the create_sha_hash function.
        The hash is then compared, if they are the same,
        the program will exit with an error message.
        """
        logging.debug("Comparing paired input files using a hash...")
        if self.create_sha_hash(
            self.input_file_list[0]
        ) == self.create_sha_hash(self.input_file_list[1]):
            logging.error("Paired content is the same, exiting...")
            raise InvalidPairedError(
                self.input_file_list[0], self.input_file_list[1]
            )
        logging.debug("Files Hashes are not identical, continuing...")

    @staticmethod
    def create_sha_hash(file: str) -> str:
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

    def check_for_same_name(self) -> None:
        """
        Function that checks if the input files are not exactly the same.
        This check is done right before the paired file check.
        Therefore, no big operations are done before this check,
        because the program will exit with an error message.
        """
        logging.debug("Paired files supplied, checking similarity...")
        if (
            self.option["input_file_list"][0]
            == self.option["input_file_list"][1]
        ):
            logging.error("Error in validating paired names, exiting...")
            raise InvalidPairedError(
                self.option["input_file_list"][0],
                self.option["input_file_list"][1],
            )

    def check_paired_names(self) -> None:
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
            logging.error("Error in validating paired names, exiting...")
            raise InvalidPairedError(
                self.option["input_file_list"][0],
                self.option["input_file_list"][1],
            )

    def run_file_checks(self, file: str) -> bool:
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
            "Checking file existence and valid extension for file: %s", file
        )
        if self.check_file_existence(file) and self.validate_file_extensions(
            file
        ):
            return True
        raise ValidationError()

    def validate(self) -> bool:
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
        if len(self.input_file_list) == 2:
            if len(self.input_file_list) == 2 and all(
                self.run_file_checks(file) for file in self.input_file_list
            ):
                self.check_for_same_name()
                self.compare_paired_files()
                self.check_paired_names()
                return True
            return False
        if len(self.input_file_list) == 1:
            return self.run_file_checks(self.input_file_list[0])
        return False
