// Copyright RottenPotato


#include "DGExcel2Data.h"
#include "LevelEditor.h"
#include "Commands/DataTableMakerCommand.h"

IMPLEMENT_MODULE(FDGExcel2Data, DGExcel2Data)void FDGExcel2Data::StartupModule()
{
	UE_LOG(LogTemp, Log, TEXT("DGExcel2Data Module Started"));
	// 커맨드 생성
	TSharedPtr<FUICommandList> GenerateDataTableCommand = MakeShareable(new FUICommandList);
	if (!GenerateDataTableCommand)
	{
		UE_LOG(LogTemp, Error, TEXT("New FUICommandList failed."));
		return;
	}

	FDataTableMakerCommand::Register();
	
	// 액션 맵핑
	GenerateDataTableCommand->MapAction(
		FDataTableMakerCommand::Get().Cmd_MakeStruct, 
FExecuteAction::CreateRaw(this, &FDGExcel2Data::MakeDataTableStruct), 
		FCanExecuteAction()
	);
	GenerateDataTableCommand->MapAction(
		FDataTableMakerCommand::Get().Cmd_MakeAsset,
		FExecuteAction::CreateRaw(this, &FDGExcel2Data::MakeDataTableAsset),
		FCanExecuteAction()
	);
	GenerateDataTableCommand->MapAction(
		FDataTableMakerCommand::Get().Cmd_CreateFolder,
		FExecuteAction::CreateRaw(this, &FDGExcel2Data::CreateFolders),
		FCanExecuteAction()
	);
	
	Extender = MakeShareable(new FExtender);

	// Extender->AddToolBarExtension(
	// 	"Settings",
	// 	EExtensionHook::Before,
	// 	GenerateDataTableCommand,
	// 	FToolBarExtensionDelegate::CreateRaw(this, &FCustomToolsModule::AddGenerateDataTableToolBar)
	// );

	Extender->AddMenuBarExtension(
		"Help",
		EExtensionHook::After,
		GenerateDataTableCommand,
		FMenuBarExtensionDelegate::CreateRaw(this, &FDGExcel2Data::AddMenuBar)
	);

	FLevelEditorModule& LevelEditorModule = FModuleManager::LoadModuleChecked<FLevelEditorModule>("LevelEditor");
	//LevelEditorModule.GetToolBarExtensibilityManager()->AddExtender(Extender);
	LevelEditorModule.GetMenuExtensibilityManager()->AddExtender(Extender);

	// TSharedRef<FGlobalTabmanager> TabManager = FGlobalTabmanager::Get();
	// TabManager->RegisterNomadTabSpawner("Custom Tools Tab", FOnSpawnTab::CreateRaw(this, &FCustomToolsModule::SpawnTab)).SetDisplayName(FText::FromString("Custom Tools"));
}

void FDGExcel2Data::ShutdownModule()
{
	IModuleInterface::ShutdownModule();

	if (Extender.IsValid())
	{
		FLevelEditorModule* LevelEditorModule = FModuleManager::GetModulePtr<FLevelEditorModule>("LevelEditor");
		if (LevelEditorModule)
		{
			LevelEditorModule->GetMenuExtensibilityManager()->RemoveExtender(Extender);
		}
		Extender.Reset();
	}
	

	FDataTableMakerCommand::Unregister();
}

// 툴바 만들 때 쓰는 함수 : 지금 안씀
void FDGExcel2Data::AddGenerateDataTableToolBar(FToolBarBuilder& ToolBarBuilder)
{
// 	UE_LOG(LogTemp, Log, TEXT("Successfully added custom tools tool bar button"));
//
// 	FSlateIcon IconBrush = FSlateIcon(FAppStyle::GetAppStyleSetName(), "LevelEditor.ViewOptions", "LevelEditor.ViewOptions.Small");
//
// 	ToolBarBuilder.AddToolBarButton(
// 		FDataTableMakerCommand::Get().Cmd_MakeStruct,
// 		NAME_None,
// FText::FromString("Custom Tools"),
// 		FText::FromString("This is custom tools"),
// 		IconBrush,
// 		NAME_None
// 	);
}

void FDGExcel2Data::AddMenuBar(FMenuBarBuilder& MenuBarBuilder)
{
	MenuBarBuilder.AddPullDownMenu(
		FText::FromString("DGExcel2Data"),
		FText::FromString("Convert Excel file to csv and generate c++ struct file and data table assets."),
		FNewMenuDelegate::CreateRaw(this, &FDGExcel2Data::FillMenu)
	);
}

