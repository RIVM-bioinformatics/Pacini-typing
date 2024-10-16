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
__all__ = ["test_full_run"]

import os
import platform
import shutil
import subprocess

import pytest

DATABASE_FILES = [
    ("test_full_run/mykma.comp.b"),
    ("test_full_run/mykma.length.b"),
    ("test_full_run/mykma.seq.b"),
    ("test_full_run/mykma.name"),
]


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def test_create_database():
    """
    Method that tests the creation of a database
    """
    if not os.path.exists("test_full_run/"):
        os.mkdir("test_full_run/")
    ARGS = [
        "python3",
        "pacini_typing.py",
        "makedatabase",
        "-i",
        "test_data/vibrio_genes.fasta",
        "-db_type",
        "kma",
        "-db_name",
        "mykma",
        "-db_path",
        "test_full_run/",
    ]
    try:
        subprocess.run(
            ARGS,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Process failed with error: {e}")


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
@pytest.mark.parametrize("file", DATABASE_FILES)
def test_database_creation(file):
    """
    Method that tests the creation of a database
    it simply checks if the database file exists
    """
    if not os.path.isfile(file):
        pytest.fail("Database was not created")


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def test_full_run():
    """
    Method that tests the full run of the Pacini CLI
    """
    ARGS = [
        "python3",
        "pacini_typing.py",
        "-v",
        "query",
        "-p",
        "test_data/ERR976461_1.fastq",
        "test_data/ERR976461_2.fastq",
        "-db_name",
        "mykma",
        "-db_path",
        "test_full_run/",
        "-o",
        "test_full_run/MYRESULTS",
    ]
    subprocess.run(
        ARGS,
        capture_output=True,
        text=True,
        check=True,
    )


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def test_cleanup():
    """
    Method that first removes all files created during the test
    and then removes the directory
    """
    dir_path = "test_full_run/"
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
