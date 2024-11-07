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
    "fasta_options",
    "fastq_options",
    "test_create_database_file_list_fasta",
    "test_create_database_file_list_fastq",
    "test_check_for_database_existence",
    "test_check_for_database_existence_missing_file",
    "test_check_for_database_path_valid",
    "test_check_for_database_path_invalid",
]


import platform
from unittest import mock

import pytest

from validation.validate_database import (
    check_for_database_existence,
    check_for_database_path,
    create_database_file_list,
)


@pytest.fixture
def fasta_options():
    """
    Fixture that returns a dictionary of options for FASTA files.
    """
    return {
        "database_path": "./refdir/",
        "database_name": "mydb",
        "file_type": "FASTA",
    }


@pytest.fixture
def fastq_options():
    """
    Fixture that returns a dictionary of options for FASTQ files.
    """
    return {
        "database_path": "./refdir/",
        "database_name": "mykma",
        "file_type": "FASTQ",
    }


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def test_create_database_file_list_fasta(fasta_options):
    """
    Test that the function returns the correct list of database files for FASTA files.
    """
    expected_files = [
        "mydb.ndb",
        "mydb.nhr",
        "mydb.nin",
        "mydb.njs",
        "mydb.not",
        "mydb.nsq",
        "mydb.ntf",
        "mydb.nto",
    ]
    assert create_database_file_list(fasta_options) == expected_files


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def test_create_database_file_list_fastq(fastq_options):
    """
    Test that the function returns the correct list of database files for FASTQ files.
    """
    expected_files = [
        "mykma.comp.b",
        "mykma.length.b",
        "mykma.name",
        "mykma.seq.b",
    ]
    assert create_database_file_list(fastq_options) == expected_files


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
@mock.patch("os.path.exists", return_value=True)
def test_check_for_database_existence(options):
    """
    Test that the function returns True when the database files are present.
    """
    assert check_for_database_existence(options) is True


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
@mock.patch("os.path.exists")
def test_check_for_database_existence_missing_file(mock_exists, fasta_options):
    """
    Test that the function raises a SystemExit when the database files are missing.
    """

    def mock_exists_side_effect(path):
        if path == "./refdir/mydb.ndb":
            return False
        return True

    mock_exists.side_effect = mock_exists_side_effect

    assert check_for_database_existence(fasta_options) is False


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
@mock.patch("os.path.exists", return_value=True)
def test_check_for_database_path_valid(fasta_options):
    """
    Test that the function returns True when the database path is valid.
    """
    assert check_for_database_path(fasta_options) is True


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
@mock.patch("os.path.exists", return_value=False)
def test_check_for_database_path_invalid(fasta_options):
    """
    Test that the function raises a SystemExit when the database path is invalid.
    """
    assert check_for_database_path(fasta_options) is False


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
@mock.patch("os.path.exists", return_value=True)
def test_check_for_database_path_append_slash(mock, fasta_options):
    """
    Test that the function appends a slash to the database path if it does not end with one.
    """
    fasta_options["database_path"] = "./refdir"
    assert check_for_database_path(fasta_options) is True
    assert fasta_options["database_path"] == "./refdir/"
