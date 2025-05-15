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
import os
import shutil
from typing import Any

import yaml

from preprocessing.exceptions.parsing_exceptions import (
    YAMLLoadingError,
    YAMLStructureError,
)
from preprocessing.exceptions.snp_detection_exceptions import (
    IncorrectSNPConfiguration,
    PathError,
    PointFinderScriptError,
)

REQUIRED_KEYS = ["metadata", "database", "global_settings", "pattern"]
RQUIRED_GLOBAL_SETTINGS_KEYS = [
    "perc_ident",
    "perc_cov",
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
        search_mode: str,
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
        self.search_mode: str = search_mode
        # Start the process
        self.read_config()
        self.validate_config_keys()
        self.validate_global_settings()
        self.validate_pattern_keys()
        self.construct_params_dict()
        self.construct_params_dict()
        if self.search_mode in {"SNPs", "both"}:
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

    def validate_global_settings(self) -> None:
        """
        Function that validates the global settings of the configuration file
        If the keys are not present, a custom error is raised.
        The keys that are required are stored in the
        RQUIRED_GLOBAL_SETTINGS_KEYS variable.
        ----------
        Raises:
            - YAMLStructureError: If the keys are not present
        ----------
        """
        logging.debug("Validating global settings of config file...")
        for key in RQUIRED_GLOBAL_SETTINGS_KEYS:
            if key not in self.pattern["global_settings"]:
                logging.error(
                    "Missing key %s in global settings, exiting...", key
                )
                raise YAMLStructureError(self.config_file)
            if "SNP_output_dir" not in self.pattern[
                "global_settings"
            ] and self.search_mode in {"SNPs", "both"}:
                logging.error(
                    "Missing key SNP_output_dir in global settings, exiting..."
                )
                raise YAMLStructureError(self.config_file)
            if "run_output" not in self.pattern[
                "global_settings"
            ] and self.search_mode in {"genes", "both"}:
                logging.error(
                    "Missing key run_output in global settings, exiting..."
                )
                raise YAMLStructureError(self.config_file)

    def _validate_first_pattern_keys(
        self, entry: dict[str, str | int]
    ) -> None:
        """
        Function that validates the first key of the pattern,
        which should be either "gene" or "SNP".
        If the first key is not one of these, a custom error is raised.
        ----------
        Input:
            - entry: dict[str, str | int]
                The entry of the pattern to be validated
        Raises:
            - YAMLStructureError: If the first key is not valid
        ----------
        """
        first_key: str = next(iter(entry))
        if not (first_key == "gene" or first_key == "SNP"):
            logging.error(
                "Found invalid first key in pattern"
                " (only gene or SNP allowed), exiting..."
            )
            raise YAMLStructureError(self.config_file)

    def validate_pattern_keys(self) -> None:
        """
        This function checks the specific keys that
        are required for the genetic pattern to be valid.
        If the constriuction is not valid, a custom error is raised.
        ----------
        Raises:
            - YAMLStructureError: If the keys are not present
        ----------
        """
        logging.debug("Validating keys of genetic pattern...")
        for entry in self.pattern["pattern"]:
            self._validate_first_pattern_keys(entry)

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
        Function that handles to adding of SNP-related parameters
        to the creation_dict. This is done by calling other functions
        that will return the required parameters.
        These getter functions also validate the variables.
        """
        self.creation_dict["SNP_database_path"] = self.pattern["database"][
            "SNP_database_path"
        ]
        self.creation_dict["species"] = self.pattern["database"]["species"]
        self.creation_dict["method"] = (
            "blastn" if self.input_file_type == "FASTA" else "kma"
        )
        self.creation_dict["method_path"] = self.get_method_path()
        self.creation_dict["SNP_output_dir"] = self.get_output_dir()
        self.creation_dict["PointFinder_script_path"] = (
            self.get_pointfinder_script_path()
        )
        self.creation_dict["SNP_list"] = self.get_snp_list()
        self.creation_dict["pointfinder_genes_file"] = (
            self.get_pointfinder_genes_file()
        )

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

    def get_output_dir(self) -> str:
        """
        Checks if the output directory exists,
        if not, it creates the directory.
        If the directory already exists, it returns the path to the directory.
        ----------
        Output:
            - str: Path to the output directory
        ----------
        """
        path: str = self.pattern["global_settings"]["SNP_output_dir"]
        path = path if path.endswith("/") else path + "/"
        if os.path.exists(path) and os.path.isdir(path):
            return path
        else:
            os.makedirs(path, exist_ok=True)
            return path

    def get_pointfinder_script_path(self) -> str:
        """
        Function that returns the path to the PointFinder script,
        if valid. If not valid, an error is raised.
        The path is not checked for existence, that is done right
        before usage.
        ----------
        Output:
            - str: Path to the PointFinder script
        ----------
        """
        path: str = self.pattern["metadata"]["PointFinder_script_path"]
        if path.endswith("PointFinder.py"):
            return path
        else:
            logging.error(
                "The PointFinder script is incorrectly specified or "
                "missing in the config file, exiting..."
            )
            raise PointFinderScriptError(path)

    def validate_SNP_list(self, snp_list: list[dict[str, str | int]]) -> bool:
        """
        Function that validates the incoming SNP list. The list should be like:
            SNPs = [
            {
            "SNP": "gyrA",
            "ref": "ATG",
            "alt": "L",
            "pos": 1
            },
            {
            "SNP": "gyrA",
            "ref": "CCC",
            "alt": "F",
            "pos": 2
            },
        ]
        The delegates the validation of every single entry to the
        _validate_snp_entry function.
        The function checks if the list is a list of dictionaries
        and if the dictionaries contain the required keys.
        ----------
        Input:
            - snp_list: list[dict[str, str | int]]
                The SNP list to be validated
        Raises:
            - IncorrectSNPConfiguration: If the SNP list is not valid
        ----------
        """
        if not isinstance(snp_list, list):
            logging.error(
                "SNP list is not a list in configuration file, exiting..."
            )
            raise IncorrectSNPConfiguration(self.config_file)

        required_keys: set[str] = {"SNP", "ref", "alt", "pos"}
        for index, entry in enumerate(snp_list):
            if not isinstance(entry, dict):
                logging.error(
                    "SNP entry in configuration file is not a dictionary, exiting..."
                )
                raise IncorrectSNPConfiguration(self.config_file)
            missing: set[str] = required_keys - entry.keys()
            if missing:
                logging.error(
                    "SNP entry in configuration file has missing keys: %s, exiting..."
                )
                raise IncorrectSNPConfiguration(self.config_file)
            self._validate_snp_entry(index, entry)
        return True

    def _validate_snp_entry(
        self, index: int, entry: dict[str, str | int]
    ) -> None:
        """
        Function that validates a single SNP entry of the SNP list.
        The entry should be a dictionary with the following keys:
            - SNP: str
            - ref: str
            - alt: str
            - pos: int
        The values should be of the correct type and not empty.
        This pattern is used to create the reference database
        and to run the query.
        ----------
        Input:
            - index: The index of the entry in the SNP list
            - entry: The entry to be validated
        Raises:
            - IncorrectSNPConfiguration: If the entry is not valid
        ----------
        """
        snp, ref, alt, pos = (
            entry["SNP"],
            entry["ref"],
            entry["alt"],
            entry["pos"],
        )
        if not (
            isinstance(snp, str)
            and snp
            and isinstance(ref, str)
            and ref
            and isinstance(alt, str)
            and alt
            and isinstance(pos, int)
            and pos >= 1
        ):
            logging.error(
                "SNP entry %d is not valid in configuration file %s",
                index,
                self.config_file,
            )
            raise IncorrectSNPConfiguration(self.config_file)

    def get_snp_list(self) -> list[dict[str, str | int]]:
        """
        Function that returns the SNP list from the pattern
        after it is retrieved from the pattern and validated.
        When retrieving the SNP list, the pattern also contains
        gene information, which is not needed and is removed from
        the list.

        *Please note the pattern existence itself has already been
        checked in the validate_pattern_keys function.
        ----------
        Output:
            - list[dict[str, str | int]]: List of SNPs like:
            [
                {
                    "SNP": "gyrA",
                    "ref": "ATG",
                    "alt": "L",
                    "pos": 1
                },
                {
                    "SNP": "gyrA",
                    "ref": "CCC",
                    "alt": "F",
                    "pos": 2
                },
        ]
        Raises:
            - IncorrectSNPConfiguration: If the SNP list is not valid
        ----------
        """
        SNP_list: list[dict[str, str | int]] = self.pattern["pattern"]
        # Remove dictionaries from the list that are having 'gene' as first key
        SNP_list = [
            entry
            for entry in SNP_list
            if not next(iter(entry)).startswith("gene")
        ]
        if self.validate_SNP_list(SNP_list):
            return SNP_list
        else:
            logging.error(
                "SNP list is not valid in configuration file %s",
                self.config_file,
            )
            raise IncorrectSNPConfiguration(self.config_file)

    def validate_pointfinder_genes_file(
        self, pointfinder_genes_file: str
    ) -> str:
        """
        Little helper function that checks if the PointFinder genes file
        exists. If it does, it returns the path to the file.
        If it does not, it raises an error.
        ----------
        Input:
            - pointfinder_genes_file: str
                Path to the PointFinder genes file
        Output:
            - str: Path to the PointFinder genes file
        Raises:
            - IncorrectSNPConfiguration: If the PointFinder genes file
                is not found
        ----------
        """
        if os.path.exists(pointfinder_genes_file):
            return pointfinder_genes_file
        else:
            logging.error(
                "PointFinder genes file %s not found, exiting...",
                pointfinder_genes_file,
            )
            raise IncorrectSNPConfiguration(self.config_file)

    def get_pointfinder_genes_file(self) -> str:
        """
        Function that returns the path to the PointFinder genes file
        from the pattern. The path is not checked for correctness,
        but only for existence.
        The path is required for the database creation.
        ----------
        Output:
            - str: Path to the PointFinder genes file
        ----------
        """
        try:
            pointfinder_genes_file: str = self.pattern["database"][
                "pointfinder_genes_file"
            ]
        except KeyError as e:
            logging.error(
                "PointFinder genes file not found in configuration file %s",
                self.config_file,
            )
            raise IncorrectSNPConfiguration(self.config_file) from e
        return self.validate_pointfinder_genes_file(pointfinder_genes_file)
