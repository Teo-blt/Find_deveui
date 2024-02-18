#!/usr/bin/env python 3.10
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: May 15 14:00:00 2023
# For Wi6labs, all rights reserved
# =============================================================================
"""The Module Has Been Build to find AppSKey"""
# =============================================================================
# Imports
import pandas as pd
import os
import csv
import warnings
import time
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import *
import sys
import concurrent.futures
from loguru import logger
import openpyxl

from helper import valid_dev_eui, valid_number_file, valid_path_to_file


# ============================================================================

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)  # Initialisation of the first window
        self._ip_wiserver1 = "192.168.100.14"
        self._NUM_WORKERS = 8
        # csv A81758FFFE08AA37
        # many 70b3d5e75e0103ad
        # xlsx 70B3D56371385CAD
        self.number_of_file_to_open = 1
        self.start_time = 0
        self.search_value = StringVar()
        self.path_to_files = StringVar()
        self.color = "#E76145"
        warnings.filterwarnings("ignore", category=UserWarning)
        self.main_window()

    def main_window(self):
        """
        main_window create the HMI window
        """
        number_of_file_to_open = IntVar()
        finder_frame = LabelFrame(self, text="Finder of AppSKey")
        finder_frame.grid(row=0, column=1, ipadx=40, ipady=10, padx=0, pady=0)
        button_frame = LabelFrame(self, text="Number of file(s) to open")
        button_frame.grid(row=1, column=2, ipadx=40, ipady=10, padx=0, pady=0)
        lunch_the_program = LabelFrame(self, text="Launch the program")
        lunch_the_program.grid(row=1, column=1, ipadx=40, ipady=10, padx=0, pady=0)
        place = finder_frame
        finder_frame_label = Label(place, text="Enter the Dev_eui :")
        finder_frame_label.pack(padx=0, pady=0, ipadx=0, ipady=0, expand=False, fill="none", side=TOP)
        entry_finder = ttk.Entry(place, textvariable=self.search_value)
        entry_finder.insert(0, "--choose your Dev_eui here--")
        entry_finder.focus()
        entry_finder.pack(ipadx=0, ipady=0, padx=20, pady=0, expand=True, side=TOP, fill="x")
        path_frame_label = Label(place, text="Enter your path to directory :")
        path_frame_label.pack(padx=0, pady=0, ipadx=0, ipady=0, expand=False, fill="none", side=TOP)
        path_label = ttk.Entry(place, textvariable=self.path_to_files)
        path_label.insert(0, "P:\VeilleCapteurs\LORAWAN")
        path_label.focus()
        path_label.pack(ipadx=0, ipady=0, padx=20, pady=0, expand=True, side=TOP, fill="x")

        def upload_action(new_path):
            """
            upload_action open a file dialog window to ask the directory to the user

            :param new_path: the entry to write the new path
            """
            filename = filedialog.askdirectory()
            new_path.delete(0, 2000)
            new_path.insert(0, filename)

        browse_button = Button(place, text="Browse", cursor="right_ptr", overrelief="sunken",
                               command=lambda: [upload_action(path_label)])
        browse_button.pack(padx=0, pady=0, ipadx=0, ipady=0, expand=False, fill="none", side=TOP)
        radiobutton_none = Radiobutton(button_frame, text="None", variable=number_of_file_to_open, value=1)
        radiobutton_none.pack(ipadx=0, ipady=0, padx=20, pady=0, expand=True, side=TOP, fill="x", anchor=W)
        radiobutton_one = Radiobutton(button_frame, text="One (1)", variable=number_of_file_to_open, value=2)
        radiobutton_one.pack(ipadx=0, ipady=0, padx=20, pady=0, expand=True, side=TOP, fill="x", anchor=W)
        radiobutton_one.select()
        radiobutton_all = Radiobutton(button_frame, text="All", variable=number_of_file_to_open, value=3)
        radiobutton_all.pack(ipadx=0, ipady=0, padx=20, pady=0, expand=True, side=TOP, fill="x", anchor=W)
        lunch_the_program_button = Button(lunch_the_program, text="Find",
                                          borderwidth=8, background=self.color,
                                          activebackground="green", cursor="right_ptr", overrelief="sunken",
                                          command=lambda: [self.main(number_of_file_to_open.get())])
        lunch_the_program_button.pack(padx=0, pady=0, ipadx=40, ipady=10, expand=False, fill="none", side=TOP)

    def main(self, nb_file):
        """
        main create the threading process

        :param nb_file: the number of files to open
        """
        if valid_dev_eui(self.search_value.get()) \
                and valid_number_file(self.number_of_file_to_open) \
                and valid_path_to_file(self.path_to_files.get()):
            self.number_of_file_to_open = nb_file
            logger.info(f"the searched value is : {self.search_value.get()}")
            logger.info(f"the path to directory is : {self.path_to_files.get()}")
            self.withdraw()
            self.start_time = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=self._NUM_WORKERS) as executor:
                futures = {executor.submit(self.do_find, self.search_value.get(), root, files) for root, dirs, files in
                           os.walk(self.path_to_files.get())}
                concurrent.futures.wait(futures)
        else:
            pass

    def do_find(self, search_value: str, root: str, files: list):
        """
        do_find does find the user's searched value in all the files of the directory

        :param search_value: the user's searched value
        :param root: root to the main directory of the files
        :param files: list of all the files
        """
        for file in files:
            if file.startswith("~"):  # pass all the files that are currently opened
                pass
            else:
                match file.split('.')[-1]:
                    case ("xlsx"):
                        xls = pd.ExcelFile(os.path.join(root, file))
                        for sheet in xls.sheet_names:
                            cat_excel = pd.read_excel(os.path.join(root, file), sheet)
                            cat_excel = cat_excel.to_csv(index=False, lineterminator=";")
                            for line in cat_excel.split(';'):
                                if search_value.lower() in line.lower():
                                    self.print_in_console(root, file, sheet, line)
                    case ("xls"):
                        xls = pd.ExcelFile(os.path.join(root, file))
                        for sheet in xls.sheet_names:
                            cat_excel = pd.read_excel(os.path.join(root, file), sheet)
                            cat_excel = cat_excel.to_csv(index=False, lineterminator=";")
                            for line in cat_excel.split(';'):
                                if search_value.lower() in line.lower():
                                    self.print_in_console(root, file, sheet, line)
                    case ("csv"):
                        with open(os.path.join(root, file), 'r') as f:
                            cat_csv = csv.reader(f, delimiter=";")
                            for line in cat_csv:
                                for item in line:
                                    if search_value.lower() in item.lower():
                                        self.print_in_console(root, file, "None", line)
                    case ("txt"):
                        with open(os.path.join(root, file), 'r', errors='ignore') as f:
                            cat_txt = f.readlines()
                            for line in cat_txt:
                                if search_value.lower() in line.lower():
                                    self.print_in_console(root, file, "None", line)
                    case _:
                        # "pdf", "htm", "docx", "pptm", "db", "pptx", "zip", "png",
                        # "jpeg", "exe", "arf", "msi", "lnk", "ods", "odt",
                        # "js", "json", "apk", "msg",...
                        pass

    # not used anymore, it was replaced by the HMI
    '''
    def ask_value_find(self):
        """
        ask_value_find ask the user the value to find

        :return: search_value: str, the user's searched value
        """
        nb_file = 0
        search_value = input("Type the value to find: ")
        for root, dirs, files in os.walk(self.path_to_files.get()):
            for file in files:
                nb_file += 1
        print("Number of files: " + str(nb_file))
        return search_value
    '''

    def print_in_console(self, root: str, file: str, sheet: str, line):
        """
        print_in_console does print all the information about the file and open it

        :param root: root of the file
        :param file: name of the file
        :param sheet: name of the sheet were the user's searched value is
        :param line: line were the user's searched value is
        """
        logger.success(f"-------------------Value find in the following file--------------")
        logger.info(f"path to file : {os.path.join(root, file)}")
        logger.info(f"file name : {file}")
        logger.info(f"Name of sheet : {sheet}")
        logger.info(f"Value find at line : {line}")
        logger.success(f"-------------------------END RECHERCHE-------------------------")
        logger.debug(f"Total time : {time.time() - self.start_time}")
        match self.number_of_file_to_open:
            case (1):  # No file to open
                self.quit()
                sys.exit()
            case (2):  # Open one (1) file
                os.startfile(root + '\\' + file)
                self.quit()
                sys.exit()
            case (3):  # Open all the files
                os.startfile(root + '\\' + file)
            case _:
                showerror("Error", "Not a valid number of files to open")


if __name__ == "__main__":
    # execute only if run as a script
    Application().mainloop()
