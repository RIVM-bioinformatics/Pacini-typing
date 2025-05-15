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
from typing import Any

import pandas as pd

from parsing.coverage_filter import CoverageFilter
from parsing.fasta_parser import FASTAParser
from parsing.fastq_parser import FASTQParser
from parsing.identity_filter import PercentageIdentityFilter
from parsing.parser import Parser
from parsing.read_config_pattern import ReadConfigPattern
from parsing.snp_parser import SNPParser
from preprocessing.exceptions.parsing_exceptions import HandlingError


class ParsingManager:
    """
    Class to manage all parsing/configurations based
    operations. It's a caller class that prepares
    the right parsers objects and adds the right filters
    to the classes.
    ----------
    Methods:
        - __init__: Constructor to initialize the config file
        - run: Function that calls the right handler function
        - _prepare_gene_parser: Function that prepares the gene parser
        - _create_snp_parser: Function that creates the SNP parser
        - _run_genes: Function that handles the parsing process for genes
        - process_reports: Function that processes the reports of either genes,
            SNPs or both
        - _run_snps: Function that handles the parsing process for SNPs
        - _run_both: Function that handles the parsing process for both genes and SNPs
        - set_parser: Function that initializes the parser object
        - get_config_gene_names: Function that retrieves the gene names
        - get_config_identity: Function that retrieves the identity
        - get_config_coverage: Function that retrieves the coverage
        - add_filters_to_parser: Function that adds the filters to the parser object
        - write_report: Function that writes a given DataFrame to a csv file
    ----------
    """

    def __init__(
        self,
        pattern: ReadConfigPattern,
        file_type: str,
        sample_name: str,
        search_mode: str,
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
        ----------
        """
        logging.debug("Preparing parsing process...")
        self.pattern = pattern
        self.file_type = file_type
        self.sample_name = sample_name
        self.search_mode: str = search_mode
        # Define the gene parser as a class variable,
        # since this is easier for adding filters and operations
        self.parser = pd.DataFrame()
        # define the handler functions for the right search mode
        self.handlers: dict[str, Any] = {
            "genes": self._run_genes,
            "SNPs": self._run_snps,
            "both": self._run_both,
        }
        self.run()

    def run(self) -> None:
        """
        Function that calls the right handler function,
        based on the search mode. The search mode is used
        to determine which parsing function to call.

        If the search mode is both, two parser objects are required,
        therefore this function contains the main logic for the calling.
        ----------
        Raises:
            - HandlingError: if something goes wrong with the
                handling of the parsing process
        ----------
        """
        logging.info("Determining which parsers to use...")
        try:
            handler = self.handlers[self.search_mode]
        except KeyError as exc:
            logging.error(
                "No handler found for search mode %s", self.search_mode
            )
            raise HandlingError(self.search_mode) from exc
        handler()

    def _prepare_gene_parser(self):
        """
        Function that prepare the gene parser object
        for running the parsing process. The object is being
        added as a class variable to easier apply filters and operations
        on the parser object.
        The parser object could either be a FASTA or FASTQ parser,
        based on the file type.
        ----------
        Output:
            - parser: FASTA or FASTQ Parser object
        ----------
        """
        logging.debug("Setting up the gene parser object...")
        self.parser = Parser(
            self.pattern.pattern,
            FASTAParser() if self.file_type == "FASTA" else FASTQParser(),
            self.pattern.creation_dict["output"],
            self.sample_name,
        )
        self.add_filters_to_parser()

        return self.parser

    def get_path_to_pointfinder_file(self) -> str:
        """
        Little helper function that combines the path to the
        PointFinder file with the hits information.
        The file name is based on the sample name and method used.
        ----------
        Output:
            - str: path to the PointFinder file
        ----------
        """
        return (
            self.pattern.creation_dict["SNP_output_dir"]
            + self.sample_name.split(".")[0].split("_")[0]
            + "_"
            + "kma"
            if self.file_type == "FASTQ"
            else "blastn" + "_results.tsv"
        )

    def _create_snp_parser(self):
        """
        Function that creates the SNP parser object
        and returns it to the caller.
        The SNP parser is not executed but only initialized
        and returned to the caller.
        ----------
        Output:
            - SNPParser: SNP parser object
        ----------
        """
        # TODO: fix the right output file name passing
        # file_fullpath = out_path + "/" + sample_name + "_" + method + "_" + output_files[i]
        # out_path: output path (/ ?)
        # method: 'kma' OR 'blastn'
        # output_files: 'results.tsv'

        # path_to_snp_file: str = self.get_path_to_pointfinder_file()
        logging.debug("Setting up the SNP parser object...")
        return SNPParser(
            self.pattern.pattern, self.sample_name, self.file_type
        )

    def _run_genes(self) -> None:
        """
        Function that handles the parsing process for the genes,
        this means calling the parser object and writing the report
        to a csv file. The parser object creation is delegated and
        the parse method is called to start the parsing process.
        """
        logging.debug("Running the gene parser...")
        parser = self._prepare_gene_parser()
        parser.parse()
        self.write_report(parser.output_report, "report", self.sample_name)

    def process_reports(
        self, gene_report: pd.DataFrame, snp_report: pd.DataFrame
    ) -> None:
        """
        Function that processes the reports of either genes, SNPs or both.
        If both reports are empty, a warning is logged and the function
        returns. Furthermore, the check seems very straightforward,
        if one of the reports is empty, the other report is used.
        ----------
        Input:
            - gene_report: DataFrame: the gene report
            - snp_report: DataFrame: the SNP report
        ----------
        """
        if gene_report.empty and snp_report.empty:
            logging.warning("Both gene and SNP reports are empty, skipping...")
            return
        if gene_report.empty:
            final_report = snp_report
            logging.info("Gene report is empty, writing SNP report only...")
        elif snp_report.empty:
            final_report = gene_report
            logging.info("SNP report is empty, writing gene report only...")
        else:
            logging.info(
                "Found both gene and SNP reports, concatenating and writing..."
            )
            final_report = pd.concat(
                [gene_report, snp_report], ignore_index=True
            )
            if "ID" in final_report.columns:
                final_report["ID"] = range(1, len(final_report) + 1)

        ParsingManager.write_report(final_report, "report", self.sample_name)

    def _run_snps(self) -> None:
        """
        Function that handles the parsing process for the SNPs,
        this means calling the SNP parser object and writing the report
        to a csv file. The SNP parser object creation is delegated and
        the parse method is called to start the parsing process.
        """
        parser = self._create_snp_parser()
        parser.parse()
        self.write_report(parser.output_report, "report", self.sample_name)

    def _run_both(self) -> None:
        """
        Main function that handles the parsing of both genes and SNPs.
        The _prepare_gene_parser and _create_snp_parser methods are called
        and respectively executed by calling the parse methods.
        Subsequently, the reports are concatenated passed along to the
        write_report method to write the report to a csv file.
        """
        logging.debug("Running both gene and SNP parsers...")
        gene_parser = self._prepare_gene_parser()
        gene_parser.parse()
        snp_parser = self._create_snp_parser()
        snp_parser.parse()
        # Define the reports and check their content
        gene_report = gene_parser.output_report
        snp_report = snp_parser.output_report
        # Process the reports
        logging.info("Parsing process finished, processing reports...")
        return self.process_reports(gene_report, snp_report)

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
            - list with gene names
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
            - percentage identity
        ----------
        """
        return float(self.pattern.pattern["pattern"]["perc_ident"])

    def get_config_coverage(self) -> float:
        """
        Simple getter function that retrieves the
        coverage from the config file obj.
        ----------
        Output:
            - percentage coverage
        ----------
        """
        return float(self.pattern.pattern["pattern"]["perc_cov"])

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
            PercentageIdentityFilter(
                self.get_config_identity(), self.file_type
            )
        )
        self.parser.add_filter(
            CoverageFilter(self.get_config_coverage(), self.file_type)
        )
        logging.debug("Filters: %s successfully added", self.parser.filters)

    @staticmethod
    def write_report(
        report: pd.DataFrame, suffix: str, input_sequence_sample: str
    ) -> None:
        """
        Function that writes a given DataFrame to a csv file.
        The pandas DataFrame is created by other methods,
        and passed to this method to write it to a file.
        ----------
        Input:
            - report: the DataFrame to write
            - suffix: suffix to add to the filename
        ----------
        """
        logging.debug("Writing the %s...", suffix)
        file_name = f"{input_sequence_sample}_{suffix}.csv"
        report.to_csv(
            file_name,
            sep=",",
            index=False,
        )
        logging.info("Successfully wrote %s...", file_name)
