#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

To be filed in later...
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["check_for_database_path"]

import sys
import os
import logging


def check_for_database_existence(database_path, database_name, input_file_type):
    """
    Function that checks if the database exists.
    Based on the input type, the method will check if the files exist:
    for option fasta/blast: db_name.ndb, db_name.nhr, db_name.nin, db_name.njs, db_name.not, db_name.nsq, db_name.ntf, db_name.nto

    for option fastq/kma: db_name.comp.b, db_name.length.b, db_name.name, db_name.seq.b
    ----------
    Input:
        - database_name: string with the database name
        - input_file_type: string with the input file type
    ----------
    """
    db_files = create_database_file_list(database_name, input_file_type)
    for db_file in db_files:
        if not os.path.exists(database_path + db_file):
            logging.error(
                "The database file %s does not exist. "
                "Please provide a valid database name or path.", db_file)
            sys.exit(1)
        return True


def create_database_file_list(database_name, input_file_type):
    """
    Function that creates a list of database files based on the input file type.
    ----------
    Input:
        - database_name: string with the database name
        - input_file_type: string with the input file type
    ----------
    """
    db_files = []
    if input_file_type == "FASTA":
        db_files = [f"{database_name}.{ext}" for ext in
                    ["ndb", "nhr", "nin", "njs", "not", "nsq", "ntf", "nto"]]
    elif input_file_type == "FASTQ":
        db_files = [f"{database_name}.{ext}" for ext in
                    ["comp.b", "length.b", "name", "seq.b"]]

    return db_files


def check_for_database_path(args, file_type):
    """
    Function that checks if the database path exists.
    If not, the program will exit with an error message.
    ----------
    Input:
        - input_path: string with the database path
    ----------
    """
    if not args.database_path.endswith("/"):
        logging.warning(
            "The database path does not end with a forward slash. "
            "Appending it to run checks.")
        args.database_path += "/"
    if not os.path.exists(args.database_path):
        logging.error(
            "The database path does not exist. "
            "Please provide a valid path, "
            "make sure the path is correct and ending with a forward slash. /")
        sys.exit(1)
    logging.info(
        "The database path exists. "
        "Checking if the database name is provided...")
    return check_for_database_existence(
        args.database_path, args.database_name, file_type)