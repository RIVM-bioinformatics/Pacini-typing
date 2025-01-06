#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Simpeler test module for the alignment_extractor module.
This module test the extracting of sequences from an alignment file.
This file is created by KMA and therefore always has the same format.

The tests are applied by using a test alignment file that was created
for his purpose. The file contains a three genes and their (shorter) sequences.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-09-24"
__all__ = [
    "test_check_alignment_file_not_found",
    "test_parse_alignment_file",
    "test_parse_alignment_file_single_gene",
    "check_file_output",
]

import os
import platform

import pytest

from parsing.alignment_extractor import AlignmentExtractor
from preprocessing.exceptions.alignment_exceptions import AlignmentFileNotFoundError


def test_check_alignment_file_not_found():
    """
    Function that tests if the AlignmentFileNotFoundError is raised
    when the alignment file is not found.
    """
    with pytest.raises(AlignmentFileNotFoundError):
        AlignmentExtractor("non_existent_file.txt", ["gene1"], "output.fasta")


@pytest.mark.skipif(
    platform.system() == "Linux", reason="Test not supported on Linux"
)
def test_parse_alignment_file():
    """
    Function that tests if the sequences are extracted correctly
    from the alignment file. The real output file is checked
    by the check_file_output function.
    """
    extractor = AlignmentExtractor(
        "test_data/expected_output/example_alignment.aln",
        ["rfbV_O1:1:AE003852", "wbfZ_O139:1:AB012956"],
        "output.fasta",
    )
    extractor.run()
    check_file_output("output.fasta", "rfbV_O1:1:AE003852")

    assert "rfbV_O1:1:AE003852" in extractor.query_sequences
    assert "wbfZ_O139:1:AB012956" in extractor.query_sequences


@pytest.mark.skipif(
    platform.system() == "Linux", reason="Test not supported on Linux"
)
def test_parse_alignment_file_single_gene():
    """
    Function that tests if the sequences are extracted correctly
    from the alignment file when only one gene is given.
    The real output file is checked by the check_file_output function.
    """
    extractor = AlignmentExtractor(
        "test_data/expected_output/example_alignment.aln",
        ["ctxA"],
        "output.fasta",
    )
    extractor.run()
    check_file_output("output.fasta", "ctxA")

    assert "ctxA" in extractor.query_sequences


@pytest.mark.skipif(
    platform.system() == "Linux", reason="Test not supported on Linux"
)
def check_file_output(file: str, gene: str):
    """
    Function that checks if the output file is correct.
    The file should start with the gene name and then the sequence.
    After checking, the file is removed.
    ----------
    Input:
        - file: The path to the output file.
        - gene: The gene name that should be in the
    ----------
    """
    with open(file, "r", encoding="utf-8") as f:
        assert f.readline() == f">{gene}\n"
    os.remove(file)
