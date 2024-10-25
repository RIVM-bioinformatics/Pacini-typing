#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

This script contains the tests for the validating_input_arguments.py module.
The tests are used to check the functions that validate the input arguments.
Both good and bad cases are tested to ensure the functions work as expected.

Parametrized tests are used to test the functions with different input parameters

For example:

@pytest.mark.parametrize("filename, expected", [
    ("myfile.txt", False),
    ("myfile.txt.gz", False),
    ("myfile.fasta", True)])
def my_good_unit_test(filename, expected):
    assert my_function(filename) == expected

The above code will run the my_good_unit_test *3* times with the given parameters,
this is the same as running:
    assert my_function("myfile.txt") == False
    assert my_function("myfile.txt.gz") == False
    assert my_function("myfile.fasta") == True

Good: The function should return the expected value
Bad: The function should raise an exception or return a different value
"""

__author__ = "Mark Van de Streek"
__date__ = "2024-10-07"

from unittest.mock import patch

import pytest

from exceptions.validation_exceptions import (
    FileNotExistsError,
    InvalidFileExtensionError,
    InvalidPairedError,
)
from validation.validating_input_arguments import ArgsValidator

GET_FILE_EXTENSIONS = [
    (["myfile", "txt"], ".txt"),
    (["myfile", "txt", "gz"], ".txt.gz"),
    (["myfile", "txt", "gz", "tar"], ".gz.tar"),
    (["myfile"], ".myfile"),
]

VALIDATE_FILE_EXTENSIONS = [
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
    ("myfile.fasta", True),
]

CHECK_FILE_EXISTENCE_GOOD = [
    ("argsparse/build_parser.py", True),
    ("pacini_typing.py", True),
    ("README.md", True),
]

CHECK_FILE_EXISTENCE_FAIL = [
    ("argsparse/build_parser", False),
    ("argsparse/build_parser.sh", False),
    ("readme", False),
]

CHECK_FOR_SAME_NAME_FAIL = [
    ("README.md", "README.md"),
    ("1234.md", "1234.md"),
    ("pacini_typing.py", "pacini_typing.py"),
]

CHECK_FOR_SAME_NAME_GOOD = [
    ("README.md", "pacini_typing.py"),
    ("1234.md", "12345.md"),
    ("Pacini-typing.md", "pacini_typing.py"),
]

CHECK_PAIRED_NAMES_GOOD = [
    ("mysample_1.fq", "mysample_2.fq"),
    ("mysample_R1.fq", "mysample_R2.fq"),
    ("mysample_R1_is_great.fq", "mysample_R2_is_great.fq"),
    ("mysample_1_is_great.fq", "mysample_2_is_great.fq"),
    ("mysampleR1.fq", "mysampleR2.fq"),
]

CHECK_PAIRED_NAMES_FAIL = [
    ("mysample1.fq", "mysampl2.fq"),
    ("mysample_R1.fq", "mysample_R1.fq"),
    ("mysample_R1_is_great.fq", "mysample_R1_is_great.fq"),
    ("mysample_2_is_great.fq", "mysample_1_is_great.fq"),
    ("_1Sample.fq", "_2Sample.fq"),
    ("R1Sample.fq", "R2Sample.fq"),
    ("Sample.R1", "Sample.R2"),
    ("mysampleR1.fq", "mysampleR1.fq"),
]


@pytest.mark.parametrize("file_list, expected", GET_FILE_EXTENSIONS)
def test_get_file_extension(file_list, expected):
    """
    Test the get_file_extension() function from the validating_input_arguments.py module.
    This function is responsible for extracting the file extension from
    a list of file name components.
    The test verifies that the function correctly identifies and
    returns the file extension in various scenarios.
    """
    v = ArgsValidator(option={"input_file_list": [], "run_path": "./pacini_typing.py"})
    assert v.get_file_extension(file_list) == expected


@pytest.mark.parametrize("filename, expected", VALIDATE_FILE_EXTENSIONS)
def test_validate_file_extensions(filename, expected):
    """
    Parametrized test for the validate_file_extensions() function.
    This function checks if the file extension of
    the given filename is valid based on predefined criteria.
    The test runs multiple times with different filenames to
    ensure the function behaves as expected.
    """
    v = ArgsValidator(option={"input_file_list": [], "run_path": "./pacini_typing.py"})

    if expected is False:
        with pytest.raises(InvalidFileExtensionError) as ex:
            v.validate_file_extensions(filename)
    else:
        assert v.validate_file_extensions(filename) == expected


@pytest.mark.parametrize("file, expected", CHECK_FILE_EXISTENCE_GOOD)
def test_check_file_existence_good(file, expected):
    """
    Parametrized test for the check_file_existence() function.
    This function verifies whether a given file exists and is a valid file.
    The test runs multiple times with different file paths to ensure the
    function correctly identifies existing and non-existing files.
    """
    v = ArgsValidator(option={"input_file_list": [], "run_path": "./pacini_typing.py"})
    assert v.check_file_existence(file) == expected


@pytest.mark.parametrize("file, expected", CHECK_FILE_EXISTENCE_FAIL)
def test_check_file_existence_fail(file, expected):
    """
    Parametrized test for the check_file_existence() function.
    This function verifies whether a given file not exists
    and is not a valid file.
    """
    v = ArgsValidator(option={"input_file_list": [], "run_path": "./pacini_typing.py"})
    with pytest.raises(FileNotExistsError) as ex:
        v.check_file_existence(file)


def test_compare_paired_files():
    """
    Test the compare_paired_files() function.
    This function checks if the same file is passed twice in the input list.
    It should raise a SystemExit exception if duplicate files are found.
    The test verifies that the function behaves correctly
    for both duplicate and unique file names.
    """
    input_list = ["README.md", "README.md"]
    v = ArgsValidator(
        option={"input_file_list": input_list, "run_path": "./pacini_typing.py"}
    )

    with pytest.raises(InvalidPairedError) as ex:
        v.compare_paired_files()

    input_list = ["README.md", "pacini_typing.py"]
    v = ArgsValidator(
        option={"input_file_list": input_list, "run_path": "./pacini_typing.py"}
    )
    try:
        v.compare_paired_files()
    except SystemExit:
        pytest.fail("check_double_files() raised SystemExit unexpectedly!")


@pytest.mark.parametrize("args1, args2", CHECK_FOR_SAME_NAME_FAIL)
def test_check_for_same_name_fail(args1, args2):
    """
    Test the check_for_same_name() function for failure cases.
    This function checks if the same file name is passed twice in the input list.
    It should raise a SystemExit exception if duplicate file names are found.
    The test verifies that the function correctly identifies
    and handles duplicate file names.
    """
    input_list = [args1, args2]
    v = ArgsValidator(
        option={"input_file_list": input_list, "run_path": "./pacini_typing.py"}
    )
    with pytest.raises(InvalidPairedError) as ex:
        v.check_for_same_name()


@pytest.mark.parametrize("args1, args2", CHECK_FOR_SAME_NAME_GOOD)
def test_check_for_same_name_good(args1, args2):
    """
    Test the check_for_same_name() function for success cases.
    This function checks if the same file name is passed twice in the input list.
    It should not raise any exceptions if the file names are unique.
    The test verifies that the function behaves correctly for unique file names.
    """
    input_list = [args1, args2]
    v = ArgsValidator(
        option={"input_file_list": input_list, "run_path": "./pacini_typing.py"}
    )

    try:
        v.check_for_same_name()
    except SystemExit:
        pytest.fail("check_for_same_name() raised SystemExit unexpectedly!")


@pytest.mark.parametrize("args1, args2", CHECK_PAIRED_NAMES_GOOD)
def test_check_paired_names_good(args1, args2):
    """
    Test the check_paired_names() function for success cases.
    This function checks if the file names in the input list are correctly paired.
    It should not raise any exceptions if the file names are paired correctly.
    The test verifies that the function behaves correctly for valid paired file names.
    """
    input_list = [args1, args2]
    v = ArgsValidator(
        option={"input_file_list": input_list, "run_path": "./pacini_typing.py"}
    )

    try:
        v.check_paired_names()
    except SystemExit:
        pytest.fail("check_paired_names() raised SystemExit unexpectedly!")


@pytest.mark.parametrize("args1, args2", CHECK_PAIRED_NAMES_FAIL)
def test_check_paired_names_fail(args1, args2):
    """
    Test the check_paired_names() function for failure cases.
    This function checks if the file names in the input list are correctly paired.
    It should raise a SystemExit exception if the file names are not paired correctly.
    The test verifies that the function correctly identifies and handles unpaired file names.
    """
    input_list = [args1, args2]
    v = ArgsValidator(
        option={"input_file_list": input_list, "run_path": "./pacini_typing.py"}
    )

    with pytest.raises(InvalidPairedError) as ex:
        v.check_paired_names()


def test_run_file_checks():
    """
    Test the run_file_checks() function
    It should raise a SystemExit exception if the file extension is not valid
    The Patch decorator is used to mock the return value of the called functions
    """
    input_list = ["README.md", "pacini_typing.py"]
    v = ArgsValidator(
        option={"input_file_list": input_list, "run_path": "./pacini_typing.py"}
    )

    with patch(
        "validation.validating_input_arguments.ArgsValidator.check_file_existence",
        return_value=True,
    ), patch(
        "validation.validating_input_arguments."
        "ArgsValidator.validate_file_extensions",
        return_value=True,
    ):
        try:
            v.run_file_checks(input_list)
        except SystemExit:
            pytest.fail("run_file_checks() raised SystemExit unexpectedly!")

    with patch(
        "validation.validating_input_arguments.ArgsValidator.check_file_existence",
        return_value=True,
    ), patch(
        "validation.validating_input_arguments."
        "ArgsValidator.validate_file_extensions",
        return_value=False,
    ):
        with pytest.raises(SystemExit) as ex:
            v.run_file_checks(input_list)

        assert ex.value.code == 1
