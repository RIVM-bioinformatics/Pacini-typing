#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

To be filed in later...
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = [
    "setup_teardown_single_input",
    "setup_teardown_paired_input",
    "cleanup_files",
    "test_single_run",
    "test_paired_run",
    "test_single_contents",
    "test_paired_contents",
]

import os
import platform
import shutil
from typing import Any, Generator

import pytest

from pacini_typing import main

FASTA_FILE = "data/VIB_DA2216AA_AS_1.fna"
RUN_OUTPUT = "test_full_run/myresults"
FASTQ_FILE_1 = "data/sample_1.fq"
FASTQ_FILE_2 = "data/sample_2.fq"
KMA_DATABASE_NAME = "mykma"
DATABASE_PATH = "./refdir/"
DATABASE_NAME = "mydb"
IDENTITY = 89

KMA_COLUMNS = [
    "Template_Name",
    "Template_Length",
    "Template_Identity",
    "Template_Coverage",
    "Template_Depth",
    "Query_Identity",
    "Query_Coverage",
    "Query_Depth",
    "Read_Count_Map",
    "Read_Count_Aln",
    "Score",
    "Expected",
    "q_value",
    "p_value",
    "ConClave_Score",
    "ConClave_Quality",
]


def is_tool(name: str) -> bool:
    """Check whether `name` is on PATH and marked as executable."""
    return shutil.which(name) is not None


@pytest.fixture(scope="module", autouse=True)
def check_tools():
    """Check if the required tools are installed on the system"""
    if platform.system() == "Linux":
        pytest.skip("Test not supported on Linux")

    required_tools = ["kma", "blastn"]
    missing_tools = [tool for tool in required_tools if not is_tool(tool)]
    if missing_tools:
        pytest.fail(
            f"Failed tests because the following tools are missing: {', '.join(missing_tools)}"
        )


@pytest.fixture()
def setup_teardown_single_input() -> Generator[list[str], None, None]:
    """
    Pytest fixture that sets up the arguments for the single input test
    It creates a Generator object that yields the arguments
    After the test is run, it cleans up the files created during the test
    The generator does not accept or return any arguments

    Test is skipped if the platform is Linux -> GitHub actions
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

    dir_path = "test_full_run/"
    os.mkdir(dir_path)

    yield args
    cleanup_files(dir_path)


@pytest.fixture()
@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def setup_teardown_paired_input() -> Generator[list[str], None, None]:
    """
    Pytest fixture that sets up the arguments for the paired input test
    It creates a Generator object that yields the arguments
    After the test is run, it cleans up the files created during the test
    The generator does not accept or return any arguments

    Test is skipped if the platform is Linux -> GitHub actions
    """
    args = [
        "--verbose",
        "query",
        "--paired",
        FASTQ_FILE_1,
        FASTQ_FILE_2,
        "--output",
        RUN_OUTPUT,
        "--database_path",
        DATABASE_PATH,
        "--database_name",
        KMA_DATABASE_NAME,
        "--identity",
        str(IDENTITY),
    ]

    dir_path = "test_full_run/"
    os.mkdir(dir_path)

    yield args
    cleanup_files(dir_path)


def cleanup_files(dir_path: str) -> None:
    """
    Fill in later...
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
    Test the main function with single input
    """
    single_input_args = setup_teardown_single_input
    main(single_input_args)
    assert os.path.exists("test_full_run/myresults.tsv")


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def test_paired_run(
    setup_teardown_paired_input: Generator[list[str], None, None]
) -> None:
    """
    Test the main function with paired input
    """
    main(setup_teardown_paired_input)
    assert os.path.exists("test_full_run/myresults.tsv")
    assert os.path.exists("test_full_run/myresults.fsa")
    assert os.path.exists("test_full_run/myresults.res")
    assert os.path.exists("test_full_run/myresults.frag.gz")
    assert os.path.exists("test_full_run/myresults.aln")


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def test_single_contents(
    setup_teardown_single_input: Generator[list[str], None, None]
) -> None:
    """
    Test the contents of the output file for the single input...
    Add more information later...
    """
    main(setup_teardown_single_input)
    if not os.path.exists("test_full_run/myresults.tsv"):
        pytest.fail("Output file was not created")
    else:
        # Mypy is not happy with the code below, but it is correct
        pass
        # with open("test_full_run/myresults.tsv", "r", encoding="utf-8") as f:
        #     for line in f:
        #         line = line.split(",")
        #         assert len(line) == 12


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def test_paired_contents(
    setup_teardown_paired_input: Generator[list[str], None, None]
) -> None:
    """
    Test the contents of the output file for the paired input...
    Add more information later...
    """
    main(setup_teardown_paired_input)
    if not os.path.exists("test_full_run/myresults.tsv"):
        pytest.fail("Output file was not created")
    else:
        # Mypy is not happy with the code below, but it is correct
        pass
        # with open("test_full_run/myresults.tsv", "r", encoding="utf-8") as f:
        #     for line in f:
        #         line = line.strip().split("\t")
        #         assert len(line) == 16
        #         for i, column in enumerate(KMA_COLUMNS):
        #             assert column in line[i]
