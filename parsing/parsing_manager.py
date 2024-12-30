#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

ParsingManager class which, as the name suggests, manages the parsing process.
It initializes the parser object, adds the right filters to the parser,
and starts the parsing process.
"""

__author__ = "Mark van de Streek"
__date__ = "2024-12-02"
__all__ = ["ParsingManager"]

import logging

from parsing.coverage_filter import CoverageFilter
from parsing.fasta_parser import FASTAParser
from parsing.fastq_parser import FASTQParser
from parsing.identity_filter import PercentageIdentityFilter
from parsing.name_filter import GeneNameFilter
from parsing.parser import Parser
from parsing.read_config_pattern import ReadConfigPattern


class ParsingManager:
    """
    Class to manage all parsing/configurations based
    operations. It's a caller class that prepares
    all arguments and call the parsing functions.
    ----------
    Methods:
        - __init__: Constructor to initialize the config file
        - set_parser: Method to initialize the parser object
        - get_config_gene_names: Getter function to retrieve gene names
        - get_config_identity: Getter function to retrieve identity
        - get_config_coverage: Getter function to retrieve coverage
        - add_filters_to_parser: Method to add filters to the parser
    ----------
    """

    def __init__(
        self, pattern: ReadConfigPattern, file_type: str, sample_name: str
    ) -> None:
        """
        Constructor of the ParsingManager class.
        This constructor initializes some of the incoming arguments
        and calls the set_parser, add_filters_to_parser, and parse methods.
        The parse method is the method of the Parser object which will start
        the actual parsing process.
        ----------
        Input:
            - pattern: ReadConfigPattern: the config file object
            - file_type: str: the type of the parser (FASTA or FASTQ)
            - sample_name: str: the name of the sample
        """
        logging.debug("Preparing parsing process...")
        self.pattern = pattern
        self.file_type = file_type
        self.sample_name = sample_name
        self.set_parser()
        self.add_filters_to_parser()
        self.parser.parse()

    def set_parser(self) -> None:
        """
        Function that initializes the parser object.
        The incoming arguments are used to initialize the parser.
        """
        logging.debug("Setting up parser object...")
        self.parser = Parser(
            self.pattern.pattern,
            FASTAParser() if self.file_type == "FASTA" else FASTQParser(),
            self.pattern.creation_dict["output"],
            self.sample_name,
        )

    def get_config_gene_names(self) -> list[str]:
        """
        Simple getter function that retrieves the
        gene names from the config file.
        ----------
        Output:
            - list[str]: list with gene names
        ----------
        """
        return [
            item["gene_name"]
            for item in self.pattern.pattern["pattern"]["genes"]
        ]

    def get_config_identity(self) -> float:
        """
        Simple getter function that retrieves the
        identity from the config file.
        ----------
        Output:
            - int: identity
        ----------
        """
        return self.pattern.pattern["pattern"]["perc_ident"]

    def get_config_coverage(self) -> float:
        """
        Simple getter function that retrieves the
        coverage from the config file obj.
        ----------
        Output:
            - int: coverage
        ----------
        """
        return self.pattern.pattern["pattern"]["perc_cov"]

    def add_filters_to_parser(self) -> None:
        """
        Methods that adds the filters to the parser object.
        The filters are based on the config file,
        the gene names, identity, and coverage.
        These specific filter are retrieved by smaller
        getter functions.
        """
        logging.info("Adding filters to Parser object...")
        self.parser.add_filter(
            GeneNameFilter(self.get_config_gene_names(), self.file_type)
        )
        self.parser.add_filter(
            PercentageIdentityFilter(
                self.get_config_identity(), self.file_type
            )
        )
        self.parser.add_filter(
            CoverageFilter(self.get_config_coverage(), self.file_type)
        )
        logging.debug("Filters: %s successfully added", self.parser.filters)
