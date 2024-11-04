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
__data__ = "2024-11-01"
__all__ = ["test_execute_capture_output", "test_execute_no_capture_output"]

import os
import subprocess
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from command_utils import execute


@pytest.fixture
def temp_files():
    """
    Fixture to create temporary files for stdout and stderr.
    The files are used by a test and removed after the test is done.
    """
    stdout_file = "test_stdout.txt"
    stderr_file = "test_stderr.txt"
    with open(stdout_file, "w", encoding="utf-8") as stdout_f, open(
        stderr_file, "w", encoding="utf-8"
    ) as stderr_f:
        yield stdout_f, stderr_f
    os.remove(stdout_file)
    os.remove(stderr_file)


def test_execute_capture_output():
    """
    Test the execute function with capturing the output
    The output is placed in a tuple with stdout and stderr,
    no files are used in this operation.
    """
    result = execute(["echo", "Hello World"], capture=True)
    assert isinstance(result, tuple), "Expected a tuple but got a boolean"
    assert result[0].strip() == "Hello World"
    assert result[1].strip() == ""


def test_execute_no_capture_output():
    """
    Test the execute function without capturing the output.
    """
    result = execute(["echo", "Hello World"], capture=False)
    assert result is True


def test_execute_with_stdout(temp_files):
    """
    Test the execute function with capturing the output to a file.
    The fixture creates temporary files for stdout and stderr.
    """
    stdout_f, stderr_f = temp_files
    execute(
        ["echo", "Hello World"],
        stdout_file=stdout_f,
        stderr_file=stderr_f,
        capture=False,
    )

    with open("test_stdout.txt", "r", encoding="utf-8") as stdout_f:
        stdout_content = stdout_f.read().strip()

    assert stdout_content == "Hello World"


def test_execute_failing_command_allow_fail_false():
    """
    Test the execute function with a failing command.
    The function makes sure that the command fails and raises an exception.
    """
    with pytest.raises(subprocess.CalledProcessError):
        execute(["ls", "xyz"], allow_fail=False)


def test_execute_failing_command_allow_fail_true():
    """
    Test the execute function with a failing command
    and allow_fail=True.
    """
    result = execute(["false"], allow_fail=True)
    assert result is False


def pytest_capture_error_file(temp_files):
    """
    Test the execute function with a failing command
    and capturing the output in a file.
    """
    stdout_f, stderr_f = temp_files
    with pytest.raises(subprocess.CalledProcessError):
        execute(
            ["ls", "xyz"],
            stdout_file=stdout_f,
            stderr_file=stderr_f,
            allow_fail=False,
        )

    with open("test_stderr.txt", "r", encoding="utf-8") as stderr_f:
        stderr_content = stderr_f.read().strip()
        assert stderr_content == "ls: xyz: No such file or directory"
