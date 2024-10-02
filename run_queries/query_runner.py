#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

To be filed in later...

blastn -query VIB_AA7903AA_AS.result.fasta -db blastdb/vibrio_genes_database -out myresults.csv -outfmt

kma -ipe corrected_VIB_AA7903AA_AS/VIB_AA7903AA1.fq corrected_VIB_AA7903AA_AS/VIB_AA7903AA2.fq -t_db kmadb/kma_vibrio_database -o VIB_AA7903AA_AS_KMA
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["QueryRunner"]

import sys
import os
import subprocess
import logging
import time

import decorators.decorators


class QueryRunner:
    """
    Fill in later...
    """

    def __init__(self, query):
        """
        Fill in later...
        """
        self.query = query
        self.start_time = None
        self.stop_time = None

    def __str__(self):
        """
        Readable representation of the class.
        This function is called when the class is printed.
        """
        return f"QueryRunner(query={self.query})"

    @decorators.decorators.log
    def run_query(self):
        """
        Fill in later...
        """
        logging.info("Running query with the following command: %s", self.query)
        self.start_time = time.time()
        result = subprocess.run(
            self.query,
            capture_output=True,
            text=True)
        self.stop_time = time.time()

        return result

    def get_runtime(self):
        """
        Fill in later...
        """
        return self.stop_time - self.start_time
