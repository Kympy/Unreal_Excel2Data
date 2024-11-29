
import subprocess as sp
import unreal as ue
import os

# 엑셀 폴더 경로
excel_folder = ue.SystemLibrary.get_project_directory() + "Excel"

# CSV 파일을 보관할 폴더 경로
csv_folder = ue.SystemLibrary.get_project_directory() + "Temp"

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
    # result = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, text=True, encoding='cp949')
    # 
    # # 실시간으로 stdout과 stderr를 읽기
    # while True:
    #     output = result.stdout.readline()  # 한 줄씩 읽음
    #     # error = result.stderr.readline()
    #     if output == '' and result.poll() is not None:  # 프로세스 종료 확인
    #         break
    #     if output:
    #         ue.log("[Excel2CSV StdOut] " + output.strip())  # 줄 출력
    #     # if error:
    #         # ue.log("[Excel2CSV StdErr] " + error.strip())
    # 
    # result.wait()
    ue.log("[Excel2CSV Result] Code : " + str(result.returncode))
    # ue.log("[Excel2CSV Result] StdOut : " + str(result.stdout))
    if result.returncode != 0:
        ue.log_error("[Excel2CSV Result] StdErr : " + str(result.stderr))


make_excel_to_csv()
