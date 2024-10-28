#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
> This script was developed with assistance from GitHub Copilot for code suggestions.
> AI-generated suggestions have been reviewed and modified as necessary by the developer.
> GitHub, OpenAI, & Microsoft. (2021). GitHub Copilot [Software]. In
    “GitHub Copilot: Your AI pair programmer” (GPT-3). GitHub, Inc.
    https://github.com/features/copilot

Python script to create custom decorators.
Decorators are used to modify the behavior of a function or a class method.
"""

__author__ = "Mark Van de Streek"
__data__ = "2024-09-24"
__all__ = ["log"]

import functools
import logging


def log(func):
    """
    Custom decorator to log the function execution. Either successful or not
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrapper function that executes and checks for possible exceptions in the function result
        This wrapper could only be used for functions that return a
        subprocess.CompletedProcess object
        ----------
        Input:
            - *args: positional arguments
            - **kwargs: keyword arguments
        Output:
            - result: subprocess.CompletedProcess object
        """
        try:
            result = func(*args, **kwargs)
            logging.debug("Checking for exceptions in %s", result.args[0])
            if result.returncode == 0:
                logging.info("Command %s executed successfully", result.args[0])
            else:
                logging.error("Error executing %s", result.args[0])
                logging.error(result.stderr)
            return result
        except Exception as e:
            logging.error(
                "Exception occurred in %s. exception: %s", func.__name__, str(e)
            )
            logging.debug("Arguments: %s", args)
            logging.debug("Keyword arguments: %s", kwargs)
            raise e

    return wrapper
