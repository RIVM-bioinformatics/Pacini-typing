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
__data__ = "2024-10-30"
__all__ = [
    "setup_teardown",
    "cleanup_files",
]

import os
import platform
import shutil
from typing import Generator

import pytest

from pacini_typing import main

INPUT_FILE = "test_data/VIB_DA2216AA_AS_1.fna"
DATABASE_PATH = "./refdir/"
DATABASE_NAME = "mydb"

KMA_EXTENSIONS = [
    ".comp.b",
    ".length.b",
    ".name",
    ".seq.b",
]

BLAST_EXTENSIONS = [
    ".ndb",
    ".nhr",
    ".nin",
    ".njs",
    ".not",
    ".nsq",
    ".ntf",
    ".nto",
]


def is_tool(name: str) -> bool:
    """Check whether `name` is on PATH and marked as executable."""
    return shutil.which(name) is not None


@pytest.fixture(scope="module", autouse=True)
def check_tools():
    """Pytest fixture that checks if the required tools are installed"""
    if platform.system() == "Linux":
        pytest.skip("Test not supported on Linux")

    required_tools = ["kma_index", "makeblastdb"]
    missing_tools = [tool for tool in required_tools if not is_tool(tool)]
    if missing_tools:
        pytest.skip(
            f"Skipping tests because the following tools are missing: {', '.join(missing_tools)}"
        )


@pytest.fixture()
def setup_teardown() -> Generator[list[str], None, None]:
    """
    Pytest fixture that sets up the arguments for the single input test
    It creates a Generator object that yields the arguments
    After the test is run, it cleans up the files created during the test
    The generator does not accept or return any arguments

    Test is skipped if the platform is Linux -> GitHub actions
    """
    if platform.system() == "Linux":
        pytest.skip("Test not supported on Linux")

    args = [
        "--verbose",
        "makedatabase",
        "--input",
        INPUT_FILE,
        "--database_path",
        DATABASE_PATH,
        "--database_name",
        DATABASE_NAME,
        "--database_type",
        "kma",
    ]

    dir_path = "test_full_run/"
    os.mkdir(dir_path)

    yield args
    cleanup_files(dir_path)


def cleanup_files(dir_path: str) -> None:
    """
    Fill in later...
    """
    if os.path.exists(dir_path):
        # Remove all files in the directory
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        # Remove the directory itself
        os.rmdir(dir_path)


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def test_make_kma_database(setup_teardown: list[str]) -> None:
    """
    ...
    """
    main(setup_teardown)
    for kma_extension in KMA_EXTENSIONS:
        assert os.path.exists(f"{DATABASE_PATH}{DATABASE_NAME}{kma_extension}")


@pytest.mark.skipif(platform.system() == "Linux", reason="Test not supported on Linux")
def test_make_blast_database(setup_teardown: list[str]) -> None:
    """
    ...
    """
    setup_teardown[-1] = "blast"
    main(setup_teardown)
    for blast_extension in BLAST_EXTENSIONS:
        assert os.path.exists(f"{DATABASE_PATH}{DATABASE_NAME}{blast_extension}")
