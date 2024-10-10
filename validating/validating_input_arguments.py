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
__all__ = ["validate_file_extensions", "get_file_extension", "get_config_input",
           "check_file_existence", "compare_paired_files", "create_sha_hash",
           "check_for_same_name", "check_paired_names", "run_file_checks", "main"]

import re
import sys
import os
import hashlib
import logging
import yaml


def validate_file_extensions(file):
    """
    Main function that is used to validate the input file extensions.
    Other functions are used to retrieve the configuration file and extract extensions.
    With these information, this function checks if extension is in the accepted list.
    If not, the program will exit with an error message.
    ----------
    Input:
        - args: parsed object with the arguments
    ----------
    """
    config = get_config_input()
    ext = get_file_extension(file.split(".")).lower()
    if ext in config["accepted_input_extensions"]:
        logging.debug("File %s is accepted", file)
        return True
    logging.error("File %s is not accepted", file)
    logging.error("Accepted file extensions are: %s", config['accepted_input_extensions'])
    return False


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
    if not len(file_extension) > 2:
        ext = f".{file_extension[-1]}"
    else:
        ext = f".{file_extension[-2]}.{file_extension[-1]}"
    return ext


def get_config_input():
    """
    Simple function that retrieves the configuration file and loads it into a dictionary.
    This dictionary is then returned and used for the input validation.
    See ./configuration/accept_arguments.yaml for the configuration file.
    ----------
    Output:
        - config: dictionary with the configuration file
    ----------
    """
    # FIXME - remove relative path, os.path.dirname(os.path.abspath(__file__))
    with open("configuration/accept_arguments.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config


def check_file_existence(file):
    """
    Function that checks if a given file exists and is a file.
    ----------
    Input:
        - file: string with the file path
    ----------
    """
    if os.path.exists(file) and os.path.isfile(file):
        logging.debug("File %s exists", file)
        return True
    logging.error("File %s does not exist", file)
    return False


def compare_paired_files(input_file_list):
    """
    Function that checks if the input files are not exactly the same.
    For this operation, a SHA256 hash is created for both files,
    this is done in the create_sha_hash function.
    The hash is then compared, if they are the same,
    the program will exit with an error message.
    ----------
    Input:
        - args: parsed object with the arguments
    ----------
    """
    logging.debug("Comparing paired input files using SHA256 hash...")
    if create_sha_hash(input_file_list[0]) == create_sha_hash(input_file_list[1]):
        logging.error("Input files: %s and %s are the same, exiting...",
                      input_file_list[0], input_file_list[1])
        sys.exit(1)
    logging.debug("Input files are not the same, continuing...")


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


def check_for_same_name(input_file_list):
    """
    Function that checks if the input files are not exactly the same.
    This check is done right before the paired file check.
    Therefore, no big operations are done before this check,
    because the program will exit with an error message.
    ---------
    Input:
        - args: parsed object with the arguments
    ----------
    """
    if input_file_list[0] == input_file_list[1]:
        logging.error("The input filenames are the same, exiting...")
        sys.exit(1)


def check_paired_names(input_file_list):
    """
    Function that checks if the input files are paired.
    This means, 1 and 2 are in the file names, or something similar.
    ---------
    Input:
        - args: parsed object with the arguments
    ----------
    """
    pattern1 = re.compile(r".+(_1|R1).+")
    pattern2 = re.compile(r".+(_2|R2).+")
    if not (pattern1.search(input_file_list[0]) and pattern2.search(input_file_list[1])):
        logging.error("Paired mode requires '_1' and '_2' or "
                      "'R1' and 'R2' in the file names, exiting...")
        sys.exit(1)


def run_file_checks(file):
    """
    Method that walks through the input files and checks if they are valid.
    The following checks are done:
        - Validate the file extensions
        - Check if the file exists
    If not, the program will exit with an error message.
    ----------
    Input:
        - args: list with the input files,
        in paired mode this is a list with two files,
        in single mode it is a single file
    ----------
    """
    if file:
        if check_file_existence(file) and validate_file_extensions(file):
            return True
        sys.exit(1)
    return False


def main(input_files):
    """
    Main function that is used to validate the input files.
    Paired mode holds two files, therefore extra checks are required.
    Most errors will exit the program with an error message.
    ----------
    Input:
        - input_files: list with the input files
    Output:
        - True: if the files are valid
        - False: if the files are not valid
    ----------
    """
    if len(input_files) == 2:
        if all(run_file_checks(file) for file in input_files):
            check_for_same_name(input_files)
            compare_paired_files(input_files)
            check_paired_names(input_files)
            return True
        return False
    if len(input_files) == 1:
        return run_file_checks(input_files[0])
    return False
