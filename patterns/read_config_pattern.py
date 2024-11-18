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
__data__ = "2024-10-30"
__all__ = ["ReadConfigPattern"]

from typing import Any

import yaml

from preprocessing.exceptions.parsing_exceptions import (
    YAMLLoadingError,
    YAMLStructureError,
)

REQUIRED_KEYS = ["metadata", "database", "pattern"]
REQUIRED_PATTERN_KEYS = [
    "perc_ident",
    "perc_cov",
    "e_value",
    "p_value",
    "genes",
    "snps",
]


class ReadConfigPattern:
    """
    Class for reading the configuration file containing the pattern
    All necessary information will be extracted from the configuration file
    The options can then be used to run the analysis
    """

    def __init__(self, config_file: str, input_file_type: str) -> None:
        """
        Constructor
        Fill in later...
        """
        self.config_file = config_file
        self.input_file_type = input_file_type
        self.pattern: dict[Any, Any] = {}
        # Create a dictionary to store information
        # This information will be used to:
        # 1. Check database existence
        # 2. Create database if it does not exist
        # 3. Run the query
        self.creation_dict: dict[str, Any] = {}
        # Start the process
        self.read_config()
        self.validate_config_keys()
        self.validate_pattern_keys()
        self.construct_params_dict()

    def read_config(self):
        """
        Read the configuration file
        Fill in later...
        """
        print("Reading configuration file...")
        try:
            with open(self.config_file, "r", encoding="utf-8") as file:
                self.pattern = yaml.safe_load(file)
        except FileNotFoundError as e:
            print("Config file not found, exiting...")
            raise FileNotFoundError(
                f"File {self.config_file} not found"
            ) from e
        except yaml.YAMLError as e:
            print("Error loading YAML file, exiting...")
            raise YAMLLoadingError(self.config_file) from e

    def validate_config_keys(self):
        """
        Validate the configuration file
        Fill in later...
        """
        print("Validating keys of config file...")
        for key in self.pattern:
            if key not in REQUIRED_KEYS:
                raise YAMLStructureError(self.config_file)

    def validate_pattern_keys(self):
        """
        Validate the pattern keys
        Fill in later...
        """
        print("Validating keys of pattern...")
        for key in REQUIRED_PATTERN_KEYS:
            if key not in self.pattern["pattern"]:
                raise YAMLStructureError(self.config_file)

    def construct_params_dict(self):
        """
        Create the database from the configuration
        Fill in later...
        """
        print("Creating database from config file...")
        # Create the database
        # Check if the database exists
        # If it does not exist, create the database
        # If it does exist, do nothing
        self.creation_dict = {
            "database_path": self.pattern["database"]["path"],
            "database_name": self.pattern["database"]["name"],
            "input_fasta_file": self.pattern["database"]["matching_seq_file"],
            "database_type": self.input_file_type.lower(),
            "file_type": self.input_file_type,
        }


if __name__ == "__main__":
    pattern = ReadConfigPattern(
        "/Users/mvandestreek/Developer/pacini_typing/patterns/O139.yaml",
        "fasta",
    )
