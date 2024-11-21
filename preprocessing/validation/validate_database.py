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

__author__ = "Mark Van de Streek"
__date__ = "2024-09-24"
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
        - database_name: string with the database name
        - input_file_type: string with the input file type
    ----------
    """
    logging.debug("Checking if the database exists.")
    db_files = create_database_file_list(arg_options)
    for db_file in db_files:
        if not os.path.exists(arg_options["database_path"] + db_file):
            logging.error("Database does not exist")
            return False
    return True


def create_database_file_list(arg_options: dict[str, Any]) -> list[str]:
    """
    Function that creates a list of database files based on the input file type.
    ----------
    Input:
        - database_name: string with the database name
        - input_file_type: string with the input file type
    ----------
    """
    logging.debug(
        "Creating a list of database files based on the input file type."
    )
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
    Function that checks if the database path exists.
    If not, the program will exit with an error message.
    ----------
    Input:
        - input_path: string with the database path
    ----------
    """
    if not arg_options["database_path"].endswith("/"):
        logging.warning(
            "The database path does not end with a forward slash. "
            "Appending it to run checks."
        )
        arg_options["database_path"] += "/"
    if not os.path.exists(arg_options["database_path"]):
        logging.error("Database does not exist")
        return False
    return check_for_database_existence(arg_options)
