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

from unittest.mock import patch
import pytest
import validating.validating_input_arguments as v


class Args:
    """
    Class that is used to simulate the argparse object.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, paired):
        self.paired = paired


def test_get_file_extension():
    """
    Test the get_file_extension() function from the validating_input_arguments.py module
    The function gets the valid file extension from a configuration file
    """
    assert v.get_file_extension(["myfile", "txt"]) == ".txt"
    assert v.get_file_extension(["myfile", "txt", "gz"]) == ".txt.gz"
    assert v.get_file_extension(["myfile", "txt", "gz", "tar"]) == ".gz.tar"
    assert not v.get_file_extension(["myfile"]) == ".txt"
    assert v.get_file_extension(["myfile"]) == ".myfile"


@pytest.mark.parametrize("filename, expected", [
    ("myfile.txt", False),
    ("myfile.txt.gz", False),
    ("myfile.txt.tar", False),
    ("myfile", False),
    ("myfile.txt.tar.gz", True),
    ("myfile.txt.gz.tar", False),
    ("myfile.tar.gz", True),
    ("myfile.FASTA", True),
    ("myfile.FASTQ.fq", False),
    ("myfile.fastq", True),
    ("myfile.fq", True),
    ("myfile.FasTA", True),
    ("myfile.fasta", True)])
def test_validate_file_extensions(filename, expected):
    """
    Parametrized test for the validate_file_extensions() function
    The function gets runs every time with different parameters
    """
    assert v.validate_file_extensions(filename) == expected


@pytest.mark.parametrize("file, expected", [
    ("argument_parser/build_parser.py", True),
    ("argument_parser/build_parser", False),
    ("argument_parser/build_parser.sh", False),
    ("readme", False),
    ("Pacini-typing.py", True),
    ("tests/test_validating_input_arguments.py", True)])
def test_check_file_existence(file, expected):
    """
    Parametrized test for the check_file_existence() function
    The function gets runs every time with different parameters
    """
    assert v.check_file_existence(file) == expected


def test_check_double_files():
    """
    Test the check_double_files() function
    It should raise a SystemExit exception if the same file is passed twice
    not identical names should pass without raising any exceptions
    """
    args = Args(paired=["README.md", "README.md"])

    with pytest.raises(SystemExit) as ex:
        v.check_double_files(args)

    assert ex.value.code == 1

    args = Args(paired=["README.md", "Pacini-typing.py"])
    try:
        v.check_double_files(args)
    except SystemExit:
        pytest.fail("check_double_files() raised SystemExit unexpectedly!")


@pytest.mark.parametrize("args1, args2", [
    ("README.md", "README.md"),
    ("1234.md", "1234.md"),
    ("Pacini-typing.py", "Pacini-typing.py"),])
def test_check_for_same_name_fail(args1, args2):
    """
    Test the check_for_same_name() function
    It should raise a SystemExit exception if the same file is passed twice
    """
    args = Args(paired=[args1, args2])

    with pytest.raises(SystemExit) as ex:
        v.check_for_same_name(args)
    assert ex.value.code == 1


@pytest.mark.parametrize("args1, args2", [
    ("README.md", "Pacini-typing.py"),
    ("1234.md", "12345.md"),
    ("Pacini-typing.md", "Pacini-typing.py"),])
def test_check_for_same_name_good(args1, args2):
    """
    Test the check_for_same_name() function.
    Function should not raise any exceptions
    """
    args = Args(paired=[args1, args2])

    try:
        v.check_for_same_name(args)
    except SystemExit:
        pytest.fail("check_for_same_name() raised SystemExit unexpectedly!")


def test_run_file_checks():
    """
    Test the run_file_checks() function
    It should raise a SystemExit exception if the file extension is not valid
    The Patch decorator is used to mock the return value of the called functions
    """
    args = Args(paired=["README.md", "Pacini-typing.py"])

    with patch('validating.validating_input_arguments.check_file_existence',
               return_value=True), \
            patch('validating.validating_input_arguments.validate_file_extensions',
                  return_value=True):
        try:
            v.run_file_checks(args.paired)
        except SystemExit:
            pytest.fail("run_file_checks() raised SystemExit unexpectedly!")

    with patch('validating.validating_input_arguments.check_file_existence',
               return_value=True), \
            patch('validating.validating_input_arguments.validate_file_extensions',
                  return_value=False):
        with pytest.raises(SystemExit) as ex:
            v.run_file_checks(args.paired)

        assert ex.value.code == 1
