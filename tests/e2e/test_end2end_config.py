#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

End-to-end test for the main function of pacini_typing.
This file tests full runs of the program with config option.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-09-24"
__all__ = [
    "setup_teardown_config_input",
    "cleanup_files",
]

import os
import shutil
from typing import Generator

import pandas as pd
import pytest

from command_utils import CommandInvoker, ShellCommand
from pacini_typing import main

FASTA_FILE = "test_data/VIB_EA5348AA_AS.fasta"
FASTQ_1 = "test_data/VIB_EA5348AA_AS_1.fq"
FASTQ_2 = "test_data/VIB_EA5348AA_AS_2.fq"
DIR_PATH = "test_full_run/"
OUTPUT = [
    "VIB_EA5348AA_AS_hits_report.csv",
    "VIB_EA5348AA_AS_report.csv",
    "VIB_EA5348AA_AS_sequences.fasta",
]

skip_in_ci = pytest.mark.skipif(
    os.getenv("CI") == "true", reason="Test not supported in CI"
)


@pytest.fixture()
@skip_in_ci
def setup_teardown_config_input() -> Generator[list[str], None, None]:
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
    args = [
        "--verbose",
        "--config",
        "test_data/test_O1.yaml",
        "--fasta-out",
        "--input",
        FASTA_FILE,
    ]
    # Make the directory for the test
    os.mkdir(DIR_PATH)
    # Yield the arguments and clean up afterwords
    yield args
    cleanup_files()


def cleanup_files() -> None:
    """
    Function to clean up the files created during the test
    Is simply removes the directory and all files in it
    """
    if os.path.exists(DIR_PATH):
        # Remove all files in the directory
        for file_name in os.listdir(DIR_PATH):
            file_path = os.path.join(DIR_PATH, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        # Remove the directory itself
        os.rmdir(DIR_PATH)


@skip_in_ci
def test_config_run(
    setup_teardown_config_input: Generator[list[str], None, None]
) -> None:
    """
    End-to-end test for the main function with single input
    it runs the main function of pacini_typing with the single input arguments
    and checks if the output file is successfully created.
    The output file is not checked for contents in this test,
    that is done in another test.
    ----------
    Input:
        setup_teardown_single_input: Generator ->
            Pytest fixture for the single input test
    ----------
    """
    main(setup_teardown_config_input)
    CommandInvoker(
        ShellCommand(["mv", "VIB_EA5348AA_AS_*", DIR_PATH], capture=True)
    ).execute()

    for output_file in OUTPUT:
        assert os.path.exists(f"{DIR_PATH}{output_file}")
        check_file_contents(output_file)


def check_file_contents(file: str) -> None:
    """
    Function to check the contents of the output file
    It checks if the output file contains the expected contents
    """
    expected_output: pd.DataFrame = pd.read_csv(
        f"test_data/expected_output/expected_config_{file}", sep="\t"
    )
    run_output: pd.DataFrame = pd.read_csv(f"{DIR_PATH}{file}", sep="\t")

    # Ignore the last column, beacuse of the difference:
    # BLAST outputs a e-value, while KMA outputs a p-value
    # These values aren't been taking into account into the making
    # Of the report, so skip it for the test
    expected_output = expected_output.iloc[:, :-1]
    run_output = run_output.iloc[:, :-1]

    pd.testing.assert_frame_equal(run_output, expected_output)


@skip_in_ci
def test_config_paired_run(
    setup_teardown_config_input: Generator[list[str], None, None]
) -> None:
    """
    Function that tests the main function with paired input
    it runs the main function of pacini_typing with the paired input arguments
    and checks if the output files are successfully created.
    ----------
    Input:
        setup_teardown_config_input: fixture for the paired input test
    ----------
    """
    setup_teardown_config_input[-1] = FASTQ_1
    setup_teardown_config_input.append(FASTQ_2)
    main(setup_teardown_config_input)
    CommandInvoker(
        ShellCommand(["mv", "VIB_EA5348AA_AS_*", DIR_PATH], capture=True)
    ).execute()

    for output_file in OUTPUT:
        assert os.path.exists(f"{DIR_PATH}{output_file}")
        check_file_contents(output_file)
