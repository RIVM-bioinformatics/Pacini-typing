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
__all__ = ["validate_file_extensions"]

import sys
import os
import hashlib
import logging
import yaml


def validate_file_extensions(file):
    """
    Main function that is used to validate the input file extensions.
    ----------
    Input:
        - args: parsed object with the arguments
    ----------
    """
    config = get_config_input()
    ext = get_file_extension(file.split("."))
    ext = ext.lower()
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
    ----------
    Output:
        - config: dictionary with the configuration file
    ----------
    """
    with open("configuration/accept_arguments.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config


def check_file_existence(file):
    """
    Function that checks if the input file exists and is a file.
    ----------
    Input:
        - file: string with the file path
    ----------
    """
    if os.path.isfile(file) and os.path.exists(file):
        logging.debug("File %s exists", file)
        return True
    logging.error("File %s does not exist", file)
    return False


def compare_paired_files(args):
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
    logging.info("Comparing paired input files using SHA256 hash...")
    if create_sha_hash(args.paired[0]) == create_sha_hash(args.paired[1]):
        logging.error("Input files: %s and %s are the same, exiting...",
                      args.paired[0], args.paired[1])
        sys.exit(1)
    else:
        logging.debug("Input files are not the same, continuing...")


def create_sha_hash(file):
    """
    Method that creates a SHA256 hash for a given file.
    The file is read in chunks of 4096 bytes and the hash is updated.
    The Hash is then returned as a hexadecimal string.
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


def check_for_same_name(args):
    """
    Function that checks if the input files are not exactly the same.
    If so, the program will exit with an error message.
    ---------
    Input:
        - args: parsed object with the arguments
    ----------
    """
    if args.paired[0] == args.paired[1]:
        logging.error("The input filenames are the same, exiting...")
        sys.exit(1)


def run_file_checks(args):
    """
    Method that walks through the input files and checks if they are valid.
    If not, the program will exit with an error message.
    ----------
    Input:
        - args: list with the input files,
        in paired mode this is a list with two files,
        in single mode it is a single file
    ----------
    """
    if args:
        if check_file_existence(args) and validate_file_extensions(args):
            return True
        sys.exit(1)
    return False


def main(args):
    """
    Main function that is used to validate the input file extensions.
    Paired mode holds two files, therefore an extra sameness check is needed.
    For input and single mode, these arguments hold a single file.
    Therefore, it's send as a list.
    ----------
    Input:
        - args: parsed object with the arguments
    ----------
    """
    if hasattr(args, "paired") and args.paired:
        # First run both files through the checks,
        # if they pass, check if they are not the same
        if all(run_file_checks(file) for file in args.paired):
            # First check for same name to prevent unnecessary I/O
            check_for_same_name(args)
            compare_paired_files(args)
            return True
        return False

    if hasattr(args, "single") and args.single:
        return run_file_checks(args.single)

    if hasattr(args, "input") and args.input:
        return run_file_checks(args.input)

    return False
