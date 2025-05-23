#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Simple module that holds the running methods for the gene and SNP queries.
The functions of this module are reused in multiple modules, including tests.

The run_gene_query and run_snp_query functions are both calling the
run_query function, only with a different class. The run_query function
then initializes the class and executes the run method. Finally, the
runtime is logged.

*Main reason for placing them separate was the circular import issue if placing
them in main PaciniTyping class.
"""

__author__ = "Mark van de Streek"
__date__ = "2025-05-07"
__all__ = ["run_query", "run_gene_query", "run_snp_query"]

import logging
from typing import Any, Type

from queries.gene_query_runner import GeneQueryRunner
from queries.snp_query_runnner import SNPQueryRunner


def run_query(
    query_runner_class: Type[Any], query_runner_builder: dict[str, Any]
) -> None:
    """
    Generic function to run a query using a specified QueryRunner class.
    The incoming class could either be the GeneQueryRunner or SNPQueryRunner.
    Both classes are following the same interface, so they could be combined
    in this function.
    The incoming class is initialized and the run method is called.
    After the run method is called, the runtime is logged.
    ----------
    Input:
        - query_runner_class: The QueryRunner class to instantiate and run.
        - query_runner_builder: Dictionary with all necessary information.
    ----------
    """
    logging.info("Starting the query running related options...")
    runner = query_runner_class(query_runner_builder)
    runner.run()
    logging.info(
        "Command raised no errors, runtime: %s seconds",
        runner.get_runtime(),
    )


def run_gene_query(query_runner_builder: dict[str, Any]) -> None:
    """
    Function to run the gene query using the GeneQueryRunner class
    ----------
    Input:
        - query_runner_builder: Dictionary with all necessary information.
    ----------
    """
    run_query(GeneQueryRunner, query_runner_builder)


def run_snp_query(query_runner_builder: dict[str, Any]) -> None:
    """
    Runs the SNP query using the SNPQueryRunner class.
    ----------
    Input:
        - query_runner_builder: Dictionary with all necessary information.
    ----------
    """
    run_query(SNPQueryRunner, query_runner_builder)
