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

import logging
import functools


def log(func):
    """
    Custom decorator to log the function execution. Either successful or not
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrapper function that executes and checks for possible errors in the function result
        This wrapper could only be used for functions that return a subprocess.CompletedProcess object
        """
        try:
            result = func(*args, **kwargs)
            logging.debug(f"Checking for errors in {result.args[0]}")
            if result.returncode == 0:
                logging.debug(f"{result.args[0]} executed successfully")
            else:
                logging.error(f"Error executing {result.args[0]}")
                logging.error(result.stderr)
            return result
        except Exception as e:
            logging.error(f"Exception occurred in {func.__name__}. exception: {str(e)}")
            logging.debug(f"Arguments: {args}")
            logging.debug(f"Keyword arguments: {kwargs}")
            raise e
    return wrapper
