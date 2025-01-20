#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Module that validates the existence of the database.
Based on the input type, the methods will check if the specific files exist.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-10-04"
__all__ = [
    "check_for_database_existence",
    "create_database_file_list",
    "check_for_database_path",
]

import logging
import os
from typing import Any


def check_for_database_existence(arg_options: dict[str, Any]) -> bool:
    """
    Function that checks if the database exists.
    Based on the input type, the method will check if the files exist:
    for option fasta/blast:
        db_name.ndb, db_name.nhr, db_name.nin,
        db_name.njs, db_name.not, db_name.nsq, db_name.ntf, db_name.nto
    for option fastq/kma:
        db_name.comp.b, db_name.length.b, db_name.name, db_name.seq.b
    ----------
    Input:
        - arg_options: dictionary with the input arguments
    Output:
        - True if all files exist, False otherwise
    ----------
    """
    db_files = create_database_file_list(arg_options)
    logging.debug("Checking if all required database files are present...")
    for db_file in db_files:
        if not os.path.exists(arg_options["database_path"] + db_file):
            logging.warning(
                "Database does not exist, "
                "the program will try to create it or exit..."
            )
            return False
    return True


def create_database_file_list(arg_options: dict[str, Any]) -> list[str]:
    """
    Function that creates a list of database files based on the input file type.
    The list will contain the required files for the database.
    ----------
    Input:
        - arg_options: dictionary with the input arguments
    Output:
        - list of required database files
    ----------
    """
    logging.debug("Creating list of required database files...")
    db_files = []
    if arg_options["file_type"] == "FASTA":
        db_files = [
            f"{arg_options["database_name"]}.{ext}"
            for ext in ["ndb", "nhr", "nin", "njs", "not", "nsq", "ntf", "nto"]
        ]
    elif arg_options["file_type"] == "FASTQ":
        db_files = [
            f"{arg_options["database_name"]}.{ext}"
            for ext in ["comp.b", "length.b", "name", "seq.b"]
        ]

    return db_files


def check_for_database_path(arg_options: dict[str, Any]) -> bool:
    """
    Main check function that validates the database path.
    The method will check if the database path exists.
    If the path does not exist, the method will return False to
    the main pacini_typing script.
    ----------
    Input:
        - arg_options: dictionary with the input arguments
    Output:
        - True if the database path exists, False otherwise
    ----------
    """
    if not arg_options["database_path"].endswith("/"):
        logging.warning(
            "The database path does not end with a forward slash. "
            "Appending it to run checks."
        )
        arg_options["database_path"] += "/"
    if not os.path.exists(arg_options["database_path"]):
        logging.warning(
            "Database does not exist, "
            "the program will try to create it or exit..."
        )
        return False
    return check_for_database_existence(arg_options)
