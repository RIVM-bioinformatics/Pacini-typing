#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

End-to-end test for the makedatabase command of Pacini-typing
This test checks if the KMA and BLAST databases are created successfully.

The setup_teardown fixture is used to set up the arguments for the tests.
It creates a directory for the test and yields the arguments for the test.
After the test is run, it cleans up the files created during the test.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-10-30"
__all__ = [
    "test_existence_of_tools",
    "setup_teardown",
    "cleanup_files",
    "test_make_kma_database",
    "test_make_blast_database",
    "compare_result_with_expected_files",
]

import os
import shutil
from typing import Generator

import pytest

from pacini_typing import main
from preprocessing.validation import validating_input_arguments
from tests.e2e.check_tool_existence import check_tools

INPUT_FILE = "test_data/vibrio_genes.fasta"
DATABASE_PATH = "./refdir/"
DATABASE_NAME = "mydb"

# Expected file extensions for KMA and BLAST databases
KMA_EXTENSIONS = [
    ".comp.b",
    ".length.b",
    ".name",
    ".seq.b",
]

BLAST_EXTENSIONS = [
    ".ndb",
    ".nhr",
    ".nin",
    ".njs",
    ".not",
    ".nsq",
    ".ntf",
    ".nto",
]

skip_in_ci = pytest.mark.skipif(
    os.getenv("CI") == "true",
    reason="Test online (GitHub Action) not available due to dependencies",
)


@skip_in_ci
def test_existence_of_tools() -> None:
    """
    Function to test the existence of the required tools for
    this test script.
    """
    check_tools(["kma_index", "makeblastdb"])


@pytest.fixture
@skip_in_ci
def setup_teardown() -> Generator[list[str], None, None]:
    """
    Pytest fixture that sets up the arguments for the single input test
    It creates a Generator object that yields the arguments.
    ----------
    Output:
        - args: list of arguments for the test
    ----------
    """
    args = [
        "--verbose",
        "makedatabase",
        "--input_file",
        INPUT_FILE,
        "--database_path",
        DATABASE_PATH,
        "--database_name",
        DATABASE_NAME,
        "--database_type",
        "fastq",
    ]

    dir_path = "test_full_run/"
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    yield args
    cleanup_files(dir_path)


def cleanup_files(dir_path: str) -> None:
    """
    Function to clean up the files created during the test
    Is simply removes the directory and all files in it
    ----------
    Input:
        - dir_path: path to the directory to remove
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


@skip_in_ci
def test_make_kma_database(setup_teardown: list[str]) -> None:
    """
    Function to test the creation of a KMA database
    It runs the main function of pacini_typing with the setup_teardown fixture
    After the test is run,
    it checks if the database files are created successfully
    ----------
    Input:
        - setup_teardown: list of arguments for the test
    ----------
    """
    main(setup_teardown)
    for kma_extension in KMA_EXTENSIONS:
        assert os.path.exists(f"{DATABASE_PATH}{DATABASE_NAME}{kma_extension}")
    compare_result_with_expected_files(KMA_EXTENSIONS, "fastq")


def compare_result_with_expected_files(
    extensions: list[str], database_type: str
) -> None:
    """
    Function to compare the files created by KMA with the expected files.
    It checks if the files are created successfully
    ----------
    Input:
        - extensions: list of extensions of the files to compare
    ----------
    """
    for extension in extensions:
        expected_file = f"test_data/expected_databases/expected_{database_type}_db{extension}"
        output_file = f"{DATABASE_PATH}{DATABASE_NAME}{extension}"
        assert validating_input_arguments.ArgsValidator.create_sha_hash(
            expected_file
        ) == validating_input_arguments.ArgsValidator.create_sha_hash(
            output_file
        )


@skip_in_ci
def test_make_blast_database(setup_teardown: list[str]) -> None:
    """
    Function to test the creation of a BLAST database.
    The main function of pacini_typing is run with the arguments.
    File existence is checked after the test is run.
    Expected files are not used, because of the binary files
    that changes with each run.
    ----------
    Input:
        - setup_teardown: list of arguments
    ----------
    """
    setup_teardown[-1] = "fasta"
    main(setup_teardown)
    for blast_extension in BLAST_EXTENSIONS:
        assert os.path.exists(
            f"{DATABASE_PATH}{DATABASE_NAME}{blast_extension}"
        )
