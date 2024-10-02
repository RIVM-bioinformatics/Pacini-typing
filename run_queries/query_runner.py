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
    Fill in later...
    """

    def __init__(self, input_file_type, input_file, database, output_file):
        """
        Fill in later...
        """
        self.input_file_type = input_file_type
        self.input_file = input_file
        self.database = database
        self.output_file = output_file
        self.start_time = None
        self.stop_time = None

        if self.input_file_type == "FASTA":
            self.query = blast_prepare_query(
                input_file=self.input_file,
                database=self.database,
                output_file=self.output_file
            )
        elif self.input_file_type == "FASTQ":
            self.query = kma_prepare_query(
                input_file=self.input_file,
                database=self.database,
                output_file=self.output_file
            )

    def __str__(self):
        """
        Readable representation of the class.
        This function is called when the class is printed.
        """
        return f"QueryRunner(query={self.query})"

    @decorators.decorators.log
    def run(self):
        """
        Fill in later...
        """
        logging.info("Running query with the following command: %s", self.query)
        self.start_time = time.time()
        result = subprocess.run(
            self.query,
            capture_output=True,
            text=True,
            check=True)
        self.stop_time = time.time()

        return result

    def get_runtime(self):
        """
        Fill in later...
        """
        return self.stop_time - self.start_time
