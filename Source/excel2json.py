import unreal as ue
import pandas as pd
import os

project_excel_path = ue.SystemLibrary.get_project_directory() + "Excel"


def read_excel(excel_folder_path, ignore_first_line):
    if not os.path.exists(excel_folder_path):
        os.makedirs(excel_folder_path)
    file_list = os.listdir(excel_folder_path)
    if len(file_list) == 0:
        ue.log_warning("Excel file count is ZERO.")
        return

    for file_path in file_list:
        read_data = pd.read_excel(file_path, engine="openpyxl", sheet_name=None)

        sheet_name_list = list(read_data.keys())
        if len(sheet_name_list) == 0:
            ue.log_error("[" + file_path + "] excel doesn't contain sheet.")
            return

        first_sheet = read_data[sheet_name_list[0]]

        id_cell = first_sheet.isin(["id"]).__nonzero__()
        if id_cell is None:
            ue.log_error("[" + file_path + "] Id cell is not exist.")
            return
        start_row = id_cell[0]
        start_col = 0

        ue.log("Start row = " + start_row)

        max_row = first_sheet.dropna(how='all').index
        max_col = first_sheet.dropna(how='all', axis= 1).colums

        ue.log("Max row = " + max_row + " / Max col = " + max_col)

        # for row in range(first_sheet.)
        # if ignore_first_line:


read_excel(project_excel_path, True)
ue.log("Finished")



