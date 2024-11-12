#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

End-to-end test for the makedatabase command of Pacini-typing
This test checks if the KMA and BLAST databases are created successfully

File contents are binary,
so there is no need to check the contents of the files.

The functions is_tool and check_tools are used to check if
the required tools are installed.

The setup_teardown fixture is used to set up the arguments for the tests.
It creates a directory for the test and yields the arguments for the test.
After the test is run, it cleans up the files created during the test.
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-10-30"
__all__ = [
    "setup_teardown",
    "cleanup_files",
]

import os
import platform
import shutil
from typing import Generator

import pytest

from pacini_typing import main

INPUT_FILE = "test_data/vibrio_genes.fasta"
DATABASE_PATH = "./refdir/"
DATABASE_NAME = "mydb"

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


def is_tool(name: str) -> bool:
    """
    Basic function to check if a tool is installed
    It uses the shutil.which() function to check if the tool is in the PATH
    ----------
    Input:
        name: str -> Name of the tool to check
    Output:
        bool -> True if the tool is installed, False otherwise
    ----------
    """
    return shutil.which(name) is not None


@pytest.fixture(scope="module", autouse=True)
def check_tools():
    """
    Fixture to check if the required tools are installed
    If the tools are not installed, the test will fail
    KMA and BLASTN are required for a run of Pacini-typing
    ----------
    Raises:
        pytest.fail
    ----------
    """
    if platform.system() == "Linux":
        pytest.skip("Test not supported on Linux")

    required_tools = ["kma_index", "makeblastdb"]
    missing_tools = [tool for tool in required_tools if not is_tool(tool)]
    if missing_tools:
        pytest.skip(
            f"Skipping tests because the following tools are missing: {', '.join(missing_tools)}"
        )


@pytest.fixture()
def setup_teardown() -> Generator[list[str], None, None]:
    """
    Pytest fixture that sets up the arguments for the single input test
    It creates a Generator object that yields the arguments
    After the test is run, it cleans up the files created during the test
    The generator does not accept or return any arguments

    Test is skipped if the platform is Linux,
    this is due to the use of GitHub actions
    ----------
    Output:
        args: list[str] -> List of arguments for the test
    ----------
    """
    if platform.system() == "Linux":
        pytest.skip("Test not supported on Linux")

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
    os.mkdir(dir_path)

    yield args
    cleanup_files(dir_path)


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


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def test_make_kma_database(setup_teardown: list[str]) -> None:
    """
    Function to test the creation of a KMA database
    It runs the main function of Pacini_typing with the setup_teardown fixture
    After the test is run,
    it checks if the database files are created successfully
    ----------
    Input:
        setup_teardown: list[str] -> Arguments for the test
    ----------
    """
    main(setup_teardown)
    for kma_extension in KMA_EXTENSIONS:
        assert os.path.exists(f"{DATABASE_PATH}{DATABASE_NAME}{kma_extension}")


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def test_make_blast_database(setup_teardown: list[str]) -> None:
    """
    Function to test the creation of a BLAST database
    It runs the main function of Pacini_typing with the setup_teardown fixture
    After the test is run,
    it checks if the database files are created successfully
    ----------
    Input:
        setup_teardown: list[str] -> Arguments for the test
    ----------
    """
    setup_teardown[-1] = "fasta"
    main(setup_teardown)
    for blast_extension in BLAST_EXTENSIONS:
        assert os.path.exists(f"{DATABASE_PATH}{DATABASE_NAME}{blast_extension}")
