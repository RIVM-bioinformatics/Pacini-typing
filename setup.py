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

__author__ = "Mark van de Streek"
__date__ = "2024-11-01"
__all__ = ["get_version"]

import platform

from setuptools import find_packages, setup

from command_utils import CommandInvoker, ShellCommand


def get_version() -> str:
    """
    Get the version of the package from git tags.
    If there are no tags, return "0.0.0".
    """
    # skip this function if the platform is Linux,
    # because of the GitHub Actions workflow
    if platform.system() == "Linux":
        return "0.0.0"

    result = CommandInvoker(
        ShellCommand(["git", "describe", "--tags"], capture=True)
    ).execute()
    if isinstance(result, tuple):
        return result[0].strip().split("-")[0]
    return "0.0.0"


setup(
    name="pacini_typing",
    version=get_version(),
    author="Mark van de Streek",
    author_email="ids-bioinformatics@rivm.nl",
    packages=find_packages(),
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    py_modules=["pacini_typing", "makedatabase", "command_utils"],
    entry_points={
        "console_scripts": [
            "pacini_typing = pacini_typing:main",
            "Pacini-typing = pacini_typing:main",
        ],
    },
)
