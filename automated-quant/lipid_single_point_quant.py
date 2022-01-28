"""lipid_single_point_quant.py: calculates concentrations for species based on internal standard heights"""

__author__ = "Bryan Roberts"

import pandas as pd
import numpy as np
import re
import csv
from pathlib import Path
import pyinputplus

FIRST_COLUMN = 1
FIRST_ROW = 1
SECOND_ROW = 2


def set_standards_from_csv(df):
    """takes in csv file with standard information and generates dictionary of standards information
    Parameters:
        df (data frame): user excel sheet in pandas data frame
    Returns:
        dictionary of with all needed standards information filled in
    """
    while True:
        try:
            file_path = pyinputplus.inputFilepath(
                "Enter full file path for csv file containing standards information: ")
            standards_file = open(file_path)
            reader = csv.reader(standards_file)
            standards_data = list(reader)
            break
        except FileNotFoundError:
            print(FileNotFoundError)

    # populate standards dictionary from file
    standards = {}
    for row in range(FIRST_ROW, len(standards_data)):
        name = standards_data[row][0]
        try:
            ng_extracted = float(standards_data[row][1])
        except ValueError:
            print(ValueError)
        standards[name] = {
            "Row": 0, "ID": 0, "ng_extracted": ng_extracted}

    # populate Row and ID from data frame
    set_standard_row_id(df, standards)
    return standards


def set_named_constant(df, pattern):
    """sets column name from data frame based on regex pattern to named constant
    Parameters:
        df (data frame): user excel sheet in pandas data frame
        pattern: regex pattern to match
    Returns:
        name of column matching regex pattern from data frame
    """
    regex_pattern = re.compile(pattern)
    for column_name in df.columns:
        found = regex_pattern.search(column_name.lower())
        if found != None:
            return column_name


def set_sample_name_list(df, pattern):
    """returns all samples column headers in data frame to list
    Parameters:
        df (data frame): user excel sheet in pandas data frame
        pattern: regex pattern to match
    Returns:
        list of sample names in data frame
    """
    sample_names = []
    regex_pattern = re.compile(pattern)
    for column_name in df.columns:
        found = regex_pattern.search(column_name.lower())
        if found != None:
            sample_names.append(column_name)
    return sample_names


def set_standard_row_id(df, standards):
    """sets row and id in standards dictionary from data frame
    Parameters:
        df (data frame): user excel sheet in pandas data frame
        standards: dictionary of standards in formath {name: {"ID":, "Row", "ng_extracted"}}
    Returns:
        None - changes standards in place
    """
    for standard_name in standards:
        for row in range(len(df)):
            if standard_name == df[ANNOTATION_NAME_COLUMN][row]:
                standards[standard_name]["Row"] = row
                standards[standard_name]["ID"] = df[ISTD_MATCH_COLUMN][row]


def find_matching_istd(df, row, standards):
    """finds matching standard of feature based on matching iSTD ID
    Parameters:
        df (data frame): user excel sheet in pandas data frame
        row: int, row currently being processed in data frame
        standards: dictionary of standards in formath {name: {"ID":, "Row", "ng_extracted"}}
    Returns:
        standard_name: string of matching standard based on ID of current row
    """
    for standard_name in standards:
        if standards[standard_name]['ID'] == df[ISTD_MATCH_COLUMN][row]:
            return standard_name


def calculate_results(df, sample_name_list, standards, sample_amount):
    """calculates single point quant results for entire data frame
    Parameters:
        df (data frame): user excel sheet in pandas data frame
        sample_name_list: list of all sample names in data frame
        standards: dictionary of standards in formath {name: {"ID":, "Row", "ng_extracted"}}
        sample_amount: dictionary of sample names as key and sample amount as value
    Returns:
        df_store_calculations - new data frame with calculated results
    """

    # create a new data frame to store values in
    df_store_calculations = df.copy()

    for sample in sample_name_list:
        for row in range(len(df)):
            # get matching internal standards and native values needed for calculation
            standard = find_matching_istd(df, row, standards)
            standard_row = standards[standard]["Row"]
            standard_concentration = standards[standard]["ng_extracted"]
            native_height = df[sample][row]
            istd_height = df[sample][standard_row]

            # update data frame location with calculated value
            calculated_concentration = (
                    ((native_height / istd_height) * standard_concentration) / sample_amount[sample])
            df_store_calculations.loc[row,
                                      sample] = calculated_concentration

    return df_store_calculations


def set_sample_amount(sample_names):
    """returns dictionary with user input sample weights
    Parameters:
        sample_names: list with all sample names in data frame
    Returns:
        dictionary with key as sample name and value as user input sample amount
    """
    # dictionary to store amount for each sample
    sample_amount = dict()

    # ask user to get individual sample amounts or the same value for each sample
    individual_values = pyinputplus.inputYesNo(
        'Enter "yes" to input individual amount per sample or enter "no" to enter a single amount for all samples: ')

    # get input for sample amount
    if individual_values.lower() == 'no':
        amount = pyinputplus.inputFloat("Enter how much sample was extracted (mL or mg): ", greaterThan=0)
    else:
        print("Enter how much sample was extracted (mL or mg):")

    # for each sample - get amount
    for sample in sample_names:
        if individual_values.lower() == 'no':
            sample_amount[sample] = amount
        else:
            amount = pyinputplus.inputFloat(f'{sample}: ', greaterThan=0)
            sample_amount[sample] = amount

    return sample_amount


if __name__ == "__main__":

    while True:

        # get files and extraction amount from user
        while True:
            try:
                df_path = pyinputplus.inputFilepath(
                    "Enter full file path for data excel sheet: ", mustExist=True)
                df = pd.read_excel(df_path)
                break
            except FileNotFoundError:
                print(FileNotFoundError)

        # set named constants and sample names from data frame
        ISTD_MATCH_COLUMN = set_named_constant(df, r'number')
        ANNOTATION_NAME_COLUMN = set_named_constant(df, r'name')
        sample_names = set_sample_name_list(
            df, r'[a-z0-9A-Z]+_[a-z0-9A-Z]+_[a-zA-Z]+')

        # get standards csv file from user and populate standards dictionary
        standards = set_standards_from_csv(df)

        # enter custom weights for each sample or user single value
        sample_amount = set_sample_amount(sample_names)

        # calculate results and save to new excel sheet
        df_after_calculations = calculate_results(df, sample_names, standards, sample_amount)
        path_obj = Path(df_path)
        save_path = str(path_obj.parent / path_obj.stem) + \
                    '_SinglePointQuant.xlsx'
        df_after_calculations.to_excel(save_path, index=False)

        # allow user to repeat on another sheet, or exit program
        again = pyinputplus.inputYesNo(
            'Enter "yes" to repeat on another sheet or enter "no" to exit: ')
        if again.lower() != "yes":
            break
