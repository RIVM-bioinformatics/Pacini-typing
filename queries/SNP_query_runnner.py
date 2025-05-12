#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

This module is responsible for running the SNP query against the
reference database. PointFinder is called to run the SNP query,
using the BaseQueryRunner class as a base. The query is prepared
by the PointFinder runner and is then executed by the command invoker.
"""


__author__ = "Mark van de Streek"
__date__ = "2025-05-12"
__all__ = ["SNPQueryRunner"]

from queries.base_query_runner import BaseQueryRunner
from queries.pointfinder_runner import PointFinder


class SNPQueryRunner(BaseQueryRunner):
    """
    Concrete implementation of the QueryRunner class
    for running SNP related queries (PointFinder).

    The class follows a command pattern, since the gene and
    SNP queries are following the same recipe, but only the
    some (small) parts are different.

    *PointFinder's doesn't have a version command,
    so the extract_version_number is a bit different here.
    ----------
    Methods:
        - __init__: Constructor of the SNPQueryRunner class
        - extract_version_number: Method to extract the version number
            from the output of the version command
    ----------
    """

    def __init__(self, run_options: dict[str, str]) -> None:
        super().__init__(run_options)
        self.query = PointFinder.get_query(option=self.run_options)
        self.version_command = PointFinder.get_version_command()
        # TODO remove ?
        # self.log_tool_version()

    def extract_version_number(self, stdout: str) -> str | None:
        """later..."""
        # TODO STILL HAVE TO IMPLEMENT THIS
        return f"{stdout.split(" ")[-1]}"
