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
__all__ = ["BlastRunner"]

import sys
import os
import subprocess
import time
from run_queries.query_runner import QueryRunner


class BlastRunner(QueryRunner):
    """
    Fill in later...
    """
    RUN_OPTION = "blastn"
    OUTPUT_FORMAT = "10"

    def __init__(self, input_file, database, output_file):
        """
        Fill in later...
        """
        self.input_file = input_file
        self.database = database
        self.output_file = output_file
        super().__init__(
            self.prepare_query(self))

    def run(self):
        """
        Fill in later...
        """
        self.run_query()

    @staticmethod
    def prepare_query(self):
        """
        Simple class method that prepares the query for the BLAST run.
        This query is passed to the super class QueryRunner.

        blastn -query VIB_AA7903AA_AS.result.fasta -db blastdb/vibrio_genes_database -out myresults.csv -outfmt
        """
        return [
            self.RUN_OPTION,
            "-query", self.input_file,
            "-db", self.database,
            "-out", self.output_file,
            "-outfmt", self.OUTPUT_FORMAT
        ]
