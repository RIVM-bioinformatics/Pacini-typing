#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

The main goal of this file is to make the package installable.
It is used when cloning the repository and installing through Bioconda.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-11-06"

from setuptools import find_packages, setup

setup(
    name="pacini_typing",
    version="3.0.1",
    author="Mark van de Streek",
    author_email="ids-bioinformatics@rivm.nl",
    packages=find_packages(),
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.12",
    include_package_data=True,
    py_modules=[
        "pacini_typing",
        "make_gene_database",
        "command_utils",
        "handle_search_modes",
        "make_snp_database",
        "codon_table_enum",
    ],
    entry_points={
        "console_scripts": [
            "pacini_typing = pacini_typing:main",
            "Pacini-typing = pacini_typing:main",
        ],
    },
)
