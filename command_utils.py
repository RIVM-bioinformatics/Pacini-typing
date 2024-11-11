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
from pathlib import Path
from typing import Tuple

# TODO: Implement a design pattern for the execute function


def execute(
    cmd: list[str] | str,
    directory: Path = Path.cwd(),
    capture: bool = False,
    stdout_file: str | None = None,
    stderr_file: str | None = None,
    allow_fail: bool = False,
) -> Tuple[str, str] | bool:
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
    ----------
    """
    try:
        logging.info("running command: %s", " ".join(cmd))
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

        if capture:
            return result.stdout, result.stderr
        return result.returncode == 0

    except subprocess.CalledProcessError as e:
        logging.error(
            "Command failed with return code %d:\n%s\n%s",
            e.returncode,
            e.cmd,
            e.stderr,
        )
        if not allow_fail:
            raise
        return False
