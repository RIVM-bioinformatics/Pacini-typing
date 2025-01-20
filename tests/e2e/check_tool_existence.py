#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Very basic python script to check if the required tools are installed
Based on two functions, this script is checking the existence of the tools.
"""

__author__ = "Mark van de Streek"
__date__ = "2025-01-18"
__all__ = ["check_tools", "is_tool"]

import shutil

import pytest


def check_tools(required_tools: list[str]) -> None:
    """
    Function to check if the required tools are installed
    If the tools are not installed, the test will fail
    KMA and BLASTN are required for a run of Pacini-typing
    ----------
    Input:
        - required_tools: list of tools to check
    Raises:
        - pytest.fail
    ----------
    """
    missing_tools = [tool for tool in required_tools if not is_tool(tool)]
    if missing_tools:
        pytest.fail(
            f"Skipping tests because the following tools are missing: {', '.join(missing_tools)}"
        )


def is_tool(name: str) -> bool:
    """
    Basic function to check if a tool is installed
    It uses the shutil.which() function to check if the tool is in the PATH
    ----------
    Input:
        - name: name of the tool to check
    Output:
        - bool: True if the tool is installed, False otherwise
    ----------
    """
    return shutil.which(name) is not None
