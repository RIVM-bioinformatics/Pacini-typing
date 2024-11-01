#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

The main goal of this file is providing utils for executing shell commands in Python.
Debugging and logging are easier with this way of executing shell commands.

See docstring for more explicit information about functions and their parameters.
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-11-01"
__all__ = ["execute"]

import logging
import subprocess
import sys
import time
from pathlib import Path

from executor import ExternalCommand, ExternalCommandFailed


def execute(
    cmd,
    directory=Path.cwd(),
    capture=False,
    stdout_file=None,
    stderr_file=None,
    allow_fail=False,
):
    """
    This function executes a shell command in the specified directory.
    The command is executed using the subprocess.run function.
    The output of the command can be captured and returned.
    ----------
    Input:
        - cmd: list of strings, the command to be executed
        - directory: Path, the directory in which to execute the command
        - capture: bool, whether to capture the output of the command
        - stdout_file: Path, the file to which to write the standard output
        - stderr_file: Path, the file to which to write the standard error
        - allow_fail: bool, whether to allow the command to fail

    Output:
        - If capture is True, a tuple of strings containing the standard output and standard error
        - If capture is False, a bool indicating whether the command was successful

    Raises:
        - subprocess.CalledProcessError: if the command fails and allow_fail is False

    Example:
        - execute(["ls", "-l"], directory="/tmp", capture=True)
    ----------
    """
    import subprocess


import logging
from pathlib import Path


def execute(
    cmd,
    directory=Path.cwd(),
    capture=False,
    stdout_file=None,
    stderr_file=None,
    allow_fail=False,
):
    """
    Executes a shell command in a specified directory with optional capturing of output.
    ----------
    Input:
        - cmd: list of strings or str, the command to be executed
        - directory: Path, the directory in which to execute the command
        - capture: bool, whether to capture the output of the command
        - stdout_file: Path, file to write standard output
        - stderr_file: Path, file to write standard error
        - allow_fail: bool, whether to allow command failures without exception

    Output:
        - tuple of (stdout, stderr) if capture is True
        - bool indicating success if capture is False
    """
    try:
        result = subprocess.run(
            " ".join(cmd) if isinstance(cmd, list) else cmd,
            shell=True,
            cwd=directory,
            stdout=(
                stdout_file if stdout_file else (subprocess.PIPE if capture else None)
            ),
            stderr=(
                stderr_file if stderr_file else (subprocess.PIPE if capture else None)
            ),
            text=True,
            check=True,
        )

        # Return captured output if requested
        if capture:
            return result.stdout, result.stderr
        return result.returncode == 0

    except subprocess.CalledProcessError as e:
        if not allow_fail:
            raise
        return None
