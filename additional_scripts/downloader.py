#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python script for downloading accession numbers from the SRA database using the
fasterq-dump tool from the SRA Toolkit.

> The script can download the accession numbers using multiple threads.

The samples are read from a file called `list.txt` in the current directory.
Of course, you can change the name of the file or the path to the file.
Additionally, the output directory can be changed to a different location.
For example, this script was used to download the samples to a mounted SSD.

Usage:
    python downloader.py

Requirements:
    - fasterq-dump (validate with `which fasterq-dump`)
"""

__author__ = "Mark van de Streek"
__date__ = "2024-11-19"
__all__ = ["download_fastq"]

import subprocess
from multiprocessing import Pool

OUTPUT_DIR = "."
LOG_FILE = "download_errors.log"
NUM_THREADS = 8


def download_fastq(accession: str):
    """
    Downloads FASTQ files for a single accession.

    Args:
      accession: The accession number.
    """

    cmd = f"fasterq-dump --split-files --outdir {OUTPUT_DIR} {accession}"
    try:
        print(cmd)
        subprocess.run(cmd, shell=True, check=True)
        print(f"Downloaded files for {accession}")
    except subprocess.CalledProcessError as e:
        with open(LOG_FILE, "a", encoding="utf-8") as error_log:
            error_msg = f"Error downloading files for {accession}: {e}\n"
            print(error_msg)
            error_log.write(error_msg)


if __name__ == "__main__":
    # Read the accession numbers from the file
    with open("list.txt", "r", encoding="utf-8") as f:
        accessions = [line.strip() for line in f]
    # Download the samples using multiple threads
    with Pool(NUM_THREADS) as p:
        p.map(download_fastq, accessions)
