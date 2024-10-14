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
__data__ = "2024-09-24"
__all__ = ["QueryRunner"]

import subprocess
import logging
import time

import decorators.decorators
from run_queries.blast_runner import prepare_query as blast_prepare_query
from run_queries.kma_runner import prepare_query as kma_prepare_query


class QueryRunner:
    """
    Main class that runs the input query against the reference database.
    The query is prepared by the prepare_query method from the respective runner.
    """

    def __init__(self, input_file_type, input_file, query_args, filter_args):
        """
        Constructor of the QueryRunner class.
        The constructor calls the prepare_query method based
        on the input type (FASTA/FASTQ).
        ----------
        Input:
            - input_file_type: str
            - input_file: str
            - database_path: str
            - database_name: str
            - output_file: str
        ----------
        """
        self.input_file_type = input_file_type
        self.input_file = input_file
        self.database = query_args.database_path + query_args.database_name
        self.output_file = query_args.output
        self.filter_args = filter_args
        self.start_time = None
        self.stop_time = None

        if self.input_file_type == "FASTA":
            self.query = blast_prepare_query(
                input_file=self.input_file,
                database=self.database,
                output_file=self.output_file,
                filter_args=self.filter_args
            )
        elif self.input_file_type == "FASTQ":
            self.query = kma_prepare_query(
                input_file=self.input_file,
                database=self.database,
                output_file=self.output_file,
                filter_args=self.filter_args
            )

    def __str__(self):
        """
        Readable representation of the class.
        This function is called when the class is printed.
        """
        # TODO: Is this function necessary?
        return f"QueryRunner(query={self.query})"

    @decorators.decorators.log
    def run(self):
        """
        The query is already prepared in the constructor. This function runs the query.
        The runtime is started and stopped to calculate the runtime.
        The decorated log function logs the query command,
            see the ./decorators/decorators.py file for more information.
            This decorator also checks if the query was successful.
        ----------
        Output:
            - Result of the subprocess.run
        ----------
        """
        logging.info("Running query with the following command: %s", self.query)
        self.start_time = time.time()
        result = subprocess.run(
            self.query,
            capture_output=True,
            text=True,
            check=True)
        self.stop_time = time.time()

        # TODO: This return statement is not used anywhere, should it be removed?
        return result

    def get_runtime(self):
        """
        Simple method that returns the runtime of the query.
        The function is called in a logging event in the main script (pacini_typing.py).
        ----------
        - Output:
            - float: with the runtime in seconds
        ----------
        """
        return round((self.stop_time - self.start_time), 2)
