#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Python script that creates a very basic report from running pacini-typing on
both internal and external samples.

Pacini-typing is runned on two different platforms, KMA and BLAST.
"""

import os

list_of_samples = "list_of_samples.csv"
sample_dir = "samples_dir/"


def create_dir_of_lines():
    """
    Function that creates a dictionary from a csv file with the first column as the key
    and the rest of a row as the value in a list.
    ----------
    Output:
        - sample_dict: dictionary with sample data
        - header: list of header columns
    ----------
    """
    sample_dict = {}
    with open(list_of_samples, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("Nummer"):
                header = line.strip().split(";")
            else:
                line = line.strip().split(";")
                sample_dict[line[0]] = line[0:]

    return sample_dict, header


def write_to_csv(header, sample_dict):
    """
    Function that writes the dictionary to a csv file.
    ----------
    Input:
        - header: list of header columns
        - sample_dict: dictionary with sample data
    ----------
    """
    with open("Pacini_on_internal_samples.csv", "w", encoding="utf-8") as f:
        f.write(";".join(header) + "\n")
        for key, value in sample_dict.items():
            f.write(";".join(value) + "\n")


def append_tsv_to_dict():
    """
    Function that retrieves the results from the Pacini-typing runs
    and appends them to the dictionary.
    This dictionary is then written to a csv file in the
    write_to_csv function.
    """
    sample_dict, header = create_dir_of_lines()
    header_added = False

    with open(list_of_samples, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            kma_file = f"{sample_dir}/{line}/KMA/Pacini_run.res.tsv"
            blast_file = f"{sample_dir}/{line}/BLAST/Pacini_run.res.tsv"

            try:
                with open(kma_file, "r", encoding="utf-8") as file:
                    for line in file:
                        if line.startswith("Template_Name"):
                            if not header_added:
                                header.extend(line.strip().split("\t"))
                                header_added = True
                        else:
                            line = line.strip().split("\t")
                            sample_dict[line[0]].extend(line)
            except FileNotFoundError:
                pass

            try:
                with open(blast_file, "r", encoding="utf-8") as file:
                    for line in file:
                        if line.startswith("Template_Name"):
                            if not header_added:
                                header.extend(line.strip().split(","))
                                header_added = True
                        else:
                            line = line.strip().split(",")
                            sample_dict[line[0]].extend(["BLAST"] + line)
            except FileNotFoundError:
                pass

    write_to_csv(header, sample_dict)


def create_external_report():
    """
    This function is only used to create a report from the external samples.
    This means runs of Pacini-typing on samples that are publicly available.
    """
    header_added = False
    samples = "dir_to_external_samples.csv"
    samples_dir = "dir_to_external_samples/"
    with open("O139_report.tsv", "w", encoding="utf-8") as report:
        with open(samples, "r", encoding="utf-8") as sample_file:
            for line in sample_file:
                line = line.strip()
                res_file = f"{samples_dir}/{line}/Pacini_run.tsv.tsv"
                if os.path.isfile(res_file):
                    with open(res_file, "r", encoding="utf-8") as res:
                        for l in res:
                            if l.startswith("Template_Name"):
                                if not header_added:
                                    report.write(l)
                                    header_added = True
                                continue
                            else:
                                report.write(line + "\t" + l)


if __name__ == "__main__":
    append_tsv_to_dict()
    create_external_report()
