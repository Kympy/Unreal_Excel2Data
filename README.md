## UE5 Excel -> Data Table Asset Converter

.Net Framework 4.8 / C# 7.3

Unreal 5 Python plugin

---

### KOR
  + Python 폴더를 언리얼 프로젝트 Content/ 하위에 복사
  + Source 폴더를 언리얼 프로젝트 Source 폴더에 복사
  + 언리얼 프로젝트 ProjectNameEditor.Target.cs 에서 "DGExcel2Data" 모듈 추가
  + ProjectName.uproject 에 Module 란에 "DGExcel2Data" 추가

2024.11.29 Update
  + 빈 셀을 제거하여 CSV 로 만들고 Temp 폴더에 저장하도록 수정
  + Temp 에 저장된 CSV 를 실 리소스 CSV 로 필요한 부분만 추출하여 Content 하위에 저장
  + 각 셀의 데이터를 모두 "" 따옴표로 묶음.
  + 기존의 Asset Generator 가 더이상 사용되지 않고, CSV 를 런타임에 읽어 UDataTable 을 메모리에 올려 사용한다.
 
### ENG
  + Copy Python folder to Content/ folder in your project.
  + Copy Source folder to your project's Source folder.
  + Add "DGExcel2Data" in your ProjectNameEditor.Target.cs
  + Add "DGExcel2Data" in your ProjectName.uproject

### Target.cs
![image](https://github.com/Kympy/Unreal_Excel2Data/assets/65384983/282cd628-e010-4b1f-b912-fa82a21bad05)

### .uproject
![image](https://github.com/Kympy/Unreal_Excel2Data/assets/65384983/7c0755d2-3826-4bab-8edf-80075ed6b214)



