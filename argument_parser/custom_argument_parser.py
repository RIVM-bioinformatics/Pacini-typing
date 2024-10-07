#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

This basic script is used to override the default help message of the argparse.ArgumentParser class.
This way, the line containing the subcommands {subcommands} is removed from the help message.
This could also be used to add custom formatting to the help message in the future.
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"

import argparse
import re

# TODO: remove this class, not necessary for the current implementation


class CustomArgumentParser(argparse.ArgumentParser):
    """
    CustomArgumentParser class that inherits from the argparse.ArgumentParser class.
    Class is only used to format the help message. It removes the line containing the subcommands.
    """
    def format_help(self):
        help_message = super().format_help()
        # Use regex to remove the line containing the subcommands
        help_message = re.sub(r'\{[^}]+\}\n', '', help_message)

        return help_message
