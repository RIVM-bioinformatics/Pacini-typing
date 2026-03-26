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

import json
import logging
import os
import shutil
import tempfile
import time
from pathlib import Path

from command_utils import CommandInvoker, ShellCommand
from queries.base_query_runner import BaseQueryRunner
from queries.pointfinder_runner import PointFinder


class SNPQueryRunner(BaseQueryRunner):
    """
    Concrete implementation of the QueryRunner class
    for running SNP related queries (PointFinder).

    The class follows a command pattern, since the gene and
    SNP queries are following the same recipe, but only the
    some (small) parts are different.
    ----------
    Methods:
        - __init__: Constructor of the SNPQueryRunner class
        - extract_version_number: Method to extract the version number
            from the output of the version command
    ----------
    """

    def __init__(self, run_options: dict[str, str]) -> None:
        """
        Constructor class of the SNPQueryRunner class.
        This class is responsible for initializing the class.
        The checking of the PointFinder existence is additionally
        to the BaseQueryRunner abstract class and is only required
        for the SNP-related operations.

        In addition to the GeneQueryRunner, this class also has
        a method to download the PointFinder script.
        ----------
        Input:
            - run_options: dictionary with the input files,
                database, and output file
        ----------
        """
        super().__init__(run_options)
        self.check_pointfinder_existence(self.run_options["pointfinder_script_path"])
        self.query = PointFinder.get_query(option=self.run_options)
        self.version_command = PointFinder.get_version_command()
        self.log_tool_version()

    def extract_version_number(self, stdout: str) -> str | None:
        """
        Function that extracts the version number
        of the incoming PointFinder output.
        PointFinder doesn't have a version command,
        so the version number is extracted from a request
        to the version history of the PointFinder API.
        ----------
        Input:
            - stdout: the output of the version command (json structure)
        Output:
            - str: the version number of the tool or
                Not available if the version number couldn't be extracted
        ----------
        """
        try:
            data = json.loads(stdout)
            return data["values"][0]["commit"]["date"]
        except Exception:
            logging.error("Error extracting version number from PointFinder, returning 'Not available'...")
            # The program should not crash if a version number could not
            # be extracted, but the error should be logged.
            return "Not available"

    def check_pointfinder_existence(self, path: str) -> None:
        """
        Function that checks if the PointFinder script exists
        and downloads if not present.
        Because the script is not available via Conda/PIP, this
        check is required to download the script.
        ----------
        Input:
            - path: Path to the PointFinder script
        ----------
        """
        if not os.path.isfile(path):
            logging.info("PointFinder script not found, downloading...")
            CommandInvoker(
                ShellCommand(
                    cmd=[
                        "wget",
                        "-O",
                        path,
                        "https://bitbucket.org/genomicepidemiology/pointfinder/raw/master/PointFinder.py",
                    ],
                    capture=True,
                )
            ).execute()
        else:
            logging.debug("PointFinder script already exists, skipping download...")

    # ? The two methods below are a fix for that we are using a single-ended KMA process within PointFinder.py
    @staticmethod
    def _replace_inputfiles_args(query: list[str], input_files: list[str]) -> list[str]:
        """Replace values passed to --inputfiles with a new list of files."""
        if "--inputfiles" not in query:
            return query
        start = query.index("--inputfiles") + 1
        stop = start
        while stop < len(query) and not query[stop].startswith("-"):  # ? break at next CLI flag (either -[something] or --[something])
            stop += 1
        return query[:start] + input_files + query[stop:]

    @staticmethod
    def _merge_input_files(input_files: list[str], output_file: str) -> str:
        """Concatenate input files into a single temporary file for PointFinder/KMA compatibility."""
        with open(output_file, "wb") as out_handle:
            for input_file in input_files:
                with open(input_file, "rb") as in_handle:
                    shutil.copyfileobj(in_handle, out_handle)
        return output_file

    def run(self) -> None:
        """
        Override ABC's run() to create temporary symlinks/copies for
        input files before invoking PointFinder. This circumvents issues
        with filenames containing spaces in PointFinder.py, which is an
        external script/dependency.
        """
        tmp_dir = None
        symlink_map: dict[str, str] = {}
        try:
            # ? make tempdir in run output if possible
            out_dir = self.run_options.get("run_output_snps") or tempfile.gettempdir()
            tmp_dir = tempfile.mkdtemp(prefix="pf_input_", dir=out_dir if os.path.isdir(out_dir) else None)
            # ? make symlinks (or copies on fail) for any input files containing spaces; housekeeping via a map
            for input_file in self.run_options.get("input_file_list", []):
                if " " in input_file:
                    src = Path(input_file)
                    dest = Path(tmp_dir) / src.name.replace(" ", "_")
                    try:
                        os.symlink(src, dest)
                    except OSError:
                        shutil.copy(src, dest)
                    symlink_map[input_file] = str(dest)
            # ? in self.query, replace input files containing spaces with their symlinked/copied underscored version
            prepared_query = [symlink_map.get(arg, arg) for arg in self.query]

            # ? PointFinder runs KMA with the assumption that there is only 1 input file. Block below merges paired FASTQ into one temporary file to fulfill this assumption.
            input_files = [symlink_map.get(file, file) for file in self.run_options.get("input_file_list", [])]
            if self.run_options.get("method") == "kma" and len(input_files) == 2:
                merged_suffix = ".fastq.gz" if all(file.endswith(".gz") for file in input_files) else ".fastq"
                # ? Keep the merged basename aligned with the sample prefix that ParsingManager uses to build the expected PointFinder output filename.
                sample_prefix = Path(input_files[0]).name.split(".")[0].split("_")[0]
                merged_file = str(Path(tmp_dir) / f"{sample_prefix}{merged_suffix}")
                self._merge_input_files(input_files=input_files, output_file=merged_file)
                prepared_query = self._replace_inputfiles_args(prepared_query, [merged_file])
                logging.debug("Merged paired FASTQ inputs %s into temporary file: %s", input_files, merged_file)

            logging.debug("Starting the SNP query via PointFinder")
            self.start_time = time.time()
            CommandInvoker(ShellCommand(cmd=prepared_query, capture=True)).execute()
            self.stop_time = time.time()
        finally:  # ? cleanup any created symlinks/copies and the tempdir
            if tmp_dir and os.path.isdir(tmp_dir):
                try:
                    shutil.rmtree(tmp_dir)
                except Exception:
                    logging.debug("Could not remove temporary PointFinder input dir %s", tmp_dir)
