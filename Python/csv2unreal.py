import unreal
import os
import sys
import csv
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

# CSV 파일을 보관할 폴더 경로
csv_folder = ue.SystemLibrary.get_project_directory() + "Temp"

# c++ struct 를 저장할 폴더 경로 ->
struct_save_folder = os.path.join(ue.SystemLibrary.get_project_directory(), "Source", project_name, "Public", "Table")

raw_csv_path = ue.SystemLibrary.get_project_content_directory() + "CSV"

if not os.path.isdir(struct_save_folder):
    os.makedirs(struct_save_folder)



# 개행 함수
def next_line(file):
    file.write("\n")


# 타입 선별 함수
def get_unreal_type(type):
    str_type = str(type).lower()
    
    if str_type == "int" or str_type == "int32" or str_type.find("int") >= 0:
        return "int32"
    elif str_type == "float" or str_type == "float32" or str_type.find("float") >= 0:
        return "float"
    elif str_type == "string" or str_type == "fstring" or str_type.find("string") >= 0:
        return "FString"
    # 룰에 의해 id 타입은 언리얼에서 RowName 으로 사용할 것이므로 FName 으로 리턴
    elif str_type == "id" or str_type.find("id") >= 0:
        return "FName"
    elif str_type == "bool" or str_type == "boolean" or str_type.find("bool") >= 0:
        return "bool"
    elif str_type == "vector" or str_type == "vector3" or str_type.find("vector") >= 0:
        return "FVector"
    elif str_type == "rotator" or str_type == "rotator" or str_type.find("rotator") >= 0:
        return "FRotator"
    elif str_type == "text" or str_type.find("text") >= 0:
        return "FText"
    elif str_type == "color" or str_type == "coloru8" or str_type.find("color") >= 0:
        return "FLinearColor"
    else:
        unreal.log_error(str_type + " << This type is not allowed. It will change to \'FString\'.")
        return "FString"


def is_array_type(type):
    is_array = str(type).find('[')
    if is_array == -1:
        return False
    return True
    

# 초기값 판별 : 값 형식만 해당, get_unreal_type 으로 판별된 이후에 넣어줘야함.
def get_initial_value(type):
    if type == "int32" or type == "float":
        return " = 0"
    elif type == "FLinearColor":
        return " = FLinearColor::White"
    elif type == "bool":
        return " = false"
    else:
        return ""


# 스크립트 작성 함수

