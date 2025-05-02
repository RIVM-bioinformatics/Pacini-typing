#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Module for reading a configuration file containing
a genetic pattern to be used for the analysis.
The configuration file is a YAML file containing
certain keys that are required for the analysis.

The ReadConfigPattern class reads the configuration file,
validates the keys, and constructs a dictionary with
parameters required for the database creation and the query operation.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-11-08"
__all__ = ["ReadConfigPattern"]

import logging
import shutil
from typing import Any

import yaml

from preprocessing.exceptions.parsing_exceptions import (
    YAMLLoadingError,
    YAMLStructureError,
)
from preprocessing.exceptions.snp_detection_exceptions import PathError

REQUIRED_KEYS = ["metadata", "database", "pattern"]
REQUIRED_PATTERN_KEYS = [
    "perc_ident",
    "perc_cov",
    "genes",
]


class ReadConfigPattern:
    """
    Class for reading the configuration file containing the pattern
    All necessary information will be extracted from the configuration file
    The options can then be used to run the analysis
    ----------
    Methods:
        - __init__: Constructor for the ReadConfigPattern class
        - read_config: Read the configuration file
        - validate_config_keys: Validate the configuration file
        - validate_pattern_keys: Validate the pattern keys
        - construct_params_dict: Create the database from the configuration
    ----------
    """

    def __init__(
        self,
        config_file: str,
        input_file_type: str,
        enable_snp_search: bool = False,
    ) -> None:
        """
        Constructor for the ReadConfigPattern class
        It accepts the configuration file and the input file type
        The pattern variable is initialized as an empty dictionary
        the pattern is placed in this pattern variable.
        The creation_dict is used for database operations and
        running the query, so that not the entire pattern will be passed around
        ----------
        Input:
            - config_file: str
            - input_file_type: str
        ----------
        """
        self.config_file = config_file
        self.input_file_type = input_file_type.upper()
        self.pattern: dict[Any, Any] = {}
        self.creation_dict: dict[str, Any] = {}
        self.enable_snp_search: bool = enable_snp_search
        # Start the process
        self.read_config()
        self.validate_config_keys()
        self.validate_pattern_keys()
        self.construct_params_dict()
        self.construct_params_dict()
        if self.enable_snp_search:
            self.handle_snp_pattern()

    def read_config(self) -> None:
        """
        Function that reads the configuration file
        If the config file is not found, an error is raised.
        If the config file is wrong constructed,
        a custom error is raised. (YAMLStructureError)
        If the config file is loaded correctly,
        the pattern is stored in the pattern variable
        ----------
        Raises:
            - FileNotFoundError: If the config file is not found
            - YAMLLoadingError: If the config file is not loaded correctly
        ----------
        """
        logging.info("Reading configuration file...")
        try:
            with open(self.config_file, "r", encoding="utf-8") as file:
                self.pattern = yaml.safe_load(file)
        except FileNotFoundError as e:
            logging.error("Config file not found, exiting...")
            raise FileNotFoundError(
                f"File {self.config_file} not found"
            ) from e
        except yaml.YAMLError as e:
            logging.error("Error loading YAML file, exiting...")
            raise YAMLLoadingError(self.config_file) from e

    def validate_config_keys(self) -> None:
        """
        Function that validates the keys of the configuration file
        If the keys are not present, a custom error is raised.
        The keys that are required are stored in the REQUIRED_KEYS variable.
        These keys are the main keys of the configuration file.
        Additional keys are not mandatory, but the main keys are required.
        ----------
        Raises:
            - YAMLStructureError: If the keys are not present
        ----------
        """
        logging.debug("Validating keys of config file...")
        missing_keys = [
            key for key in REQUIRED_KEYS if key not in self.pattern
        ]
        if missing_keys:
            raise YAMLStructureError(
                f"The following required keys are missing in {self.config_file}: {missing_keys}"
            )

    def validate_pattern_keys(self) -> None:
        """
        This function checks the specific keys that
        are required for the genetic pattern to be valid.
        If the keys are not present, a custom error is raised.
        The keys that are required are stored
        in the REQUIRED_PATTERN_KEYS variable
        ----------
        Raises:
            - YAMLStructureError: If the keys are not present
        ----------
        """
        logging.debug("Validating keys of genetic pattern...")
        for key in REQUIRED_PATTERN_KEYS:
            if key not in self.pattern["pattern"]:
                raise YAMLStructureError(self.config_file)

    def construct_params_dict(self) -> None:
        """
        Constructs a dictionary with parameters required for
        the database creation and the query operation.
        """
        logging.debug("Creating database from config file...")
        self.creation_dict = {
            "database_path": self.pattern["database"]["path"],
            "database_name": self.pattern["database"]["name"],
            "input_fasta_file": self.pattern["database"]["target_genes_file"],
            "database_type": self.input_file_type,
            "file_type": self.input_file_type,
        }

    def handle_snp_pattern(self) -> None:
        """
        TODO: Fill in later...
        - validate SNP pattern
        - prepare SNP pattern
        - add SNP pattern to creation_dict
            self.craetion_dict["my_variable"] =
                self.pattern["pattern"]["my_variable"]

        - Add the execution path to the creation_dict (self.get_method_path())
        """
        pass

    def get_method_path(self) -> str:
        """
        Returns the path to either the kma or blastn executable,
        based on the input files type. This path is required to
        be passed to PointFinder.
        ----------
        Output:
            - str: Path to the executable
        ----------
        """
        path: str | None = shutil.which(
            "blastn" if self.input_file_type == "FASTA" else "kma"
        )
        if path:
            return path
        raise PathError
