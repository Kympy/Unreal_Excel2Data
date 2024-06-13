
#include "DataTableMakerCommand.h"

// NSLOCTEXT( 로컬라이징된 네임스페이스 (모듈이름 등등), 텍스트 식별할 키, 실제 텍스트)
FDataTableMakerCommand::FDataTableMakerCommand() : TCommands("DGExcel2Data", NSLOCTEXT("DGExcel2Data", "GenerateDataTable", "Generate Data Table"), NAME_None, FAppStyle::GetAppStyleSetName())
{
}

void FDataTableMakerCommand::RegisterCommands()
{
// UI_COMMAND 사용하려면 LOCTEXT_NAMESPACE 정의가 필요함 - "" 로 설정 시 특정 네임 스페이스에 속하지 않게 가능 
#define LOCTEXT_NAMESPACE "DGExcel2Data"

	UI_COMMAND(Cmd_MakeStruct, "Make data table struct", "Make C++ sturct", EUserInterfaceActionType::Button, FInputGesture());
	UI_COMMAND(Cmd_MakeAsset, "Make data table asset", "Make data table asset", EUserInterfaceActionType::Button, FInputGesture());
	UI_COMMAND(Cmd_CreateFolder, "Create folder", "Create folder", EUserInterfaceActionType::Button, FInputGesture());

#undef LOCTEXT_NAMESPACE
}
