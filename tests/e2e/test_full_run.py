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
__all__ = ["setup_teardown_single_input", "setup_teardown_paired_input"]

import os
import platform
import shutil
from typing import Generator

import pytest

from pacini_typing import main

sequence = "data/VIB_DA2216AA_AS_1.fna"
output = "test_full_run/myresults"
paired_file1 = "test_data/ERR976461_1.fastq"
paired_file2 = "test_data/ERR976461_2.fastq"
KMA_db_name = "mykma"
db_path = "./refdir/"
db_name = "mydb"
identity = 89


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
        sequence,
        "--output",
        output,
        "--database_path",
        db_path,
        "--database_name",
        db_name,
        "--identity",
        str(identity),
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
        paired_file1,
        paired_file2,
        "--output",
        output,
        "--database_path",
        db_path,
        "--database_name",
        KMA_db_name,
        "--identity",
        str(identity),
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
def test_app(setup_teardown_single_input: list[str]) -> None:
    """
    Test the main function...
    Add more information later...
    """
    main(setup_teardown_single_input)
    assert os.path.exists("test_full_run/myresults.tsv")


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def test_paired_run(setup_teardown_paired_input: list[str]) -> None:
    """
    Test the main function with paired input...
    Add more information later...
    """
    main(setup_teardown_paired_input)
    assert os.path.exists("test_full_run/myresults.tsv")
    assert os.path.exists("test_full_run/myresults.fsa")
    assert os.path.exists("test_full_run/myresults.res")
    assert os.path.exists("test_full_run/myresults.frag.gz")
    assert os.path.exists("test_full_run/myresults.aln")









# ------------------- OLD TESTS -------------------

# @pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
# def test_create_database():
#     """
#     Method that tests the creation of a database
#     """
#     if not os.path.exists("test_full_run/"):
#         os.mkdir("test_full_run/")
#     ARGS = [
#         "python3",
#         "pacini_typing.py",
#         "makedatabase",
#         "-i",
#         "test_data/vibrio_genes.fasta",
#         "-db_type",
#         "kma",
#         "-db_name",
#         "mykma",
#         "-db_path",
#         "test_full_run/",
#     ]
#     try:
#         subprocess.run(
#             ARGS,
#             capture_output=True,
#             text=True,
#             check=True,
#         )
#     except subprocess.CalledProcessError as e:
#         pytest.fail(f"Process failed with error: {e}")


# @pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
# @pytest.mark.parametrize("file", DATABASE_FILES)
# def test_database_creation(file):
#     """
#     Method that tests the creation of a database
#     it simply checks if the database file exists
#     """
#     if not os.path.isfile(file):
#         pytest.fail("Database was not created")


# @pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
# def test_full_run():
#     """
#     Method that tests the full run of the Pacini CLI
#     """
#     ARGS = [
#         "python3",
#         "pacini_typing.py",
#         "-v",
#         "query",
#         "-p",
#         "test_data/ERR976461_1.fastq",
#         "test_data/ERR976461_2.fastq",
#         "-db_name",
#         "mykma",
#         "-db_path",
#         "test_full_run/",
#         "-o",
#         "test_full_run/MYRESULTS",
#     ]
#     subprocess.run(
#         ARGS,
#         capture_output=True,
#         text=True,
#         check=True,
#     )

# @pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
# def test_full_run_output():
#     """
#     Method that tests the output of the full run of the Pacini CLI
#     """
#     found = False
#     if not os.path.isfile("test_full_run/MYRESULTS.tsv"):
#         pytest.fail("Output file was not created")

#     with open("test_full_run/MYRESULTS.tsv", "r", encoding="utf-8") as f:
#         lines = f.readlines()
#         if not len(lines) > 1:
#             pytest.fail("Output file does not have the correct number of lines")
#         for line in lines:
#             if "rfbV_O1" in line:
#                 found = True
#     if not found:
#         pytest.fail("Output file does not contain the expected sequence")


# @pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
# def test_cleanup():
#     """
#     Method that first removes all files created during the test
#     and then removes the directory
#     """
#     dir_path = "test_full_run/"
#     if os.path.exists(dir_path):
#         # Remove all files in the directory
#         for file_name in os.listdir(dir_path):
#             file_path = os.path.join(dir_path, file_name)
#             if os.path.isfile(file_path):
#                 os.remove(file_path)
#             elif os.path.isdir(file_path):
#                 shutil.rmtree(file_path)
#         # Remove the directory itself
#         os.rmdir(dir_path)