void FDGExcel2Data::FillMenu(FMenuBuilder& MenuBuilder)
{
	MenuBuilder.BeginSection("Data Table");
	{
		MenuBuilder.AddMenuEntry(
			FDataTableMakerCommand::Get().Cmd_MakeStruct,
			NAME_None,
			FText::FromString("1. Make Data Table C++ Struct"),
			FText::FromString("Make data table c++ struct. *FIRST*"),
			FSlateIcon()
		);
		MenuBuilder.AddMenuEntry(
			FDataTableMakerCommand::Get().Cmd_MakeAsset,
			NAME_None,
			FText::FromString("2. Make Data Table Asset"),
			FText::FromString("Make data table asset from struct."),
			FSlateIcon()
		);
		MenuBuilder.AddMenuEntry(
			FDataTableMakerCommand::Get().Cmd_CreateFolder,
			NAME_None,
			FText::FromString("Create Folders"),
			FText::FromString("Create necessary folders."),
			FSlateIcon()
		);
	}
	MenuBuilder.EndSection();
}

// 지금 안씀
TSharedRef<SDockTab> FDGExcel2Data::SpawnTab(const FSpawnTabArgs& TabSpawnArgs)
{
	TSharedRef<SDockTab> SpawendTab = SNew(SDockTab).TabRole(ETabRole::NomadTab)
	[
		SNew(SButton)
			.Text(FText::FromString("DGExcel2Data")).ContentPadding(3)
	];

	return SpawendTab;
}

void FDGExcel2Data::MakeDataTableStruct()
{
	// TSharedRef<class FGlobalTabmanager> TabManager = FGlobalTabmanager::Get();
	// TabManager->TryInvokeTab(FTabId("Custom Tools Tab"));
	UE_LOG(LogTemp, Log, TEXT(" "))
	UE_LOG(LogTemp, Log, TEXT("------------------------------"))
	UE_LOG(LogTemp, Log, TEXT("----- [DGExcel2Data] Make Excel To CSV AND C++ STRUCT -----"))
	UE_LOG(LogTemp, Log, TEXT(" "))
	
	FString PythonScriptPath = FPaths::Combine(FPaths::ProjectContentDir(), "Python", "DGExcel2Data", "excel2csv.py");
	PythonScriptPath = FPaths::ConvertRelativePathToFull(PythonScriptPath);
	PythonScriptPath.InsertAt(0, "py ");
	GEngine->Exec(nullptr, *PythonScriptPath);
	
	PythonScriptPath = FPaths::Combine(FPaths::ProjectContentDir(), "Python", "DGExcel2Data", "struct_generator.py");
	PythonScriptPath = FPaths::ConvertRelativePathToFull(PythonScriptPath);
	PythonScriptPath.InsertAt(0, "py ");
	GEngine->Exec(nullptr, *PythonScriptPath);
		
	UE_LOG(LogTemp, Log, TEXT(" "))
	UE_LOG(LogTemp, Log, TEXT(" "))
	UE_LOG(LogTemp, Log, TEXT("------------------------------"))
}

void FDGExcel2Data::MakeDataTableAsset()
{
	UE_LOG(LogTemp, Log, TEXT(" "))
	UE_LOG(LogTemp, Log, TEXT("------------------------------"))
	UE_LOG(LogTemp, Log, TEXT("----- [DGExcel2Data] Make Data Table Asset -----"))
	UE_LOG(LogTemp, Log, TEXT(" "))
	
	FString PythonScriptPath = FPaths::Combine(FPaths::ProjectContentDir(), "Python", "DGExcel2Data", "asset_generator.py");
	PythonScriptPath = FPaths::ConvertRelativePathToFull(PythonScriptPath);
	PythonScriptPath.InsertAt(0, "py ");
	GEngine->Exec(nullptr, *PythonScriptPath);
	
	UE_LOG(LogTemp, Log, TEXT(" "))
	UE_LOG(LogTemp, Log, TEXT(" "))
	UE_LOG(LogTemp, Log, TEXT("------------------------------"))
}

void FDGExcel2Data::CreateFolders()
{
	UE_LOG(LogTemp, Log, TEXT(" "))
	UE_LOG(LogTemp, Log, TEXT("------------------------------"))
	UE_LOG(LogTemp, Log, TEXT("----- [DGExcel2Data] Create Folders -----"))
	UE_LOG(LogTemp, Log, TEXT(" "))
	FString ExcelFolder = FPaths::Combine(FPaths::ProjectDir(), "Excel");
	if (FPaths::DirectoryExists(ExcelFolder) == false)
	{
		IPlatformFile& PlatformFile = FPlatformFileManager::Get().GetPlatformFile();
		if (PlatformFile.CreateDirectory(*ExcelFolder))
		{
			UE_LOG(LogTemp, Log, TEXT("Excel folder is created."))
		}
		else
		{
			UE_LOG(LogTemp, Log, TEXT("Excel folder creation is failed."))
		}
	}
	else
	{
		UE_LOG(LogTemp, Log, TEXT("Excel folder is already exists."))
	}
	UE_LOG(LogTemp, Log, TEXT(" "))
	UE_LOG(LogTemp, Log, TEXT(" "))
	UE_LOG(LogTemp, Log, TEXT("------------------------------"))
}

