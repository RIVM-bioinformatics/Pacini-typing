#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

End-to-end test for the main function of pacini_typing.
This file tests full runs of the program with paired input

The check_tools and is_tool functions are used to check if the required tools are installed.

The setup_teardown_single_input fixture is used to set up the arguments for a paired input test.
It creates a directory for the test and yields the arguments for the test.
After the test is run, it cleans up the files created during the test.

Example output of Pacini-typing for a paired input file (KMA results):

Template_Name	Template_Length	Template_Identity	Template_Coverage	Template_Depth	Query_Identity	Query_Coverage	Query_Depth	Read_Count_Map	Read_Count_Aln	Score	Expected	q_value	p_value	ConClave_Score	ConClave_Quality
rfbV_O1:1:AE003852	1233	100.000000	100.000000	48.077048	100.000000	100.000000	48.077048	421	421	59156	52648.350130	378.782282	1.000000e-26	59156	439.517332
wbfZ_O139:1:AB012956	1177	96.176720	99.150382	48.905692	97.000857	97.000857	49.324764	405	401	51524	52873.156064	17.435552	2.972197e-05	51524	433.992120
ctxA:1:CP001235	777	100.000000	100.000000	44.438867	100.000000	100.000000	44.438867	247	247	34493	34640.170051	0.313294	5.756657e-01	34493	417.940467
ctxB:1:KJ437653	348	96.551724	100.287356	40.350575	96.275072	96.275072	40.234957	105	105	12277	15851.962347	454.348640	1.000000e-26	12277	376.619315
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = [
    "check_tools",
    "is_tool",
    "setup_teardown_paired_input",
    "cleanup_files",
    "test_paired_run",
    "test_paired_contents",
    "validate_header_columns",
    "extract_rows_and_validate",
    "check_template_identity_bounds",
    "check_fields_non_empty",
]

import csv
import os
import platform
import shutil
from typing import Generator, Iterator

import pandas as pd
import pytest

from pacini_typing import main
from preprocessing.validation import validating_input_arguments

RUN_OUTPUT = "test_full_run/myresults"

EXPECTED_FILES = [
    "test_data/expected_output/expected_paired_VIB_EA5348AA.tsv",
    "test_data/expected_output/expected_paired_VIB_EA5348AA.aln",
    "test_data/expected_output/expected_paired_VIB_EA5348AA.fsa",
    "test_data/expected_output/expected_paired_VIB_EA5348AA.frag.gz",
    "test_data/expected_output/expected_paired_VIB_EA5348AA.res",
]


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
@pytest.mark.skipif(
    platform.system() == "Linux", reason="Test not supported on Linux"
)
def setup_teardown_paired_input() -> Generator[list[str], None, None]:
    """
    Pytest fixture that sets up the arguments for the paired input test
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
        "--identity",
        "90",
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
def test_paired_run(
    setup_teardown_paired_input: Generator[list[str], None, None]
) -> None:
    """
    End-to-end test for the main function with paired input
    it runs the main function of pacini_typing with the paired input arguments
    and checks if the output file is successfully created.
    ----------
    Input:
        setup_teardown_paired_input: Generator ->
            Pytest fixture for the paired input test
    ----------
    """
    main(setup_teardown_paired_input)
    assert os.path.exists(f"{RUN_OUTPUT}.tsv")
    assert os.path.exists(f"{RUN_OUTPUT}.fsa")
    assert os.path.exists(f"{RUN_OUTPUT}.res")
    assert os.path.exists(f"{RUN_OUTPUT}.frag.gz")
    assert os.path.exists(f"{RUN_OUTPUT}.aln")
    check_file_contents()


def check_file_contents() -> None:
    """
    Function to check the contents of the output files
    """
    run_output = pd.read_csv(f"{RUN_OUTPUT}.tsv", sep="\t")
    expected_output = pd.read_csv(EXPECTED_FILES[0], sep="\t")

    # Use the equals function of the pandas DataFrame to compare the files
    assert run_output.equals(expected_output)
    compare_additional_files()


def compare_additional_files() -> None:
    """
    Fill in...
    """
    for output_file, expected_file in zip(
        [
            f"{RUN_OUTPUT}.aln",
            f"{RUN_OUTPUT}.fsa",
            f"{RUN_OUTPUT}.frag.gz",
            f"{RUN_OUTPUT}.res",
        ],
        EXPECTED_FILES[1:],
    ):
        assert validating_input_arguments.ArgsValidator.create_sha_hash(
            output_file
        ) == validating_input_arguments.ArgsValidator.create_sha_hash(
            expected_file
        )
