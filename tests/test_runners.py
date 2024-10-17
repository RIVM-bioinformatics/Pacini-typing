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
__data__ = "2024-10-17"
__all__ = ["test"]

import os
import time

import pytest

from run_queries.blast_runner import BLASTn
from run_queries.kma_runner import KMA
from run_queries.query_runner import QueryRunner

OPTION = {
    "database_path": "./refdir/",
    "database_name": "mydb",
    "option": "query",
    "verbose": True,
    "input_file_list": ["1.fq", "2.fq"],
    "run_path": os.path.abspath(__file__).rsplit('.', 1)[0],
    "query": None,
    "file_type": "FASTA",
    "makedatabase": None,
    "query" : {
        "paired": ["/dummy/path", "/dummy/path"],
        "single": "dummy_file.fastq",
        "output": "/dummy/path",
        "filters": {
            "identity": 100,
        }
    }
}

def test_prepare_query():
    """
    Function that tests the prepare_query() function(s) of the enums
    """
    query = KMA.get_query(OPTION)
    assert query == [
        "kma",
        "-ipe",
        "1.fq",
        "2.fq",
        "-ID",
        "100",
        "-tsv",
        "-t_db",
        "./refdir/mydb",
        "-o",
        "/dummy/path",
        "-mrc",
        "0.7",
        "-pm",
        "p",
    ]


def test_get_query_different():
    """
    Function that tests the prepare_query() function(s) of the enums
    """
    SUB_OPTION = OPTION.copy()
    SUB_OPTION["database_name"] = "my_new_db"
    query = KMA.get_query(SUB_OPTION)
    assert query == [
        "kma",
        "-ipe",
        "1.fq",
        "2.fq",
        "-ID",
        "100",
        "-tsv",
        "-t_db",
        "./refdir/my_new_db",
        "-o",
        "/dummy/path",
        "0.7",
        "-pm",
        "p",
    ]


def test_get_query_verbose_false():
    """
    Function that tests the prepare_query() function(s) of the enums with verbose set to False
    """
    SUB_OPTION = OPTION.copy()
    SUB_OPTION["verbose"] = False
    query = KMA.get_query(SUB_OPTION)
    assert query == [
        "kma",
        "-ipe",
        "1.fq",
        "2.fq",
        "-ID",
        "100",
        "-tsv",
        "-t_db",
        "./refdir/mydb",
        "-o",
        "/dummy/path",
        "0.7",
        "-pm",
        "p",
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
        "10",
        "-perc_identity",
        "100",
    ]

def test_blast_get_query_different():
    """
    Function that tests the prepare_query() function(s) of the enums
    """
    SUB_OPTION = OPTION.copy()
    SUB_OPTION["database_name"] = "my_new_db"
    query = BLASTn.get_query(SUB_OPTION)
    assert query == [
        "blastn",
        "-query",
        "1.fq",
        "-db",
        "./refdir/my_new_db",
        "-out",
        "/dummy/path.tsv",
        "-outfmt",
        "10",
        "-perc_identity",
        "100",
    ]

# class QueryRunner:
#     def __init__(self):
#         self.start_time = None
#         self.stop_time = None

#     def start(self):
#         self.start_time = time.time()

#     def stop(self):
#         self.stop_time = time.time()

#     def get_runtime(self):
#         """
#         Simple method that returns the runtime of the query.
#         The function is called in a logging event in the main script (pacini_typing.py).
#         ----------
#         - Output:
#             - float: with the runtime in seconds
#         ----------
#         """
#         logging.debug("Getting the runtime of the query...")
#         return round((self.stop_time - self.start_time), 2)


RUN_TIMES = [
    0.1,
    0.04,
    1.5673,
]

@pytest.mark.parametrize("runtime", RUN_TIMES)
def test_get_runtime(runtime):
    """
    Function that tests the get_runtime() method of the QueryRunner class
    """
    runner = QueryRunner(OPTION)
    runner.start_time = time.time()
    time.sleep(runtime)  # Simulate a query that takes 1 second
    runner.stop_time = time.time()
    runtime = runner.get_runtime()
    assert runtime == runtime

@pytest.mark.parametrize("runtime, expected", [
    (0.1, 0.1),
    (0.04, 0.04),
    (1.2345, 1.24),
    (1.4567, 1.46),
    (1.5673, 1.57),
])
def test_get_runtime_rounding(runtime, expected):
    """
    Function that tests the get_runtime() method of the QueryRunner class for correct rounding
    """
    runner = QueryRunner(OPTION)
    runner.start_time = time.time()
    time.sleep(runtime)  # Simulate a query that takes the specified time
    runner.stop_time = time.time()
    actual_runtime = runner.get_runtime()
    assert actual_runtime == expected