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

The check_tools and is_tool functions are used to check if the required tools are installed.

The setup_teardown_single_input fixture is used to set up the arguments for the single input test.
It creates a directory for the test and yields the arguments for the test.
After the test is run, it cleans up the files created during the test.

Example output of Pacini-typing for a single input file (BLAST results):

VIB_EA5348AA_AS_NODE_11_length_166519_cov_13.420434	rfbV_O1:1:AE003852	100.000	1233	0	0	106763	107995	1233	1	0.0	2278
VIB_EA5348AA_AS_NODE_11_length_166519_cov_13.420434	wbfZ_O139:1:AB012956	96.907	1164	35	1	111617	112780	15	1177	0.0	1949
VIB_EA5348AA_AS_NODE_19_length_64079_cov_13.745954	ctxA:1:CP001235	100.000	777	0	0	54336	55112	1	777	0.0	1435
VIB_EA5348AA_AS_NODE_19_length_64079_cov_13.745954	ctxB:1:KJ437653	96.532	346	12	0	53994	54339	346	1	4.79e-165	573
"""

__author__ = "Mark van de Streek"
__date__ = "2024-09-24"
__all__ = [
    "check_tools",
    "is_tool",
    "setup_teardown_single_input",
    "cleanup_files",
    "test_single_run",
    "check_file_contents",
]

import os
import platform
import shutil
from typing import Generator
import pandas as pd

import pytest

from pacini_typing import main

FASTA_FILE = "test_data/VIB_EA5348AA_AS.fasta"
RUN_OUTPUT = "test_full_run/myresults"
DATABASE_PATH = "./refdir/"
DATABASE_NAME = "my_blast_db"


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


@pytest.mark.skipif(
    platform.system() == "Linux", reason="Test not supported on Linux"
)
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
