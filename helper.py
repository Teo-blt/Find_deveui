#!/usr/bin/env python 3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: June 6 10:00:00 2023
# For Wi6labs, all rights reserved
# =============================================================================
"""The Module Has Been Build as a helper to main"""
# =============================================================================
# Imports
from tkinter.messagebox import *


# ============================================================================


def valid_dev_eui(dev_eui_to_check: str):
    """
    valid_dev_eui verify that the user enter a valid value

    :param dev_eui_to_check: the value to check
    :return True or False
    """
    match dev_eui_to_check:
        case (""):
            showerror("Error", "You must select a valid Dev_eui")
            return False
        case ("--choose your Dev_eui here--"):
            showerror("Error", "You must select a valid Dev_eui")
            return False
        case _:
            if len(dev_eui_to_check) < 17:
                return True
            else:
                showerror("Error", "The Dev_eui is too long")
                return False


def valid_number_file(number_file_to_check: int):
    """
    valid_number_file verify that the user enter a valid value

    :param number_file_to_check: the number to check
    :return True or False
    """
    if number_file_to_check == 1 or number_file_to_check == 2 or number_file_to_check == 3:
        return True
    else:
        showerror("Error", "Not a valid number of files to open")
        return False


def valid_path_to_file(path_to_file_to_check: str):
    """
    valid_path_to_file verify that the user enter a valid value

    :param path_to_file_to_check: the path to check
    :return True or False
    """
    match path_to_file_to_check:
        case (""):
            showerror("Error", "You must select a valid path")
            return False
        case _:
            return True
