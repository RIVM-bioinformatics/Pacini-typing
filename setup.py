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
__all__ = ["get_version"]

from setuptools import find_packages, setup

from command_utils import execute


def get_version() -> str:
    """
    Get the version of the package from git tags.
    If there are no tags, return "0.0.0".
    """
    result = execute(["git", "describe", "--tags"], capture=True)
    if isinstance(result, tuple):
        return result[0].strip().split("-")[0]
    return "0.0.0"


setup(
    name="pacini_typing",
    version=get_version(),
    packages=find_packages(),
    py_modules=["pacini_typing"],
    entry_points={
        "console_scripts": [
            "pacini_typing = pacini_typing:main",
        ],
    },
)
