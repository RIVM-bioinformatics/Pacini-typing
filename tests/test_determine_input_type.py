#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Test module for the determine_input_type module.

This module is used to test what happens if wrong files are
passed to the determine_input_type module.
These tests are used to check if the module can correctly
determine the file type and if it can correctly validate

The tests are applied by StringIO objects that are used to
simulate file objects. But also real files are used,
and bigger datasets with larger sequences.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-09-24"
__all__ = [
    "setup_valid_data",
    "test_validate_fasta_valid",
    "test_validate_fasta_no_header",
    "test_validate_fasta_invalid_sequence",
    "test_validate_fastq_valid",
    "test_validate_fastq_missing_plus",
    "test_validate_fastq_length_mismatch",
    "test_determine_file_type_fasta",
    "test_determine_file_type_fastq",
    "test_compare_types_mixed",
    "test_compare_types_same",
    "test_empty_file",
]

import os
from io import StringIO

import pytest

from preprocessing.exceptions.determine_input_type_exceptions import (
    InvalidFastaOrFastqError,
    InvalidSequenceError,
    InvalidSequencingTypesError,
)
from preprocessing.validation.determine_input_type import InputFileInspector

skip_in_ci = pytest.mark.skipif(
    os.getenv("CI") == "true",
    reason="Test online (GitHub Action) not available due to dependencies",
)


@pytest.fixture
def setup_valid_data() -> dict[str, str]:
    """
    Simple fixture to provide valid and invalid FASTA and FASTQ data.
    The variations are used to test the validation functions.
    ----------
    Output:
        - dict: A dictionary with valid and invalid FASTA and FASTQ data.
    ----------
    """
    return {
        "valid_fasta": ">header1\nACTGACTG\n>header2\nGTACTGAC\n",
        "invalid_fasta_no_header": "ACTGACTG\nGTACTGAC\n",
        "invalid_fasta_invalid_sequence": ">header1\nACTGXCTG\n",
        "valid_fastq": (
            "@header1\nACTGACTG\n+\nB@@FDFFF\n"
            "@header2\nGTACTGAC\n+\nB@@FDFFF\n"
        ),
        "invalid_fastq_missing_plus": (
            "@header1\nACTGACTG\nINVALID_LINE\n!~@#$%^&*\n"
        ),
        "invalid_fastq_length_mismatch": ("@header1\nACTGACTG\n+\n!~@#\n"),
    }


def test_validate_fasta_valid(setup_valid_data: dict[str, str]):
    """
    Function that tests if a valid FASTA file passes validation.
    It's a sunny day test: everything should pass.
    ----------
    Input:
        - setup_valid_data: valid and invalid FASTA and FASTQ data.
    ----------
    """
    inspector = InputFileInspector([])
    file_handle = StringIO(setup_valid_data["valid_fasta"])

    inspector.validate_fasta(file_handle, "valid.fasta")


def test_validate_fasta_no_header(setup_valid_data: dict[str, str]):
    """
    Function that tests if a FASTA file with no header raises an error.
    ----------
    Input:
        - setup_valid_data: valid and invalid FASTA and FASTQ data.
    ----------
    """
    inspector = InputFileInspector([])
    file_handle = StringIO(setup_valid_data["invalid_fasta_no_header"])
    with pytest.raises(InvalidFastaOrFastqError):
        inspector.validate_fasta(file_handle, "no_header.fasta")


def test_validate_fasta_invalid_sequence(setup_valid_data: dict[str, str]):
    """
    Function that tests if a FASTA file with an
    invalid sequence raises an error.
    ----------
    Input:
        - setup_valid_data: valid and invalid FASTA and FASTQ data.
    ----------
    """
    inspector = InputFileInspector([])
    file_handle = StringIO(setup_valid_data["invalid_fasta_invalid_sequence"])
    with pytest.raises(InvalidSequenceError):
        inspector.validate_fasta(file_handle, "invalid_sequence.fasta")


def test_validate_fastq_valid(setup_valid_data: dict[str, str]):
    """
    Test a valid FASTQ file passes validation.
    This test should simply pass.
    -----------
    Input:
        - setup_valid_data: valid and invalid FASTA and FASTQ data.
    ----------
    """
    inspector = InputFileInspector([])
    file_handle = StringIO(setup_valid_data["valid_fastq"])

    inspector.validate_fastq(file_handle, "valid.fastq")


def test_validate_fastq_missing_plus(setup_valid_data: dict[str, str]):
    """
    Function that tests FASTQ file with missing '+' line raises an error.
    ----------
    Input:
        - setup_valid_data: valid and invalid FASTA and FASTQ data.
    ----------
    """
    inspector = InputFileInspector([])
    file_handle = StringIO(setup_valid_data["invalid_fastq_missing_plus"])
    with pytest.raises(InvalidFastaOrFastqError):
        inspector.validate_fastq(file_handle, "missing_plus.fastq")


def test_validate_fastq_length_mismatch(setup_valid_data: dict[str, str]):
    """
    Function that tests FASTQ file with mismatched sequence and
    quality lengths raises an error.
    ----------
    Input:
        - setup_valid_data: valid and invalid FASTA and FASTQ data.
    ----------
    """
    inspector = InputFileInspector([])
    file_handle = StringIO(setup_valid_data["invalid_fastq_length_mismatch"])
    with pytest.raises(InvalidFastaOrFastqError):
        inspector.validate_fastq(file_handle, "length_mismatch.fastq")


@skip_in_ci
def test_determine_file_type_fasta():
    """
    Function that tests file type determination for a FASTA file.
    It is tested with a real file and should give FASTA as output.
    """
    file_validator = InputFileInspector(["test_data/VIB_EA5348AA_AS.fasta"])
    assert file_validator.get_file_type() == "FASTA"


@skip_in_ci
def test_determine_file_type_fastq():
    """
    Function that tests file type determination for a FASTQ file.
    It is tested with a real file and should give FASTQ as output.
    """
    paired_validator = InputFileInspector(
        ["test_data/VIB_EA5348AA_AS_1.fq", "test_data/VIB_EA5348AA_AS_2.fq"]
    )
    assert paired_validator.get_file_type() == "FASTQ"


@skip_in_ci
def test_compare_types_mixed():
    """
    Function that tests if an error is raised for
    mixed FASTA and FASTQ files.
    """
    with pytest.raises(InvalidSequencingTypesError):
        InputFileInspector(
            [
                "test_data/VIB_EA5348AA_AS_1.fq",
                "test_data/VIB_EA5348AA_AS.fasta",
            ]
        )


@skip_in_ci
def test_compare_types_same():
    """
    Function that tests if error is raised for multiple files of the same type.
    So this only applies to two FASTA files in this case.
    """
    with pytest.raises(InvalidSequencingTypesError):
        InputFileInspector(
            ["test_data/vibrio_genes.fasta", "test_data/VIB_EA5348AA_AS.fasta"]
        )


def test_empty_file():
    """
    Function that tests if an error is raised for an empty file.
    """
    with pytest.raises(InvalidFastaOrFastqError):
        InputFileInspector(["test_data/wrong_files/empty.fasta"])
