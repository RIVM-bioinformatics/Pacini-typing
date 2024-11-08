#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

To be filed in later...

VIB_EA5348AA_AS_NODE_11_length_166519_cov_13.420434	rfbV_O1:1:AE003852	100.000	1233	0	0	106763	107995	1233	1	0.0	2278
VIB_EA5348AA_AS_NODE_11_length_166519_cov_13.420434	wbfZ_O139:1:AB012956	96.907	1164	35	1	111617	112780	15	1177	0.0	1949
VIB_EA5348AA_AS_NODE_19_length_64079_cov_13.745954	ctxA:1:CP001235	100.000	777	0	0	54336	55112	1	777	0.0	1435
VIB_EA5348AA_AS_NODE_19_length_64079_cov_13.745954	ctxB:1:KJ437653	96.532	346	12	0	53994	54339	346	1	4.79e-165	573
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = [
    "check_tools",
    "is_tool",
    "setup_teardown_single_input",
    "cleanup_files",
    "test_single_run",
    "test_single_contents",
    "check_non_empty_content",
    "validate_float_columns",
    "validate_thresholds",
]

import os
import platform
import shutil
from typing import Generator, List

import pytest

from pacini_typing import main

FASTA_FILE = "test_data/VIB_EA5348AA_AS.fasta"
RUN_OUTPUT = "test_full_run/myresults"
DATABASE_PATH = "./refdir/"
DATABASE_NAME = "my_blast_db"
IDENTITY = 90


@pytest.fixture(scope="module", autouse=True)
def check_tools():
    """
    Fixture to check if the required tools are installed
    If the tools are not installed, the test will fail
    KMA and BLASTN are required for a full run of Pacini-typing
    ----------
    Raises:
        pytest.fail
    ----------
    """
    if platform.system() == "Linux":
        pytest.skip("Test not supported on Linux")

    required_tools = ["kma", "blastn"]
    missing_tools = [tool for tool in required_tools if not is_tool(tool)]
    if missing_tools:
        pytest.fail(
            f"Failed tests because the following tools are missing: {', '.join(missing_tools)}"
        )


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


@pytest.fixture()
def setup_teardown_single_input() -> Generator[list[str], None, None]:
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
        "query",
        "--single",
        FASTA_FILE,
        "--output",
        RUN_OUTPUT,
        "--database_path",
        DATABASE_PATH,
        "--database_name",
        DATABASE_NAME,
        "--identity",
        str(IDENTITY),
    ]
    # Make the directory for the test
    dir_path = "test_full_run/"
    os.mkdir(dir_path)
    # Yield the arguments and clean up afterwords
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
def test_single_run(
    setup_teardown_single_input: Generator[list[str], None, None]
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
    main(setup_teardown_single_input)
    assert os.path.exists("test_full_run/myresults.tsv")


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def test_single_contents(
    setup_teardown_single_input: Generator[list[str], None, None]
) -> None:
    """
    End-to-end test for the contents of the output file for the single input
    it runs the main function of pacini_typing with the single input arguments
    and checks the contents of the output file.
    The output file is checked for the correct number of columns.
    """
    main(setup_teardown_single_input)
    output_file = f"{RUN_OUTPUT}.tsv"
    assert os.path.exists(output_file), "Output file was not created"
    with open(output_file, "r", encoding="utf-8") as f:
        for line in f:
            columns = line.strip().split("\t")
            check_non_empty_content(columns)
            assert len(columns) == 12
            validate_float_columns(columns)
            validate_thresholds(columns)


def check_non_empty_content(columns: List[str]) -> None:
    """
    Function to check if the content of the output file is not empty
    If the content is empty, the test fails
    ----------
    Input:
        columns: list -> List of columns in the output file
    ----------
    """
    assert columns != []


def validate_float_columns(columns: List[str]) -> None:
    """
    Function to validate that the columns in the output file are floats
    It tries to convert the columns to floats, if it fails the test fails
    ----------
    Input:
        columns: list -> List of columns in the output file
    Raises:
        pytest.fail -> If the columns are not floats
    ----------
    """
    try:
        float(columns[2])
        float(columns[10])
        float(columns[11])
    except ValueError:
        pytest.fail("Values in the output file are not floats")


def validate_thresholds(columns: List[str]) -> None:
    """
    Validate that the rfbV_O1 column is above a certain threshold
    If the column is below the threshold, the test fails
    ----------
    Input:
        columns: list -> List of columns in the output file
    ----------
    """
    if "rfbV_O1:1" in columns:
        assert 98.0 <= float(columns[2]) <= 100.0
    if "wbfZ_O139" in columns:
        # WbfZ_O139 is not allowed to be 100% identical, only in O139 strains
        # Input file is not a Vibrio cholerae O139 strain
        assert int(columns[2]) != 100
