#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

End-to-end test for the main function of pacini_typing.
This file tests full runs of the program with single input files (FASTA).

The setup_teardown fixture is used to set up the arguments for the tests.
It creates a directory for the test and yields the arguments for the test.
After the test is run, it cleans up the files created during the test.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-09-24"
__all__ = [
    "test_existence_of_tools",
    "setup_teardown_single_input",
    "cleanup_files",
    "test_single_run",
    "check_file_contents",
]

import os
import shutil
from typing import Generator

import pandas as pd
import pytest

from pacini_typing import main
from tests.e2e.check_tool_existence import check_tools

FASTA_FILE = "test_data/VIB_EA5348AA_AS.fasta"
RUN_OUTPUT = "test_full_run/myresults"
DATABASE_PATH = "./refdir/"
DATABASE_NAME = "my_blast_db"

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
    check_tools(["kma", "blastn"])


@pytest.fixture
@skip_in_ci
def setup_teardown_single_input() -> Generator[list[str], None, None]:
    """
    Pytest fixture that sets up the arguments for the single input test.
    It creates a Generator object that yields the arguments.
    After the test is run, it cleans up the files created during the test.
    The generator does not accept or return any arguments
    ----------
    Output:
        - args: list of arguments for the test
    ----------
    """
    args = [
        "--verbose",
        "query",
        "--single",
        FASTA_FILE,
        "--output",
        RUN_OUTPUT,
        "--database_path",
        DATABASE_PATH,
        "--database_name",
        DATABASE_NAME,
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
def test_single_run(setup_teardown_single_input: list[str]) -> None:
    """
    End-to-end test for the main function with single input.
    It runs the main function of pacini_typing with the single input arguments
    and checks if the output file is successfully created.
    The output file is not checked for contents in this test,
    that is done in another test.
    ----------
    Input:
        - setup_teardown_single_input: list of arguments for the test
    ----------
    """
    main(setup_teardown_single_input)
    assert os.path.exists("test_full_run/myresults.tsv")
    check_file_contents()


def check_file_contents() -> None:
    """
    File that checks the contents of the tsv output file
    with the expected output file
    """
    run_output: pd.DataFrame = pd.read_csv(f"{RUN_OUTPUT}.tsv", sep="\t")
    expected_output: pd.DataFrame = pd.read_csv(
        "test_data/expected_output/expected_non_paired_VIBEA5348AA_AS.tsv",
        sep="\t",
    )

    pd.testing.assert_frame_equal(run_output, expected_output)
