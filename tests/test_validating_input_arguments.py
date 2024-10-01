#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To be filed in later...
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"

import pytest
import validating.validating_input_arguments as v
from unittest.mock import patch
import os
import logging
import yaml
import sys
import re
import sys
import logging
F =


class Args:
    """
    Class that is used to simulate the argparse object.
    """
    def __init__(self, paired):
        self.paired = paired


def test_get_file_extension():
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
    assert v.validate_file_extensions(filename) == expected


@pytest.mark.parametrize("file, expected", [
    ("argument_parser/build_parser.py", True),
    ("argument_parser/build_parser", False),
    ("argument_parser/build_parser.sh", False),
    ("readme", False),
    ("Pacini-typing.py", True),
    ("tests/test_validating_input_arguments.py", True)])
def test_check_file_existence(file, expected):
    assert v.check_file_existence(file) == expected


def test_check_double_files():
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
    args = Args(paired=[args1, args2])

    with pytest.raises(SystemExit) as ex:
        v.check_for_same_name(args)
    assert ex.value.code == 1


@pytest.mark.parametrize("args1, args2", [
    ("README.md", "Pacini-typing.py"),
    ("1234.md", "12345.md"),
    ("Pacini-typing.md", "Pacini-typing.py"),])
def test_check_for_same_name_good(args1, args2):
    args = Args(paired=["README.md", "Pacini-typing.py"])

    try:
        v.check_for_same_name(args)
    except SystemExit:
        pytest.fail("check_for_same_name() raised SystemExit unexpectedly!")


def test_run_file_checks():
    args = Args(paired=["README.md", "Pacini-typing.py"])

    with patch('validating.validating_input_arguments.check_file_existence', return_value=True), \
            patch('validating.validating_input_arguments.validate_file_extensions', return_value=True):
        try:
            v.run_file_checks(args.paired)
        except SystemExit:
            pytest.fail("run_file_checks() raised SystemExit unexpectedly!")

    with patch('validating.validating_input_arguments.check_file_existence', return_value=True), \
            patch('validating.validating_input_arguments.validate_file_extensions', return_value=False):
        with pytest.raises(SystemExit) as ex:
            v.run_file_checks(args.paired)

        assert ex.value.code == 1
