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
"""

__author__ = "Mark van de Streek"
__date__ = "2024-10-07"

from unittest import mock

import pytest

from preprocessing.exceptions.validation_exceptions import (
    FileNotExistsError,
    InvalidFileExtensionError,
    InvalidPairedError,
    ValidationError,
)
from preprocessing.validation.validating_input_arguments import ArgsValidator

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
    ("preprocessing/argsparse/build_parser.py", True),
    ("pacini_typing.py", True),
    ("README.md", True),
]

CHECK_FILE_EXISTENCE_FAIL = [
    ("preprocessing/argsparse/build_parser", False),
    ("preprocessing/argsparse/build_parser.sh", False),
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
    ("mysampleR1R2.fq", "mysampleR2R1.fq"),
    ("mysample_R2R1.fq", "mysample_R1R2.fq"),
    ("mysam_2ple_1_is_great.fq", "mysam_1le_2_is_great.fq"),
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
def test_get_file_extension(file_list: list[str], expected: str) -> None:
    """
    Test the get_file_extension() function.
    This function is responsible for extracting the file extension from
    a list of file name components.
    The test verifies that the function correctly identifies and
    returns the file extension in various scenarios.
    ----------
    Input:
        - file_list: List of file name components
        - expected: Expected file extension
    ----------
    """
    args_obj = ArgsValidator(
        option={"input_file_list": [], "run_path": "./pacini_typing.py"}
    )
    assert args_obj.get_file_extension(file_list) == expected


@pytest.mark.parametrize("filename, expected", VALIDATE_FILE_EXTENSIONS)
def test_validate_file_extensions(filename: str, expected: bool) -> None:
    """
    Parametrized test for the validate_file_extensions() function.
    This function checks if the file extension of
    the given filename is valid based on predefined criteria.
    The test runs multiple times with different filenames to
    ensure the function behaves as expected.
    ----------
    Input:
        - filename: File name to validate
        - expected: Expected result of the validation
    ----------
    """
    args_obj = ArgsValidator(
        option={"input_file_list": [], "run_path": "./pacini_typing.py"}
    )

    if expected is False:
        with pytest.raises(InvalidFileExtensionError):
            args_obj.validate_file_extensions(filename)
    else:
        assert args_obj.validate_file_extensions(filename) == expected


def test_validate_file_extension_fail() -> None:
    """
    Test the validate_file_extensions() function for failure cases.
    This function checks if the file extension of the given filename is valid
    based on predefined criteria. It should raise an InvalidFileExtensionError
    exception if the file extension is not valid. The test verifies that the
    function correctly identifies and handles invalid file extensions.
    """
    v = ArgsValidator(
        option={"input_file_list": [], "run_path": "./pacini_typing.py"}
    )

    with pytest.raises(InvalidFileExtensionError):
        v.validate_file_extensions("not_a_valid_file_extension")
        v.validate_file_extensions("")


@pytest.mark.parametrize("file, expected", CHECK_FILE_EXISTENCE_GOOD)
def test_check_file_existence_good(file: str, expected: bool) -> None:
    """
    Parametrized test for the check_file_existence() function.
    This function verifies whether a given file exists and is a valid file.
    The test runs multiple times with different file paths to ensure the
    function correctly identifies existing and non-existing files.
    ----------
    Input:
        - file: File path to check
        - expected: Expected result of the check
    ----------
    """
    v = ArgsValidator(
        option={"input_file_list": [], "run_path": "./pacini_typing.py"}
    )
    assert v.check_file_existence(file) == expected


@pytest.mark.parametrize("file, expected", CHECK_FILE_EXISTENCE_FAIL)
def test_check_file_existence_fail(file: str, expected: bool) -> None:
    """
    Parametrized test for the check_file_existence() function.
    This function verifies whether a given file not exists
    and is not a valid file.
    Expected is not used but the uses it to accept the parameters.
    ----------
    Input:
        - file: File path to check
        - expected: Expected result of the check
    ----------
    """
    v = ArgsValidator(
        option={"input_file_list": [], "run_path": "./pacini_typing.py"}
    )
    with pytest.raises(FileNotExistsError):
        v.check_file_existence(file)


def test_compare_paired_files() -> None:
    """
    Test the compare_paired_files() function.
    This function checks if the same file is passed twice in the input list.
    It should raise a SystemExit exception if duplicate files are found.
    The test verifies that the function behaves correctly
    for both duplicate and unique file names.
    """
    input_list = ["README.md", "README.md"]
    v = ArgsValidator(
        option={
            "input_file_list": input_list,
            "run_path": "./pacini_typing.py",
        }
    )

    with pytest.raises(InvalidPairedError):
        v.compare_paired_files()

    input_list = ["README.md", "pacini_typing.py"]
    v = ArgsValidator(
        option={
            "input_file_list": input_list,
            "run_path": "./pacini_typing.py",
        }
    )
    try:
        v.compare_paired_files()
    except SystemExit:
        pytest.fail("check_double_files() raised SystemExit unexpectedly!")


@pytest.mark.parametrize("name1, name2", CHECK_FOR_SAME_NAME_FAIL)
def test_check_for_same_name_fail(name1: str, name2: str) -> None:
    """
    Test the check_for_same_name() function for failure cases.
    This function checks if the same file name is
    passed twice in the input list.
    The test verifies that the function correctly identifies
    and handles duplicate file names.
    ----------
    Input:
        - name1: First file name to check
        - name2: Second file name to check
    ----------
    """
    input_list = [name1, name2]
    v = ArgsValidator(
        option={
            "input_file_list": input_list,
            "run_path": "./pacini_typing.py",
        }
    )
    with pytest.raises(InvalidPairedError):
        v.check_for_same_name()


@pytest.mark.parametrize("name1, name2", CHECK_FOR_SAME_NAME_GOOD)
def test_check_for_same_name_good(name1: str, name2: str) -> None:
    """
    Test the check_for_same_name() function for success cases.
    This function checks if the same file name is
    passed twice in the input list.
    ----------
    Input:
        - name1: First file name to check
        - name2: Second file name to check
    ----------
    """
    input_list = [name1, name2]
    v = ArgsValidator(
        option={
            "input_file_list": input_list,
            "run_path": "./pacini_typing.py",
        }
    )

    try:
        v.check_for_same_name()
    except SystemExit:
        pytest.fail("check_for_same_name() raised SystemExit unexpectedly!")


@pytest.mark.parametrize("name1, name2", CHECK_PAIRED_NAMES_GOOD)
def test_check_paired_names_good(name1: str, name2: str) -> None:
    """
    Test the check_paired_names() function for success cases.
    This function checks if the file names in
    the input list are correctly paired.
    ----------
    Input:
        - name1: First file name to check
        - name2: Second file name to check
    ----------
    """
    input_list = [name1, name2]
    v = ArgsValidator(
        option={
            "input_file_list": input_list,
            "run_path": "./pacini_typing.py",
        }
    )

    try:
        v.check_paired_names()
    except SystemExit:
        pytest.fail("check_paired_names() raised SystemExit unexpectedly!")


@pytest.mark.parametrize("name1, name2", CHECK_PAIRED_NAMES_FAIL)
def test_check_paired_names_fail(name1: str, name2: str) -> None:
    """
    Test the check_paired_names() function for failure cases.
    This function checks if the file names in
    the input list are correctly paired.
    ----------
    Input:
        - name1: First file name to check
        - name2: Second file name to check
    ----------
    """
    input_list = [name1, name2]
    v = ArgsValidator(
        option={
            "input_file_list": input_list,
            "run_path": "./pacini_typing.py",
        }
    )

    with pytest.raises(InvalidPairedError):
        v.check_paired_names()


@mock.patch(
    target="preprocessing.validation.validating_input_arguments.ArgsValidator.check_file_existence",
    return_value=False,
)
@mock.patch(
    target="preprocessing.validation.validating_input_arguments.ArgsValidator.validate_file_extensions",
    return_value=False,
)
# pylint: disable=unused-argument
def test_run_file_checks(mock_validate, mock_check) -> None:
    """
    Test the run_file_checks() function.
    It should raise a SystemExit exception if the file extension is not valid
    The Patch decorator is used to mock the return value
    of the called functions. It is not directly used.
    """
    input_list = ["README.md", "pacini_typing.py"]
    v = ArgsValidator(
        option={
            "input_file_list": input_list,
            "run_path": "./pacini_typing.py",
        }
    )

    with pytest.raises(ValidationError):
        for file in input_list:
            v.run_file_checks(file)