def create_struct():
    print("#######   Data Table C++ Struct Generator Started!     #######")
    print("######    Target CSV Folder : " + csv_folder)
    print("-")
    # csv_folder 내부의 모든 파일 리스트 검출
    file_list = os.listdir(csv_folder)

    csv_file_list = []
    # CSV 가 아닌 것 걸러내기
    for file in file_list:
        if file.endswith(".csv"):
            csv_file_list.append(file)

    if len(csv_file_list) == 0:
        unreal.log_error("There's no CSV file in folder : " + csv_folder)
        sys.exit(0)

    print("----------- CSV File List ------------")
    print("-")
    # 반복문 시작 : 하나 씩 변환 시작
    index = 1
    for file in csv_file_list:
        print("(" + str(index) + ") " + file)
        index += 1

    print("-")
    for file in csv_file_list:
        print("-")
        print("::::::::::::: Start making [" + file + "] ::::::::::::::")
        # csv 파일 경로 추출
        csv_file_path = os.path.join(csv_folder, file)
        
        # CSV 를 행 별로 저장
        rows = []
        # 파일 열고 행 별로 rows 에 담는다
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile, quotechar='"', delimiter=',')
            for row in csv_reader:
                rows.append(row)
                # print(row)

        # 행이 아무것도 없다면 종료
        if len(rows) == 0:
            ue.log_error("CSV row count is 0")
            continue

        # Id 로 시작하는 행을 찾기 위해 초기값 -1 로 설정
        column_name_row_index = -1
        for data in rows:
            if data[0] == "Id" or str(data[0]).lower() == "id":
                column_name_row_index = rows.index(data)

        if column_name_row_index == -1:
            ue.log_error("Cannot found Id column")
            continue

        # 먼저 C++ 부터 작성
        print("----------   Writing C++ Struct row table And Raw CSV... RowCount : " + str(len(rows) - column_name_row_index) + " ... ", end="")

        type_name_list = []
        column_name_list = []
        ignore_line_index = []
        # 타입 이름과 컬럼 이름 수집
        column_name_row = rows[column_name_row_index]
        for index, column_name in enumerate(column_name_row):
            # '#' 으로 시작하는 칼럼은 추가하지 않는다.
            if not column_name.startswith("#"):
                # Id 칼럼 위 행은 타입 행이므로 -1 한 위치에서 타입 이름을 저장.
                # rows[Id 칼럼의 윗 행 인덱스][현재 열 인덱스]
                type_row = rows[column_name_row_index - 1]
                type_name_list.append(type_row[index])
                column_name_list.append(column_name)
            else:
                ignore_line_index.append(index)

        # 타입 갯수와 칼럼 열 갯수가 다르면 경고 후 스킵
        if len(type_name_list) != len(column_name_list):
            print("Type name count and column name count is not correct : " + len(type_name_list) + "/" + len(
                column_name_list))
            continue
        
        # 파일명 추출
        file_name = os.path.basename(csv_file_path)
        file_name = str(file_name).split('.')[0]

        # with open(os.path.join(raw_csv_path, os.path.basename(csv_file_path)), 'w', encoding='utf-8') as raw_csv:
        #     writer = csv.writer(raw_csv, quoting=csv.QUOTE_ALL)
        #     for row_index, row in enumerate(rows):
        #         if row_index < column_name_row_index:
        #             continue
        #         for index, data in enumerate(row):
        #             # 무시할 열이면 스킵
        #             if index in ignore_line_index:
        #                 continue
        #             writer.write()
        
        # 날것의 CSV 만 리소스로 저장
        with open(os.path.join(raw_csv_path, os.path.basename(csv_file_path)), 'w', encoding='utf-8') as raw_csv:
            # writer = csv.writer(raw_csv, quoting=csv.QUOTE_ALL)
            for row_index, row in enumerate(rows):
                if row_index < column_name_row_index:
                    continue
                for index, data in enumerate(row):
                    # 무시할 열이면 스킵
                    if index in ignore_line_index:
                        continue
                    # print(f"Index: {index}, Data: {data}")
                    # 빈셀 버그 제거
                    if data == "" or data is None:
                        continue
                    raw_csv.write("\"" + data + "\"")
                    
                    # 마지막이 아니라면 콤마
                    if index != len(row) - 1:
                        # print("Comma" + str(index) + "Len - " + str(len(row) - 1))
                        raw_csv.write(",")
                raw_csv.write("\n")
        
        # 세이브 경로
        struct_file_path = os.path.join(struct_save_folder, "F" + file_name + "Data.h")  
        # 폴더 체크
        
        # 파일 작성 시작
        with open(struct_save_folder + "/F" + file_name + "Data.h", 'w') as c_file:
            c_file.writelines("// Copyright 2024. DragonGate Co. all rights reserved.\n")
            c_file.writelines("// This file is auto generated by UE_DGExcel2Data.\n")
            next_line(c_file)
            c_file.writelines("# pragma once\n")
            next_line(c_file)
            c_file.writelines("#include \"Engine/DataTable.h\"\n")
            c_file.writelines("#include \"F" + file_name + "Data.generated.h\"\n")
            next_line(c_file)
            c_file.writelines("USTRUCT(Blueprintable)\n")
            c_file.writelines("struct F" + file_name + "Data" + " : public FTableRowBase\n")
            c_file.writelines("{\n")
            c_file.writelines("\tGENERATED_USTRUCT_BODY()\n")
            next_line(c_file)
            c_file.writelines("public:\n")
            next_line(c_file)
            # 변수 선언
            for index, value in enumerate(column_name_list):
                # id 변수는 선언하지 않는다 -> 기본적으로 Row Name 칼럼이 Id 역할을 해주기 때문.
                if str(value).lower() == "id":
                    continue
                if str(value).lower() == "":
                    continue
                c_file.writelines("\tUPROPERTY(EditAnywhere, BlueprintReadWrite)\n")
                str_type = get_unreal_type(type_name_list[index])
                # 배열 타입이라면 TArray<> 붙이기
                if is_array_type(type_name_list[index]):
                    c_file.writelines("\tTArray<" + str_type + "> " + str(value) + ";\n")
                # 배열이 아니면 노말하게 출력
                else:
                    c_file.writelines("\t" + str_type + " " + str(value) + get_initial_value(str_type) + ";\n")
                next_line(c_file)

            c_file.writelines("};\n")

        # struct_path : ex) "/Script/project_name.TestTable"
        # unreal_struct_path = "/Script/" + project_name + "." + file_name
        print("SUCCESS -------------")


# 실행
create_struct()

print("\t** Struct Generator Finished. **")
