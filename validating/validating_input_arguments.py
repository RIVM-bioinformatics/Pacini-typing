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
import subprocess
import logging
import yaml


def validate_file_extensions(args):
    """
    Main function that is used to validate the input file extensions.
    ----------
    Input:
        - args: parsed object with the arguments
    ----------
    """
    # TODO: There should be a boolean flag to check single or paired
    #  Based on that, the function should call the check_file_extension function
    config = get_config_input()
    if args.paired:
        for file in args.paired:
            ext = get_file_extension(file.split("."))
            if ext in config["accepted_input_extensions"]:
                logging.debug(f"File {file} is accepted")
            else:
                logging.error(f"File {file} is not accepted")
                logging.error(f"Accepted file extensions are: {config['accepted_input_extensions']}")
                sys.exit(1)
    elif args.single:
        ext = get_file_extension(args.single[0].split("."))
        if ext in config["accepted_input_extensions"]:
            logging.debug(f"File {args.single[0]} is accepted")
        else:
            logging.error(f"File {args.single[0]} is not accepted")
            logging.error(f"Accepted file extensions are: {config['accepted_input_extensions']}")
            sys.exit(1)


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
    with open("configuration/accept_arguments.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


def check_existence_paired_or_single(args):
    """
    Function that checks if the arguments are either paired or single.
    Based on the input, the function will call the check_file_existence function.
    ----------
    Input:
        - args: parsed object with the arguments, either single or paired
    ----------
    """
    # TODO: This function could be combined with other functions based on booleans
    if args.paired:
        for file in args.paired:
            check_file_existence(file)
    elif args.single:
        check_file_existence(args.single)


def check_file_existence(file):
    """
    Function that checks if the input file exists and is a file.
    ----------
    Input:
        - file: string with the file path
    ----------
    """
    file = file[0]
    if not os.path.isfile(file) and not os.path.exists(file):
        logging.error(f"File {file} does not exist")
        sys.exit(1)
    else:
        logging.debug(f"File {file} exists")


def main(args):
    """
    Main function that is used to validate the input file extensions.
    ----------
    ...
    ----------
    """
    validate_file_extensions(args)
    check_existence_paired_or_single(args)
