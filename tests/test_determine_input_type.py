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
__all__ = ["test_get_file_type"]

import platform

import pytest

from validation.determine_input_type import FileValidator


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def test_get_file_type():
    """
    Test the retrieve_body() function from the determine_input_type.py module
    The function retrieves the body of the input file

    Self.body is a dictionary with the input files as keys and the body of the file as values:
    {
        file1: [line1, line2, line3, line4, line5],
        file2: [line1, line2, line3, line4, line5]
    }
    """
    file_validator = FileValidator(["test_data/VIB_AA2784AA_AS.scaffold.fasta"])
    paired_validator = FileValidator(
        ["test_data/ERR976461_1.fastq", "test_data/ERR976461_2.fastq"]
    )
    assert file_validator.get_file_type() == "FASTA"
    assert paired_validator.get_file_type() == "FASTQ"
