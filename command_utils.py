#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Wrapper module for executing shell commands in a specified directory.
The main goal of this module is to provide a simple
interface for running shell commands and capturing their output for
further processing.

For this purpose, the module is using the command design pattern.
This is done in the folowing classes:
    - Command: Interface for all concrete commands
    - ShellCommand: Concrete implementation of a shell command
    - CommandInvoker: Invoker class that is responsible for executing a command

Example:
        >>> from command_utils import CommandInvoker, ShellCommand
        >>> stdout, stderr = CommandInvoker(ShellCommand(
                ["ls", "-l", "my_directory"],
                capture=True,
                    )).execute()

Or capture output in a file:

        >>> with open ("output.txt", "w") as f:
                with open ("error.txt", "w") as e:
                    CommandInvoker(ShellCommand(
                        ["ls", "-l", "my_directory"],
                        stdout_file=f,
                        stderr_file=e,
                    )).execute()
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-11-01"
__all__ = ["ShellCommand", "CommandInvoker", "Command"]

import logging
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple

from preprocessing.exceptions.command_utils_exceptions import SubprocessError


class Command(ABC):
    """
    Class to define the command interface,
    which is the base class for all concrete commands.
    This class could very well being extended to include
    more functionality like undo, redo, etc.
    ----------
    Methods:
        - execute: Abstract method to execute the command
    ----------
    """

    @abstractmethod
    def execute(self) -> Tuple[str, str] | bool:
        """
        Abstract method for executing a command
        The output of this command is either a tuple of stdout and stderr
        or a boolean indicating success or
        failure if the capture flag is False.
        ----------
        Output:
            - tuple of (stdout, stderr) if capture is True
            - bool indicating success if capture is False
        ----------
        """


class ShellCommand(Command):
    """
    Concrete implementation of a shell command
    as a subclass of the Command interface.
    This class holds all necessary information for
    running a shell command without depending on
    other classes or modules.
    ----------
    Methods:
        - execute: implementation of the execute method
            for shell commands
    ----------
    """

    def __init__(
        self,
        cmd: list[str] | str,
        directory: Path = Path.cwd(),
        capture: bool = False,
        stdout_file: str | None = None,
        stderr_file: str | None = None,
        allow_fail: bool = False,
    ) -> None:
        """
        Constructor of the ShellCommand class
        where all incoming parameters are stored as attributes.
        ----------
        Input:
            - cmd: list of strings or str, the command to be executed
            - directory: Path, the directory in which to execute the command
            - capture: bool, whether to capture the output of the command
            - stdout_file: Path, file to write standard output
            - stderr_file: Path, file to write standard error
            - allow_fail: bool, whether to allow command failures without exception
        ----------
        """
        self.cmd = cmd
        self.directory = directory
        self.capture = capture
        self.stdout_file = stdout_file
        self.stderr_file = stderr_file
        self.allow_fail = allow_fail

    def execute(self) -> Tuple[str, str] | bool:
        """
        Executes a shell command in a specified directory with
        optional capturing of output.
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
        Raises:
            - SubprocessError: if the command fails and allow_fail is False
        ----------
        """
        try:
            logging.info("running command: '%s'", " ".join(self.cmd))
            result = subprocess.run(
                " ".join(self.cmd) if isinstance(self.cmd, list) else self.cmd,
                shell=True,
                cwd=self.directory,
                stdout=(
                    self.stdout_file
                    if self.stdout_file
                    else (subprocess.PIPE if self.capture else None)
                ),
                stderr=(
                    self.stderr_file
                    if self.stderr_file
                    else (subprocess.PIPE if self.capture else None)
                ),
                text=True,
                check=True,
            )

            if self.capture:
                return result.stdout, result.stderr
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            logging.error(
                "Command failed with return code %d:\n%s\n%s",
                e.returncode,
                e.cmd,
                e.stderr,
            )
            if not self.allow_fail:
                raise SubprocessError(e.stderr) from e
            return False


class CommandInvoker:
    """
    Invoker class that is repsponsible for executing a command
    This could be any implementation of the Command interface.
    But in this case, it is a ShellCommand.
    ----------
    Methods:
        - execute: Executes the command
    ----------
    """

    def __init__(self, command: Command) -> None:
        """
        Constructor of the CommandInvoker class
        ----------
        Input:
            - command: Command, the command to be executed
        ----------
        """
        self.command = command

    def execute(self) -> Tuple[str, str] | bool:
        """
        Method that starts the execution of the command
        ----------
        Output:
            - tuple of (stdout, stderr) if capture is True
            - bool indicating success if capture is False
        ----------
        """
        return self.command.execute()
