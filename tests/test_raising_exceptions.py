#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

This module contains tests for testing some of the failure cases
There are already smaller unit tests that test the individual functions,
but these tests are used to test the entire pipeline with the wrong input
It only tests the cases where the input is wrong, so it's not a complete
end-to-end test setup.
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-10-30"
__all__ = [
    "setup_args",
    "test_wrong_extension",
    "test_not_existing_file",
    "test_wrong_sequence",
    "test_wrong_fasta_construction",
]

import os
import shutil
from typing import Generator

import pytest

from pacini_typing import main
from preprocessing.exceptions.determine_input_type_exceptions import (
    InvalidFastaOrFastqError,
    InvalidSequenceError,
    InvalidSequencingTypesError,
)
from preprocessing.exceptions.validation_exceptions import (
    FileNotExistsError,
    InvalidFileExtensionError,
    InvalidPairedError,
)


@pytest.fixture()
def setup_args() -> Generator[list[str], None, None]:
    """
    Pytest fixture that sets up the arguments for tests.
    It creates a Generator object that yields the arguments
    After the test is run, it comes back and looks for possible cleanup

    Test is skipped if the platform is Linux,
    this is due to the use of GitHub actions
    ----------
    Output:
        args: list[str] -> List of arguments for the test
    ----------
    """
    args = [
        "--config",
        "parsing/O1.yaml",
        "--input",
    ]

    yield args
    # If a test is not failing,
    # clean up the files created during the test
    cleanup_files("databases/")
    cleanup_files("output/")


def cleanup_files(dir_path: str) -> None:
    """
    Function to clean up the files created during the test
    Is simply removes the directory and all files in it
    ----------
    Input:
        dir_path: str -> Path to the directory to remove
    ----------
    """
    if os.path.exists(dir_path):
        # Remove all files in the directory
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        # Remove the directory itself
        os.rmdir(dir_path)


def test_wrong_extension(setup_args: list[str]):
    """
    Test if the InvalidFileExtensionError is raised when
    the wrong extension is provided for the database.
    ----------
    Input:
        setup_args: list[str] -> Arguments for the test
    ----------
    """
    setup_args.extend(
        [
            "test_data/wrong_files/sample_1.ff",
            "test_data/wrong_files/sample_2.ff",
        ]
    )
    with pytest.raises(InvalidFileExtensionError):
        main(setup_args)
        setup_args[-1] = "test_data/sample_3.fq"
        main(setup_args)


def test_not_existing_file(setup_args: list[str]):
    """
    Test if the FileNotExistsError is raised when
    a file that does not exist is provided.
    ----------
    Input:
        setup_args: list[str] -> Arguments for the test
    ----------
    """
    setup_args.extend(["test_data/VIBAABBCC_1.fq", "test_data/VIBAABBCC_2.fq"])
    with pytest.raises(FileNotExistsError):
        main(setup_args)


def test_wrong_sequence(setup_args: list[str]):
    """
    Test if the InvalidSequenceError is raised when
    the wrong sequence is provided for the database.

    In this case, the sequence is mutated with wrong characters
    ----------
    Input:
        setup_args: list[str] -> Arguments for the test
    ----------
    """
    setup_args.extend(["test_data/wrong_files/wrong_sequence.fasta"])
    with pytest.raises(InvalidSequenceError):
        main(setup_args)


def test_wrong_fasta_construction(setup_args: list[str]):
    """
    Test if the InvalidFastaOrFastqError is raised when
    a file is provided which is not a valid FASTA file.

    In this case, the header line '>' is changed to '+'
    ----------
    Input:
        setup_args: list[str] -> Arguments for the test
    ----------
    """
    setup_args.extend(["test_data/wrong_files/wrong_constructed.fasta"])
    with pytest.raises(InvalidFastaOrFastqError):
        main(setup_args)


def test_wrong_fastq_construction(setup_args: list[str]):
    """
    Test if the InvalidFastaOrFastqError is raised when
    a file is provided which is not a valid FASTQ file.

    In this case, the seperator line '+' is changed to '-'
    ----------
    Input:
        setup_args: list[str] -> Arguments for the test
    ----------
    """
    setup_args.extend(["test_data/wrong_files/wrong_constructed.fastq"])
    with pytest.raises(InvalidFastaOrFastqError):
        main(setup_args)


def test_wrong_fastq_construction_2(setup_args: list[str]):
    """
    Test if the InvalidFastaOrFastqError is raised when
    a file is provided which is not a valid FASTQ file.

    In this case, the fastq file quality score line length
    is not equal to the sequence length
    ----------
    Input:
        setup_args: list[str] -> Arguments for the test
    ----------
    """
    setup_args.extend(["test_data/wrong_files/wrong_constructed_2.fastq"])
    with pytest.raises(InvalidFastaOrFastqError):
        main(setup_args)


def test_wrong_pairing(setup_args: list[str]):
    """
    Test if the InvalidPairedError is raised when
    the wrong files are provided.
    ----------
    Input:
        setup_args: list[str] -> Arguments for the test
    ----------
    """
    setup_args.extend(
        [
            "test_data/wrong_files/VIB_EA5348AA_AS.fasta",
            "test_data/wrong_files/VIB_EA5348AA_AS_1.fq",
        ]
    )
    with pytest.raises(InvalidPairedError):
        main(setup_args)


def test_wrong_fastq_input(setup_args: list[str]):
    """
    Test if the InvalidSequencingTypesError is raised when
    the wrong amount of input files are provided.
    ----------
    Input:
        setup_args: list[str] -> Arguments for the test
    ----------
    """
    setup_args.extend(["test_data/wrong_files/VIB_EA5348AA_AS_1.fq"])
    with pytest.raises(InvalidSequencingTypesError):
        main(setup_args)


def test_wrong_fasta_input(setup_args: list[str]):
    """
    Test if the InvalidPairedError is raised when
    the wrong amount of input files are provided.
    ----------
    Input:
        setup_args: list[str] -> Arguments for the test
    ----------
    """
    setup_args.extend(
        [
            "test_data/wrong_files/VIB_EA5348AA_AS.fasta",
            "test_data/wrong_files/vibrio_genes.fasta",
        ]
    )
    with pytest.raises(InvalidPairedError):
        main(setup_args)


def test_wrong_fasta_with_fastq_names(setup_args: list[str]):
    """
    Test if the InvalidInputError is raised when
    the wrong amount of input files are provided.

    In this case, two FASTA files are provided with FASTQ names.
    ----------
    Input:
        setup_args: list[str] -> Arguments for the test
    ----------
    """
    setup_args.extend(
        ["test_data/wrong_files/VIB_1.fq", "test_data/wrong_files/VIB_2.fq"]
    )
    with pytest.raises(InvalidSequencingTypesError):
        main(setup_args)
