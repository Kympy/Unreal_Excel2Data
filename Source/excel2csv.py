
import subprocess as sp
import unreal as ue
import os

# 엑셀 폴더 경로
excel_folder = ue.SystemLibrary.get_project_directory() + "Excel"

# CSV 파일을 보관할 폴더 경로
csv_folder = ue.SystemLibrary.get_project_directory() + "CSV"

# excel 2 csv exe 경로
excel_to_csv_exe_path = os.path.join(ue.SystemLibrary.get_project_content_directory(), "Python", "DGExcel2Data", "Excel2CSV", "DGExcel2CSV.exe")

if not os.path.isdir(excel_folder):
    os.makedirs(excel_folder)

if not os.path.isdir(csv_folder):
    os.makedirs(csv_folder)


# Excel -> CSV 함수


def make_excel_to_csv():

    # 존재하는 엑셀이 있는지 검사하기
    excel_file_list = os.listdir(excel_folder)
    xlsx_count = 0
    for file in excel_file_list:
        if file.endswith(".xlsx"):
            xlsx_count += 1

    if xlsx_count == 0:
        ue.log("Excel file is not exists.")
        return

    parameters = " \"" + excel_folder + "\"" + " " + "\"" + csv_folder + "\""
    cmd = excel_to_csv_exe_path + " " + parameters
    ue.log("Execute Excel2CSV => " + cmd)
    result = sp.run(cmd, capture_output=True, text=True, encoding='cp949')
    ue.log("[Excel2CSV Result] Code : " + str(result.returncode))
    ue.log("[Excel2CSV Result] StdOut : " + str(result.stdout))
    if result.returncode != 0:
        ue.log_error("[Excel2CSV Result] StdErr : " + str(result.stderr))


make_excel_to_csv()
