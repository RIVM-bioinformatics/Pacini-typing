#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Enum class to store all codons and their corresponding
amino acids.
This class is used to convert codons to amino acids
and to get the full name of the amino acid.

*PLEASE NOTE: This class is probably way too overkill for the
simple process of converting codons to amino acids. However, for potential
future use of expansion of PointFinder related code,
this class could be very helpful.

For example, the output report of Pacini-typing could be extended
with more alternative amino acid information, like long names.
"""

__author__ = "Mark van de Streek"
__date__ = "2025-05-15"
__all__ = ["CodonTable"]


from enum import Enum


class CodonTable(Enum):
    """
    Enum class to store all codon-related information.
    ----------
    Methods:
        - __init__: Constructor of the class
        - __str__: String representation of the class
        - short: Getter for the short name of the amino acid
        - full: Getter for the full name of the amino acid
        - get_amino_acid: Get the short name of the amino acid
        - get_full_name: Get the full name of the amino acid
    ----------
    """

    TTT = ("F", "Phenylalanine")
    TTC = ("F", "Phenylalanine")
    TTA = ("L", "Leucine")
    TTG = ("L", "Leucine")
    TCT = ("S", "Serine")
    TCC = ("S", "Serine")
    TCA = ("S", "Serine")
    TCG = ("S", "Serine")
    TAT = ("Y", "Tyrosine")
    TAC = ("Y", "Tyrosine")
    TAA = ("*", "Stop")
    TAG = ("*", "Stop")
    TGT = ("C", "Cysteine")
    TGC = ("C", "Cysteine")
    TGA = ("*", "Stop")
    TGG = ("W", "Tryptophan")
    CTT = ("L", "Leucine")
    CTC = ("L", "Leucine")
    CTA = ("L", "Leucine")
    CTG = ("L", "Leucine")
    CCT = ("P", "Proline")
    CCC = ("P", "Proline")
    CCA = ("P", "Proline")
    CCG = ("P", "Proline")
    CAT = ("H", "Histidine")
    CAC = ("H", "Histidine")
    CAA = ("Q", "Glutamine")
    CAG = ("Q", "Glutamine")
    CGT = ("R", "Arginine")
    CGC = ("R", "Arginine")
    CGA = ("R", "Arginine")
    CGG = ("R", "Arginine")
    ATT = ("I", "Isoleucine")
    ATC = ("I", "Isoleucine")
    ATA = ("I", "Isoleucine")
    ATG = ("M", "Methionine")
    ACT = ("T", "Threonine")
    ACC = ("T", "Threonine")
    ACA = ("T", "Threonine")
    ACG = ("T", "Threonine")
    AAT = ("N", "Asparagine")
    AAC = ("N", "Asparagine")
    AAA = ("K", "Lysine")
    AAG = ("K", "Lysine")
    AGT = ("S", "Serine")
    AGC = ("S", "Serine")
    AGA = ("R", "Arginine")
    AGG = ("R", "Arginine")
    GTT = ("V", "Valine")
    GTC = ("V", "Valine")
    GTA = ("V", "Valine")
    GTG = ("V", "Valine")
    GCT = ("A", "Alanine")
    GCC = ("A", "Alanine")
    GCA = ("A", "Alanine")
    GCG = ("A", "Alanine")
    GAT = ("D", "Aspartic acid")
    GAC = ("D", "Aspartic acid")
    GAA = ("E", "Glutamic acid")
    GAG = ("E", "Glutamic acid")
    GGT = ("G", "Glycine")
    GGC = ("G", "Glycine")
    GGA = ("G", "Glycine")
    GGG = ("G", "Glycine")

    def __init__(self, short: str, full: str):
        self._short = short
        self._full = full

    def __str__(self):
        """
        String representation of the class.
        Used for debugging and logging purposes.
        ----------
        Output:
            - String representation of the class
        ----------
        """
        return f"{self.name}: {self.short} ({self.full})"

    @property
    def short(self) -> str:
        """
        Getter function to return the short name of the amino acid.
        ----------
        Output:
            - str: short name of the amino acid
        ----------
        """
        return self._short

    @property
    def full(self) -> str:
        """
        Getter function to return the full name of the amino acid.
        ----------
        Output:
            - str: full name of the amino acid
        ----------
        """
        return self._full

    @classmethod
    def get_amino_acid(cls, codon: str) -> str:
        """
        Getter function to return the amino acid for
        a given codon. It translates the codon to the corresponding
        amino acid using the enum class.
        ----------
        Input:
            - codon: The codon to be translated
        Output:
            - str: The amino acid corresponding to the codon
        ----------
        """
        return cls[codon].short

    @classmethod
    def get_full_name(cls, codon: str) -> str:
        """
        Getter function to return the full name of the amino acid
        for a given codon. It translates the codon to the corresponding
        amino acid using the enum class.
        ----------
        Input:
            - codon: The codon to be translated
        Output:
            - str: The full name of the amino acid corresponding to the codon
        ----------
        """
        return cls[codon].full
