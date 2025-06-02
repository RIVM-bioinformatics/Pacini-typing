#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Enum class to store all PointFinder-related options and flags.
This class is used to create the right query for the PointFinder and
return the command to retrieve the version number.

The get_query() method prepares the query for the PointFinder run
and returns it to the (main) SNPQueryRunner class.
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
    DATABASE_PATH_OPTION: option for the database path
    DATABASE_SUBDIR_OPTION: option for the database subdirectory
    ----------
    """

    DATABASE_PATH_OPTION = "--databasePath"
    # PointFinder requires the database path and a species.
    # The 'species' is actually the subdirname of the specific
    # database that is used. The could therfore be a bit misleading.
    DATABASE_SUBDIR_OPTION = "--species"

    @staticmethod
    def get_query(option: dict[str, str]) -> list[str]:
        """
        Getter method that combines the options and input
        variables of the user into a query that could be
        executed in PointFinder. The query is executed
        using the custom command invoker.
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
            option["pointfinder_script_path"],
            "--inputfiles",
            *option["input_file_list"],
            "--out_path",
            option["run_output_snps"],
            PointFinder.DATABASE_PATH_OPTION.value,
            option["path_snps"],
            PointFinder.DATABASE_SUBDIR_OPTION.value,
            option["species"],
            "--method",
            option["method"],
            "--method_path",
            option["method_path"],
        ]

    @staticmethod
    def get_version_command() -> list[str]:
        """
        Method that returns the version command for KMA.
        The PointFinder script doesn't have a version command,
        so the version number is extracted from a request.

        *The logging of the version number is a wish of the RIVM
        team, but is not a big requirement for Pacini-typing.
        ----------
        Output:
            - list with the version command
        ----------
        """
        return [
            "curl",
            "-s",
            # Request to the PointFinder API and retrieve the commit dates
            "https://api.bitbucket.org/2.0/repositories/genomicepidemiology/pointfinder/filehistory/master/PointFinder.py?fields=values.commit.date",
        ]
