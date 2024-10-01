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


def check_double_files(args):
    """
    Function that checks if the input files are not exactly the same.
    The first 150 lines of both files are compared.
    ----------
    Input:
        - args: parsed object with the arguments
    ----------
    """
    file1, file2 = args.paired[0], args.paired[1]

    try:
        with (open(file1, 'r', encoding="utf-8") as f1,
              open(file2, 'r', encoding="utf-8") as f2):
            for _ in range(150):
                line1 = f1.readline()
                line2 = f2.readline()
                if line1 != line2:
                    logging.debug("Files are different.")
                    return
        logging.error("The input files are the same, exiting...")
        sys.exit(1)
    except OSError as e:
        logging.error("An error occurred while comparing files: %s", e)
        sys.exit(1)


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
        for file in args:
            if check_file_existence(file) and validate_file_extensions(file):
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
        check_double_files(args)
        check_for_same_name(args)
        return run_file_checks(args.paired)

    if hasattr(args, "single") and args.single:
        return run_file_checks([args.single])

    if hasattr(args, "input") and args.input:
        return run_file_checks([args.input])

    return False
