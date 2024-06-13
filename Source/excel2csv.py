
import subprocess as sp
import unreal as ue
import os

# 엑셀 폴더 경로
excel_folder = ue.SystemLibrary.get_project_directory() + "Excel"

# CSV 파일을 보관할 폴더 경로
csv_folder = ue.SystemLibrary.get_project_directory() + "CSV"

# excel 2 csv exe 경로
excel_to_csv_exe_path = os.path.join(ue.SystemLibrary.get_project_content_directory(), "Python", "DGExcel2Data", "Excel2CSV", "DGExcel2CSV.exe")

ue.log("Execute program Excel2CSV : " + excel_to_csv_exe_path)

if not os.path.isdir(excel_folder):
    os.makedirs(excel_folder)

if not os.path.isdir(csv_folder):
    os.makedirs(csv_folder)


# Excel -> CSV 함수


def make_excel_to_csv():

    parameters = [excel_folder, csv_folder]
    result = sp.run([excel_to_csv_exe_path] + parameters, capture_output=True, text=True)
    ue.log("[Excel2CSV Result] Code : " + str(result.returncode))


make_excel_to_csv()
