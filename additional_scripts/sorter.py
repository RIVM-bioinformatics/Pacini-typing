#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Python script that is used to sort the downloaded files
into the correct directories.
Some additional preprocessing is also done.

See the functions for more information.
"""

import csv
import json
import os
import sys


def create_dirs(sample_file: str):
    """
    Function that reads the sample file and
    created a directory for each sample.
    This directory is used to place the downloaded files in.
    ----------
    Input:
        - sample_file: path to the file with the samples
    ----------
    """
    with open(sample_file, "r", encoding="utf-8") as file:
        for i in file:
            os.system(f"mkdir {i}")


def compare_first_column_csv(file1: str, file2: str) -> bool:
    """
    This is a utility function that compares th original sample file
    with the list of samples that were retrieved and used for
    downloading files from IRODS.

    This function is needed to check if the samples are actually the same,
    to prevent missing files or files that are not related to the samples.
    ----------
    Input:
        - file1: path to the first file
        - file2: path to the second file
    Output:
        - bool: True if the two files are the same, False otherwise
    ----------
    """
    with open(file1, "r", encoding="utf-8") as f1, open(
        file2, "r", encoding="utf-8"
    ) as f2:
        csv1 = csv.reader(f1)
        csv2 = csv.reader(f2)
        for row1, row2 in zip(csv1, csv2):
            if row1[0] != row2[0]:
                return False
    return True


def sort_downloaded_files(output_dir: str, samples_file: str):
    """
    Function that walks through all samples in sample file and
    searches for files that match the sample name.
    All these matching files are moved to the samples directory,
    which was created with the create_dirs() function.
    ----------
    Input:
        - output_dir: path to the directory with the downloaded files
        - samples_file: path to the file with the samples
    ----------
    """
    with open(samples_file, "r", encoding="utf-8") as file:
        for i in file:
            i = i.strip()
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    if i in file:
                        print(f"mv {output_dir}/{file} {output_dir}/{i}/")
                        os.system(f"mv {output_dir}/{file} {i}")


def sort_meta_data_into_sample_folder(meta_data_file: str, output_dir: str):
    """
    Function that reads the meta data file and for every row,
    it creates a new file in the folder of the sample,
    with the header from the metadata file and the information from the row.
    The first column of the metadata file contains the dir names.
    ----------
    Input:
        - meta_data_file: path to the metadata file
        - output_dir: path to the directory where the metadata files should be placed
    ----------
    """
    with open(meta_data_file, "r", encoding="utf-8") as f:
        header = f.readline().strip().split(";")
        for line in f:
            line = line.strip().split(";")
            sample_dir = line[0]
            new_file = f"{output_dir}/{sample_dir}/{sample_dir}_metadata.json"
            metadata = dict(zip(header, line))
            with open(new_file, "w", encoding="utf-8") as out:
                json.dump(metadata, out, indent=4)


if __name__ == "__main__":
    create_dirs(sample_file="secrid_path_to_sample.csv")
    if not compare_first_column_csv(
        file1="secrid_path_to_sample.csv", file2="secrid_path_to_sample.csv"
    ):
        sys.exit("The samples are not the same, please check the files")

    sort_downloaded_files(
        output_dir="secrid_path_to_downloaded_files",
        samples_file="secrid_path_to_sample.csv",
    )
    sort_meta_data_into_sample_folder(
        meta_data_file="secrid_path_to_metadata.csv",
        output_dir="secrid_path_to_downloaded_files",
    )
