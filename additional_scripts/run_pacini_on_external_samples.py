#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Python script that runs pacini-typing on all external (public) samples.
"""

import os

samples_dir = "location_of_samples_dir"
sample_list = "location_of_sample_list"
pacini_tool_location = "location_of_pacini_typing_tool"


def run_pacini_on_all_samples():
    """
    Function that loops through all samples dirs and runs pacini with the
    pR1 and pR2 fastq.gz files and places the contents into this folder
    """
    with open(sample_list, "r") as sample_file:
        for line in sample_file:
            line = line.strip()
            sample1 = f"{samples_dir}/{line}/{line}_1.fastq.gz"
            sample2 = f"{samples_dir}/{line}/{line}_2.fastq.gz"
            if os.path.isfile(sample1) and os.path.isfile(sample2):
                os.system(
                    f"python3 {pacini_tool_location}/pacini_typing.py -v query -p {sample1} {sample2} -db_name mykma -db_path {pacini_tool_location}/refdir/ -o {samples_dir}/{line}/Pacini_run.tsv"
                )


def get_hits():
    """
    Function that reads the results of the pacini run and prints the hits
    This is useful for quick inspection of the results.
    """
    with open(sample_list, "r") as sample_file:
        for line in sample_file:
            line = line.strip()
            res_file = f"{samples_dir}/{line}/Pacini_run.tsv.tsv"
            if os.path.isfile(res_file):
                with open(res_file, "r") as res:
                    for line in res:
                        if line.startswith("Template"):
                            print("\t".join(line.split("\t")[0:5]))
                        if line.startswith("wbfZ_"):
                            print("\t".join(line.split("\t")[0:5]))
                            print()


if __name__ == "__main__":
    run_pacini_on_all_samples()
    get_hits()
