#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

This file contains tests for the query_runner module.
These tests are responsible for testing the query_runner module.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-10-17"
__all__ = [
    "test_prepare_query",
    "test_get_query_different",
    "test_get_query_verbose_false",
    "test_blast_prepare_query",
    "test_blast_get_query_different",
    "test_get_runtime",
]

import os
import time
from typing import Any, Dict
from unittest import mock

import pytest

from queries.blast_runner import BLASTn
from queries.kma_runner import KMA
from queries.query_runner import QueryRunner

skip_in_ci = pytest.mark.skipif(
    os.getenv("CI") == "true",
    reason="Test online (GitHub Action) not available due to dependencies",
)

RUN_TIMES = [
    0.1,
    0.04,
    1.5673,
    1.4567,
    1.2345,
    0.01,
]


@pytest.fixture()
def setup_query_input() -> Dict[str, Any]:
    """
    Pytest fixture that sets up the input options for the query test.
    ----------
    Output:
        - Dict: Dictionary of test configuration options
    ----------
    """
    return {
        "database_path": "./refdir/",
        "database_name": "mydb",
        "option": "query",
        "verbose": True,
        "input_file_list": ["1.fq", "2.fq"],
        "run_path": os.path.abspath(__file__).rsplit(".", 1)[0],
        "file_type": "FASTA",
        "output": "./dummy/path",
        "makedatabase": None,
        "query": {
            "paired": ["/dummy/path", "/dummy/path"],
            "single": "dummy_file.fastq",
        },
        "threads": 6,
    }


def test_prepare_query(setup_query_input: Dict[str, Any]) -> None:
    """
    Function that tests the prepare_query() function(s) of the enums
    ----------
    Input:
        - setup_query_input: Dictionary of test configuration options
    ----------
    """
    query: list[str] = KMA.get_query(setup_query_input)
    assert query == [
        "kma",
        "-ipe",
        "1.fq",
        "2.fq",
        "-t_db",
        "./refdir/mydb",
        "-o",
        "./dummy/path",
        "-t",
        "6",
    ]


def test_get_query_different(setup_query_input: Dict[str, Any]) -> None:
    """
    Function that tests the prepare_query() function(s) of the enums.
    It uses a different database name by simply copying the
    OPTION dictionary and changing the database name
    ----------
    Input:
        - setup_query_input: Dictionary of test configuration options
    ----------
    """
    sub_option = setup_query_input.copy()
    sub_option["database_name"] = "my_new_db"
    query: list[str] = KMA.get_query(sub_option)
    assert query == [
        "kma",
        "-ipe",
        "1.fq",
        "2.fq",
        "-t_db",
        "./refdir/my_new_db",
        "-o",
        "./dummy/path",
        "-t",
        "6",
    ]


def test_get_query_verbose_false(setup_query_input: Dict[str, Any]) -> None:
    """
    Function that tests the prepare_query() function(s) of the
    enums with verbose set to False
    ----------
    Input:
        - setup_query_input: Dictionary of test configuration options
    ----------
    """
    sub_option = setup_query_input.copy()
    sub_option["verbose"] = False
    query = KMA.get_query(sub_option)
    assert query == [
        "kma",
        "-ipe",
        "1.fq",
        "2.fq",
        "-t_db",
        "./refdir/mydb",
        "-o",
        "./dummy/path",
        "-t",
        "6",
    ]


def test_blast_prepare_query(setup_query_input: Dict[str, Any]) -> None:
    """
    Function that tests the prepare_query() function(s) of the enums
    ----------
    Input:
        - setup_query_input: Dictionary of test configuration options
    ----------
    """
    query = BLASTn.get_query(setup_query_input)
    assert query == [
        "blastn",
        "-query",
        "1.fq",
        "-db",
        "./refdir/mydb",
        "-out",
        "./dummy/path.tsv",
        "-outfmt",
        f"'6 {" ".join(BLASTn.FORMATS.value)}'",
        "-num_threads",
        "6",
    ]


def test_blast_get_query_different(setup_query_input: Dict[str, Any]) -> None:
    """
    Function that tests the prepare_query() function(s) of the enums
    ----------
    Input:
        - setup_query_input: Dictionary of test configuration options
    ----------
    """
    sub_option = setup_query_input.copy()
    sub_option["database_name"] = "my_new_db"
    query = BLASTn.get_query(sub_option)
    assert query == [
        "blastn",
        "-query",
        "1.fq",
        "-db",
        "./refdir/my_new_db",
        "-out",
        "./dummy/path.tsv",
        "-outfmt",
        f"'6 {" ".join(BLASTn.FORMATS.value)}'",
        "-num_threads",
        "6",
    ]


@skip_in_ci
@mock.patch("os.path.exists", return_value=False)
@mock.patch("os.makedirs")
@pytest.mark.parametrize("runtime", RUN_TIMES)
def test_get_runtime(
    mock, mock1, runtime: float, setup_query_input: Dict[str, Any]
) -> None:
    """
    Function that tests the get_runtime() method of the QueryRunner class.
    Certain mocks are used to simulate the runtime of the test.
    ----------
    Input:
        - mock: mock object for os.path.exists
        - mock1: mock object for os.makedirs
        - runtime: runtime to test
        - setup_query_input: Dictionary of test configuration options
    ----------
    """
    runner = QueryRunner(setup_query_input)
    runner.start_time = time.time()
    time.sleep(runtime)
    runner.stop_time = time.time()

    assert runner.get_runtime() == pytest.approx(runtime, 1)
