#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

TODO: Add exact description of the PointFinder class
"""

__author__ = "Mark van de Streek"
__date__ = "2025-04-30"
__all__ = ["PointFinder"]

from enum import Enum


class PointFinder(Enum):
    """
    Class to prepare the right query for PointFinder run.
    The class holds the options and prepares the right command
    to be executed in PointFinder.
    The options could be changed for future versions.
    ----------
    RUN_OPTION: string that is used in the command invoker
    DATABASE_PATH_OPTION: option for the database path
    DATABASE_SUBDIR_OPTION: option for the database subdirectory
    UNKNOWN_MUT_OPTION: option for the unknown mutations
        (outputs the unknown mutations)
    ----------
    """

    RUN_OPTION = "pointfinder.py"
    DATABASE_PATH_OPTION = "--databasePath"
    # PointFinder requires the database path and a species.
    # The 'species' is actually the subdirname of the specific
    # database that is used. The could therfore be a bit misleading.
    DATABASE_SUBDIR_OPTION = "--species"
    UNKNOWN_MUT_OPTION = "--unknown_mut"

    @staticmethod
    def get_query(option: dict[str, str]) -> list[str]:
        """
        Getter method that combines the options and input
        variables of the user in a list to be
        called in the other modules.
        ----------
        Input:
            - dictionary with the input files,
                database, and output file
        Output:
            - list with the query to run PointFinder
        ----------
        """
        return [
            "python",
            PointFinder.RUN_OPTION.value,
            "--inputfiles",
            *option["input_file_list"],
            "--out_path",
            (
                option["SNP_output_dir"]
                if option["SNP_output_dir"].endswith("/")
                else option["SNP_output_dir"] + "/"
            ),
            PointFinder.DATABASE_PATH_OPTION.value,
            option["SNP_database_path"],
            PointFinder.DATABASE_SUBDIR_OPTION.value,
            option["species"],
            "--method",
            option["method"],
            "--method_path",
            option["method_path"],
            PointFinder.UNKNOWN_MUT_OPTION.value,
            #
            # Expected:
            # PointFinder.py
            #   -i test.fsa - (test_1.fastq test_2.fastq)
            #   -o /path/to/output-dir/ - Dir should exist
            #   -p /path/to/db/ - Path to database
            #   -s escherichia_coli - Species name - Database dir name
            #   -m blastn - kma/blastn
            #   -m_p /path/to/blastn - Path to blastn or kma
            #   --unknown_mut
            #
        ]

    @staticmethod
    def get_version_command() -> list[str]:
        """
        Method that returns the version command for PointFinder.
        This command could then directly be used in the
        CommandInvoker class to retrieve the version of PointFinder.
        ----------
        Output:
            - list with the version command
        ----------
        """
        return ["python", PointFinder.RUN_OPTION.value, "--version"]
