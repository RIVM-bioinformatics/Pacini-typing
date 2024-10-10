#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

To be filed in later...
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["test_retrieve_body"]

from validating.determine_input_type import FileValidator


def test_retrieve_body():
    """
    Test the retrieve_body() function from the determine_input_type.py module
    The function retrieves the body of the input file
    """
    pass
    # file_name = "./test_data/part_of_VIB_DA2216AA_AS_genomic.fna"
    # input_files = [file_name]
    # validator = FileValidator(input_files)
    #
    # expected = {file_name: [
    # '>NZ_QECI01000275.1 Vibrio cholerae strain OYP3E02 Vc_OYP3E02_Contig_1, whole genome shotgun sequence',
    # 'ATAATGTGATATCGCTAAATAACGGGCACGTATGTGCTCAATCAACAAACGCACTTTGTTGGGCGGTTGGCGCGTGAATG',
    # 'GATAAACTGCGTAGATACCAAGTTTTTTGCCGACCTGTTCTGGAAACACGTCCACCAATTCGCCATTACGAAAATCGTGA',
    # 'TACACCAAACAGCGCGGTACATAAGCAATGCCGTGCCCACCAAGCGCAGCTTTACGCAGTGCGGTGGCATTATCGGTCGA',
    # 'GATAAACTGCGTAGATACCAAGTTTTTTGCCGACCTGTTCTGGAAACACGTCCACCAATTCGCCATTACGAAAATCGTGA']}

    # assert validator.body == expected
