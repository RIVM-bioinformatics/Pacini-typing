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
__all__ = ["test_help_format"]

import subprocess

import pytest

SUB_ARGUMENTS = [
    ("makedatabase"),
    ("query"),
]

WRONG_SUB_ARGUMENTS = [
    ("make_database"),
    ("querying"),
]


def test_help_format():
    """
    Fill in later...
    """
    assert (
        subprocess.run(
            ["python3", "pacini_typing.py", "--help"],
            capture_output=True,
            text=True,
            check=True,
        ).returncode
        == 0
    )

    assert (
        subprocess.run(
            ["python3", "pacini_typing.py", "-h"],
            capture_output=True,
            text=True,
            check=True,
        ).returncode
        == 0
    )


@pytest.mark.parametrize("subarg", SUB_ARGUMENTS)
def test_sub_help_format(subarg: str):
    """
    Fill in later...
    """
    assert (
        subprocess.run(
            ["python3", "pacini_typing.py", subarg, "--help"],
            capture_output=True,
            text=True,
            check=True,
        ).returncode
        == 0
    )


@pytest.mark.parametrize("wrong_subarg", WRONG_SUB_ARGUMENTS)
def test_sub_page_not_found(wrong_subarg):
    """
    Test that the commands return an exit status code of 2.
    """
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        subprocess.run(
            ["python3", "pacini_typing.py", wrong_subarg, "-h"],
            capture_output=True,
            text=True,
            check=True,
        )
    assert excinfo.value.returncode == 2
