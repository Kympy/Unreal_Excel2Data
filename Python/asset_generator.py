import unreal
import os
import csv
import sys
import unreal as ue


def get_project_name():
    # 언리얼 엔진의 프로젝트 경로 가져오기
    project_dir = unreal.SystemLibrary.get_project_directory()

    # 프로젝트 디렉토리에서 .uproject 파일 찾기
    for file_name in os.listdir(project_dir):
        if file_name.endswith('.uproject'):
            return os.path.splitext(file_name)[0]
    return None


# 프로젝트 명
project_name = get_project_name()
if project_name is None:
    ue.log_error("Cannot define project_name.")
    exit(0)

# 데이터 테이블 에셋 저장 경로
asset_path = "/Game/Table"

# 데이터 테이블 클래스
asset_class = ue.DataTable

# CSV 파일을 보관할 폴더 경로
csv_folder = ue.SystemLibrary.get_project_directory() + "CSV"

if not os.path.isdir(csv_folder):
    os.makedirs(csv_folder)


# struct_path : ex) "/Script/RottenPotato.TestTable"
# 데이터 테이블 에셋 생성 함수
def create_data_table_asset(csv_path):
    # 파일명
    file_name = str(os.path.basename(csv_path)).split('.')[0]
    # 데이터 테이블 파일명
    asset_name = "DT_" + file_name
    # base struct 스크립트 경로
    unreal_struct_path = "/Script/" + project_name + "." + file_name + "Data"

    ue.log("--------- Creating data table asset..." + " Struct path : " + unreal_struct_path + " ----------")
    ue.log(".")
    # 데이터 테이블 구조체
    asset_factory = ue.DataTableFactory()
    asset_factory.struct = ue.load_object(None, unreal_struct_path)
    if asset_factory.struct is None:
        ue.log_error("Asset factory struct is none.")
        return

    # CSV 를 추출해서 순 데이터만 존재하는 임시파일 생성
    origin_rows = []
    with open(csv_path, 'r', encoding='utf-8') as origin:
        csv_reader = csv.reader(origin)
        id_row_index = -1

        for index, row in enumerate(csv_reader):
            origin_rows.append(row)
            if str(row[0]).lower() == "id":
                id_row_index = index

        if id_row_index == -1:
            ue.log_error("Cannot found Id column.")
            return

    raw_data_rows = []
    for index, row in enumerate(origin_rows):
        if index >= id_row_index:
            raw_data_rows.append(row)

    temp_folder = os.path.join(csv_folder, "Temp")
    if not os.path.isdir(temp_folder):
        os.makedirs(temp_folder)

    temp_csv_path = os.path.join(temp_folder, "Temp_" + file_name + ".csv")

    # 무시할 열 인덱스 찾기 -> # 붙은거
    ignore_column_index = []
    for index, column in enumerate(raw_data_rows[0]):
        if str(column).find("#") >= 0:
            ignore_column_index.append(index)
            ue.log("Ignore line : " + str(index))

    with open(temp_csv_path, 'w', encoding='utf-8') as temp_csv:
        for row in raw_data_rows:
            for index, data in enumerate(row):
                # 무시할 열이면 스킵
                if index in ignore_column_index:
                    continue
                temp_csv.write(data)
                if index != len(row):
                    temp_csv.write(",")
            temp_csv.write("\n")

    csv_factory = ue.CSVImportFactory()
    csv_factory.automated_import_settings.import_row_struct = asset_factory.struct

    task = unreal.AssetImportTask()
    task.filename = temp_csv_path
    task.destination_name = asset_name
    task.destination_path = asset_path
    task.replace_existing = True
    task.automated = True
    task.save = True
    task.factory = csv_factory

    ue.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    ue.log("-SUCCESS")
    ue.log(".")
    ue.log(".")
    ue.log(".")
    
    try:
        os.remove(temp_csv_path)
    except FileNotFoundError:
        return
    except Exception as e:
        ue.log_error(e)


# 시작 함수
def start():
    ue.log("#######   Data Table Asset Generator Started!     #######")
    ue.log("######    Target CSV Folder : " + csv_folder)
    ue.log("-")
    # csv_folder 내부의 모든 파일 리스트 검출
    file_list = os.listdir(csv_folder)

    csv_file_list = []
    # CSV 가 아닌 것 걸러내기
    for file in file_list:
        if file.endswith(".csv"):
            csv_file_list.append(file)

    if len(csv_file_list) == 0:
        ue.log_error("There's no CSV file in folder : " + csv_folder)
        sys.exit(0)

    ue.log("----------- CSV File List ------------")
    ue.log("-")
    # 반복문 시작 : 하나 씩 변환 시작
    index = 1
    for file in csv_file_list:
        ue.log("(" + str(index) + ") " + file)
        index += 1

    ue.log(".")
    for file in csv_file_list:
        ue.log(".")
        ue.log(".")
        ue.log("::::::::::::: Start making [" + file + "] ::::::::::::::")
        # csv 파일 경로 추출
        csv_file_path = os.path.join(csv_folder, file)
        create_data_table_asset(csv_file_path)


# 실행 부분
start()
ue.log("********* Asset Generator Finished. **********")
