#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Test module for the command_utils module.
This module tests the execute function from the command_utils module.

The pytest fixture temp_files is used to
create temporary files for stdout and stderr.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-11-01"
__all__ = [
    "test_execute_capture_output",
    "test_execute_no_capture_output",
    "test_execute_with_stdout",
    "test_execute_failing_command_allow_fail_false",
    "test_execute_failing_command_allow_fail_true",
    "test_capture_error_file",
]

import os
from typing import Generator, TextIO, Tuple

import pytest

from command_utils import CommandInvoker, ShellCommand
from preprocessing.exceptions.command_utils_exceptions import SubprocessError


@pytest.fixture
def temp_files() -> Generator[Tuple[TextIO, TextIO], None, None]:
    """
    Fixture to create temporary files for stdout and stderr.
    The files are used by a test and removed after the test is done.
    ----------
    Output:
        - stdout_f: temporary file for stdout
        - stderr_f: temporary file for stderr
    ----------
    """
    stdout_file = "test_stdout.txt"
    stderr_file = "test_stderr.txt"
    with open(stdout_file, "w", encoding="utf-8") as stdout_f, open(
        stderr_file, "w", encoding="utf-8"
    ) as stderr_f:
        yield stdout_f, stderr_f
    os.remove(stdout_file)
    os.remove(stderr_file)


def test_execute_capture_output() -> None:
    """
    Test the execute function with capturing the output
    The output is placed in a tuple with stdout and stderr,
    no files are used in this operation.
    """
    cmd = ShellCommand(cmd=["echo", "Hello World"], capture=True)
    result = CommandInvoker(cmd).execute()
    assert isinstance(result, tuple), "Expected a tuple but got a boolean"
    assert result[0].strip() == "Hello World"
    assert result[1].strip() == ""


def test_execute_no_capture_output() -> None:
    """
    Test the execute function without capturing the output.
    """
    result = CommandInvoker(
        ShellCommand(cmd=["echo", "Hello World"], capture=False)
    ).execute()

    assert result is True


def test_execute_with_stdout(temp_files: tuple[TextIO, TextIO]) -> None:
    """
    Test the execute function with capturing the output to a file.
    The fixture creates temporary files for stdout and stderr.
    ----------
    Input:
        - temp_files: temporary files for stdout and stderr
    ----------
    """
    stdout_f, stderr_f = temp_files
    CommandInvoker(
        ShellCommand(
            cmd=["echo", "Hello World"],
            capture=False,
            stdout_file=stdout_f,
            stderr_file=stderr_f,
        )
    ).execute()

    with open("test_stdout.txt", "r", encoding="utf-8") as stdout_f:
        stdout_content = stdout_f.read().strip()

    assert stdout_content == "Hello World"


def test_execute_failing_command_allow_fail_false() -> None:
    """
    Test the execute function with a failing command.
    The function makes sure that the command fails and raises an exception.
    """
    with pytest.raises(SubprocessError):
        CommandInvoker(
            ShellCommand(cmd=["ls", "xyz"], allow_fail=False)
        ).execute()


def test_execute_failing_command_allow_fail_true() -> None:
    """
    Test the execute function with a failing command
    and allow_fail=True.
    """
    result = CommandInvoker(
        ShellCommand(cmd=["false"], allow_fail=True)
    ).execute()
    assert result is False


def test_capture_error_file(temp_files: tuple[TextIO, TextIO]) -> None:
    """
    Test the execute function with a failing command
    and capturing the output in a file.
    ----------
    Input:
        - temp_files: temporary files for stdout and stderr
    ----------
    """
    stdout_f, stderr_f = temp_files
    with pytest.raises(SubprocessError):
        CommandInvoker(
            ShellCommand(
                cmd=["ls", "xyz"],
                stdout_file=stdout_f,
                stderr_file=stderr_f,
                allow_fail=False,
            )
        ).execute()

    with open("test_stderr.txt", "r", encoding="utf-8") as stderr_f:
        stderr_content = stderr_f.read().strip()
        assert stderr_content == "ls: xyz: No such file or directory"
