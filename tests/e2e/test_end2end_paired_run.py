#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

End-to-end test for the main function of pacini_typing.
This file tests full runs of the program with paired input (FASTQ).

The setup_teardown fixture is used to set up the arguments for the tests.
It creates a directory for the test and yields the arguments for the test.
After the test is run, it cleans up the files created during the test.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-09-24"
__all__ = [
    "test_existence_of_tools",
    "setup_teardown_paired_input",
    "cleanup_files",
    "test_paired_run",
    "check_file_contents",
]

import os
import shutil
from typing import Generator

import pandas as pd
import pytest

from pacini_typing import main
from preprocessing.validation import validating_input_arguments
from tests.e2e.check_tool_existence import check_tools

RUN_OUTPUT = "test_full_run/myresults"

EXPECTED_FILES = [
    "test_data/expected_output/expected_paired_VIB_EA5348AA.res",
    "test_data/expected_output/expected_paired_VIB_EA5348AA.aln",
    "test_data/expected_output/expected_paired_VIB_EA5348AA.fsa",
    "test_data/expected_output/expected_paired_VIB_EA5348AA.frag.gz",
]

skip_in_ci = pytest.mark.skipif(
    os.getenv("CI") == "true",
    reason="Test online (GitHub Action) not available due to dependencies",
)


@skip_in_ci
def test_existence_of_tools() -> None:
    """
    Function to test the existence of the required tools for
    this test script
    """
    check_tools(["kma", "blastn"])


@pytest.fixture()
@skip_in_ci
def setup_teardown_paired_input() -> Generator[list[str], None, None]:
    """
    Pytest fixture that sets up the arguments for the paired input test.
    It creates a Generator object that yields the arguments.
    The generator does not accept or return any arguments
    ----------
    Output:
        - args: list of arguments for the test
    ----------
    """
    args = [
        "--verbose",
        "query",
        "--paired",
        "test_data/VIB_EA5348AA_AS_1.fq",
        "test_data/VIB_EA5348AA_AS_2.fq",
        "--output",
        RUN_OUTPUT,
        "--database_path",
        "./refdir/",
        "--database_name",
        "mykma",
    ]
    dir_path = "test_full_run/"
    os.mkdir(dir_path)

    yield args
    cleanup_files(dir_path)


def cleanup_files(dir_path: str) -> None:
    """
    Function to clean up the files created during the test
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
def test_paired_run(setup_teardown_paired_input: list[str]) -> None:
    """
    End-to-end test for the main function with paired input.
    It runs the main function of pacini_typing with the paired input arguments
    and checks if the output file is successfully created.
    ----------
    Input:
        - setup_teardown_paired_input: list of input arguments
    ----------
    """
    main(setup_teardown_paired_input)
    assert os.path.exists(f"{RUN_OUTPUT}.fsa")
    assert os.path.exists(f"{RUN_OUTPUT}.res")
    assert os.path.exists(f"{RUN_OUTPUT}.frag.gz")
    assert os.path.exists(f"{RUN_OUTPUT}.aln")
    check_file_contents()


def check_file_contents() -> None:
    """
    File that checks the contents of the tsv output file
    with the expected output file. The actual comparison is done
    in the compare_output_files function.
    """
    run_output = pd.read_csv(f"{RUN_OUTPUT}.res", sep="\t")
    expected_output = pd.read_csv(EXPECTED_FILES[0], sep="\t")

    # Use the equals function of the pandas DataFrame to compare the files
    pd.testing.assert_frame_equal(run_output, expected_output)
    compare_additional_files()


def compare_additional_files() -> None:
    """
    Function to compare the additional output files.
    The function compares the hash of the output files with the expected
    hash of the expected files.
    For this hash comparison, the create_sha_hash function of the
    ArgsValidator class is used.
    """
    for output_file, expected_file in zip(
        [
            f"{RUN_OUTPUT}.aln",
            f"{RUN_OUTPUT}.fsa",
            f"{RUN_OUTPUT}.frag.gz",
        ],
        EXPECTED_FILES[1:],
    ):
        assert validating_input_arguments.ArgsValidator.create_sha_hash(
            output_file
        ) == validating_input_arguments.ArgsValidator.create_sha_hash(
            expected_file
        )
