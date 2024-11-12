#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

This file contains tests for the query_runner module.
These tests are repsponsible for testing the query_runner module.

The tests are divided into the following functions:
- test_prepare_query
- test_get_query_different
- test_get_query_verbose_false
- test_blast_prepare_query
- test_blast_get_query_different
- test_get_runtime

The OPTION dictionary is a mock dictionary that is used in the tests.
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-10-17"
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

import pytest

from queries.blast_runner import BLASTn
from queries.kma_runner import KMA
from queries.query_runner import QueryRunner

OPTION: Dict[str, Any] = {
    "database_path": "./refdir/",
    "database_name": "mydb",
    "option": "query",
    "verbose": True,
    "input_file_list": ["1.fq", "2.fq"],
    "run_path": os.path.abspath(__file__).rsplit(".", 1)[0],
    "file_type": "FASTA",
    "output": "/dummy/path",
    "makedatabase": None,
    "query": {
        "paired": ["/dummy/path", "/dummy/path"],
        "single": "dummy_file.fastq",
        "filters": {
            "identity": 100,
        },
    },
}

RUN_TIMES = [
    0.1,
    0.04,
    1.5673,
    1.4567,
    1.2345,
    0.01,
]


def test_prepare_query() -> None:
    """
    Function that tests the prepare_query() function(s) of the enums
    """
    query: list[str] = KMA.get_query(OPTION)
    assert query == [
        "kma",
        "-ipe",
        "1.fq",
        "2.fq",
        "-tsv",
        "-t_db",
        "./refdir/mydb",
        "-o",
        "/dummy/path",
    ]


def test_get_query_different() -> None:
    """
    Function that tests the prepare_query() function(s) of the enums
    It uses a different database name by simply copying the
    OPTION dictionary and changing the database name
    """
    sub_option = OPTION.copy()
    sub_option["database_name"] = "my_new_db"
    query: list[str] = KMA.get_query(sub_option)
    assert query == [
        "kma",
        "-ipe",
        "1.fq",
        "2.fq",
        "-tsv",
        "-t_db",
        "./refdir/my_new_db",
        "-o",
        "/dummy/path",
    ]


def test_get_query_verbose_false():
    """
    Function that tests the prepare_query() function(s) of the enums with verbose set to False
    """
    sub_option = OPTION.copy()
    sub_option["verbose"] = False
    query = KMA.get_query(sub_option)
    assert query == [
        "kma",
        "-ipe",
        "1.fq",
        "2.fq",
        "-tsv",
        "-t_db",
        "./refdir/mydb",
        "-o",
        "/dummy/path",
    ]


def test_blast_prepare_query():
    """
    Function that tests the prepare_query() function(s) of the enums
    """
    query = BLASTn.get_query(OPTION)
    assert query == [
        "blastn",
        "-query",
        "1.fq",
        "-db",
        "./refdir/mydb",
        "-out",
        "/dummy/path.tsv",
        "-outfmt",
        "6",
    ]


def test_blast_get_query_different():
    """
    Function that tests the prepare_query() function(s) of the enums
    """
    sub_option = OPTION.copy()
    sub_option["database_name"] = "my_new_db"
    query = BLASTn.get_query(sub_option)
    assert query == [
        "blastn",
        "-query",
        "1.fq",
        "-db",
        "./refdir/my_new_db",
        "-out",
        "/dummy/path.tsv",
        "-outfmt",
        "6",
    ]


@pytest.mark.parametrize("runtime", RUN_TIMES)
def test_get_runtime(runtime: float):
    """
    Function that tests the get_runtime() method of the QueryRunner class
    """
    runner = QueryRunner(OPTION)
    runner.start_time = time.time()
    time.sleep(runtime)
    runner.stop_time = time.time()

    assert runner.get_runtime() == pytest.approx(runtime, 1)
