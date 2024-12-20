#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

# TODO: Add module docstrings
"""

__author__ = "Mark van de Streek"
__date__ = "2024-11-25"
__all__ = [
    "test_read_config_good",
    "test_read_config_file_error",
    "test_read_config_wrong_structure_yaml",
    "test_validate_config_keys_structure_error",
    "test_validate_pattern_keys_structure_error",
    "test_construct_params_dict",
]

import json

import pytest

from parsing import read_config_pattern
from preprocessing.exceptions.parsing_exceptions import (
    YAMLLoadingError,
    YAMLStructureError,
)


def test_read_config_good():
    """
    Test the reading of a good configuration file
    First assert that the pattern var is actually being
    filled with the correct information
    Then, assert the pattern that is being read is the
    same as in the expected file.
    The file /test_data/expected_output/expected_O1_config.json
    contains the expected output of the pattern read from the
    configuration file parsing/O1.yaml
    """
    config = read_config_pattern.ReadConfigPattern("config/O139.yaml", "fasta")
    assert len(config.pattern) > 1
    with open(
        "test_data/expected_output/expected_O139_config.json",
        "r",
        encoding="utf-8",
    ) as file:
        assert config.pattern == json.load(file)


def test_read_config_file_error():
    """
    Test the reading of a non-existing configuration file
    The reading function of the class should raise a FileNotFoundError
    """
    with pytest.raises(FileNotFoundError):
        read_config_pattern.ReadConfigPattern("parsing/O100.yaml", "fasta")


def test_read_config_wrong_structure_yaml():
    """
    Test if wrong YAML structured config files are raising
    the correct exception. In the test_data/wrong_files folder
    there are two files that are not correctly structured.
    The function should raise a YAMLLoadingError.
    Why not a YAMLStructureError?
    This because a wrong constructed YAML file is not valid,
    and therefore could not be read by the yaml module.
    A YAMLStructureError is raised when the structure of the
    YAML file contains wrong keys or is missing keys.
    """
    with pytest.raises(YAMLLoadingError):
        read_config_pattern.ReadConfigPattern(
            "test_data/wrong_files/wrong_constructed_O1.yaml", "fasta"
        )
        read_config_pattern.ReadConfigPattern(
            "test_data/wrong_files/wrong_constructed_O139.yaml", "fasta"
        )


def test_validate_config_keys_structure_error():
    """
    Test if missing/wrong keys in the configuration file are raising
    the correct exception. In the test_data/wrong_files
    folder there are two files that are not correct.
    The incorrectness is in the keys of the configuration file.
    This function should raise a YAMLStructureError.
    """
    with pytest.raises(YAMLStructureError):
        read_config_pattern.ReadConfigPattern(
            "test_data/wrong_files/wrong_keys_O1.yaml", "fasta"
        )
        read_config_pattern.ReadConfigPattern(
            "test_data/wrong_files/wrong_keys_O139.yaml", "fasta"
        )


def test_validate_pattern_keys_structure_error():
    """
    Test if missing/wrong pattern-keys in the configuration file are raising
    the correct exception. In the test_data/wrong_files folder there
    are two files that are not correct. The incorrectness is especially
    in the pattern keys of the configuration file. This function should
    raise a YAMLStructureError.
    """
    with pytest.raises(YAMLStructureError):
        read_config_pattern.ReadConfigPattern(
            "test_data/wrong_files/wrong_pattern_keys_O1.yaml", "fasta"
        )
        read_config_pattern.ReadConfigPattern(
            "test_data/wrong_files/wrong_pattern_keys_O139.yaml", "fasta"
        )


def test_construct_params_dict():
    """
    Test if the construct_params_dict function is working correctly.
    The function should fill the creation_dict with the correct
    parameters. The function should also be able to change the
    input_file_type. The input_file_type should be the same as the
    file_type in the creation_dict.
    ----------
    Note: although the input_file_type should be fasta or fastq,
    the functionality is tested with a custom_file_type.
    potential errors caused by input_file_types that are not
    fasta or fastq are already checked in earlier code
    ----------
    """
    config = read_config_pattern.ReadConfigPattern("config/O1.yaml", "fastq")
    assert (
        config.pattern["database"]["path"]
        == config.creation_dict["database_path"]
    )
    assert (
        config.pattern["database"]["name"]
        == config.creation_dict["database_name"]
    )
    assert config.input_file_type == config.creation_dict["file_type"]
    config.input_file_type = "custom_file_type"
    config.construct_params_dict()
    assert config.input_file_type == config.creation_dict["file_type"]
