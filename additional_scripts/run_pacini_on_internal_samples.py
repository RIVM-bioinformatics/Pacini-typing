#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Python script that runs pacini-typing on all internal samples.
"""

import os
import shutil
import subprocess
from pathlib import Path

samples_dir = "location_of_samples_dir"
sample_list = "location_of_sample_list"
pacini_typing_tool = "location_of_pacini_typing_tool"

# TODO harmonize internal and external sample scripts?


# TODO use command_utils.py?
def clean_failed_runs():
    """
    Function that checks for failed runs by verifying the existence
    of the expected output and removes the output directory if the run failed.
    """
    with open(sample_list, "r", encoding="utf-8") as sample_file:
        for line in sample_file:
            line = line.strip()
            if not line.endswith("02"):
                parent = Path(f"{samples_dir}/{line}/RUN_001")
                if parent.is_dir():
                    for child in parent.iterdir():
                        shutil.rmtree(child) if child.is_dir() else child.unlink()


def run_pacini_on_all_samples():
    """
    Function that loops through all sample directories and runs pacini with the
    pR1 and pR2 fastq.gz files, placing the contents into the output folder.
    """
    with open(sample_list, "r", encoding="utf-8") as sample_file:
        for line in sample_file:
            line = line.strip()
            sample1 = f"{samples_dir}/{line}/{line}_pR1.fastq.gz"
            sample2 = f"{samples_dir}/{line}/{line}_pR2.fastq.gz"
            output = f"{samples_dir}/{line}/KMA/"
            if not os.path.exists(output):
                os.mkdir(output)
            if os.path.isfile(sample1) and os.path.isfile(sample2):
                cmd = [
                    "python3",
                    f"{pacini_typing_tool}/pacini_typing.py",
                    "-v",
                    "query",
                    "-p",
                    sample1,
                    sample2,
                    "-db_name",
                    "mykma",
                    "-db_path",
                    f"{pacini_typing_tool}/refdir/",
                    "-o",
                    f"{output}Pacini_run.res",
                ]
                try:
                    subprocess.run(cmd, check=True)
                except subprocess.CalledProcessError:
                    print(f"Pacini failed for sample {line}")


if __name__ == "__main__":
    # clean_failed_runs()
    run_pacini_on_all_samples()
