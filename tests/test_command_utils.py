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


def test_execute_capture_output():
    result = execute(["echo", "Hello World"], capture=True)
    assert result[0].strip() == "Hello World"
    assert result[1].strip() == ""


def test_execute_no_capture_output():
    result = execute(["echo", "Hello World"], capture=False)
    assert result is True


def test_execute_with_stdout():
    with open("test_stdout.txt", "w", encoding="utf-8") as stdout_f:
        with open("test_stderr.txt", "w", encoding="utf-8") as stderr_f:
            execute(
                ["echo", "Hello World"],
                stdout_file=stdout_f,
                stderr_file=stderr_f,
                capture=False,
            )

    with open("test_stdout.txt", "r", encoding="utf-8") as stdout_f:
        stdout_content = stdout_f.read().strip()

    assert stdout_content == "Hello World"

    os.remove("test_stdout.txt")
    os.remove("test_stderr.txt")


def test_execute_failing_command_allow_fail_false():
    with pytest.raises(subprocess.CalledProcessError):
        execute(["ls", "xyz"], allow_fail=False)


def test_execute_failing_command_allow_fail_true():
    result = execute(["false"], allow_fail=True)
    assert result is None


def test_execute_failing_command():
    with open("test_stderr.txt", "w", encoding="utf-8") as stderr_f:
        with pytest.raises(subprocess.CalledProcessError):
            result = execute(
                ["ls", "xyz"],
                stderr_file=stderr_f,
                allow_fail=False,
            )
    with open("test_stderr.txt", "r", encoding="utf-8") as stderr_f:
        stderr_content = stderr_f.read().strip()
        assert stderr_content == "ls: xyz: No such file or directory"

    os.remove("test_stderr.txt")
