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
__all__ = ["KMARunner"]

from run_queries.query_runner import QueryRunner


class KMARunner(QueryRunner):
    """
    Fill in later...
    """
    RUN_OPTION = "kma"
    PAIRED_OPTION = "-ipe"
    OUTPUT_FORMAT = "still to be determined..."

    def __init__(self, input_file, database, output_file):
        """
        Fill in later...
        """
        self.input_file = input_file
        self.database = database
        self.output_file = output_file
        super().__init__(
            query=self.prepare_query()
        )

    def run(self):
        """
        Fill in later...
        """
        self.run_query()

    def prepare_query(self):
        """
        Simple class method that prepares the query for the KMA run.
        This query is passed to the super class QueryRunner
        """
        return [
            self.RUN_OPTION,
            self.PAIRED_OPTION, self.input_file[0], self.input_file[1],
            "-t_db", self.database,
            "-o", self.output_file,
        ]
