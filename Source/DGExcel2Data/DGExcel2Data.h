// Copyright RottenPotato

#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleInterface.h"

class FDGExcel2Data : public IModuleInterface
{

public:
	// 모듈 시작 시 생성한 Extender -> 해제 시 필요함.
	TSharedPtr<FExtender> Extender;
	
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
	
	void AddGenerateDataTableToolBar(FToolBarBuilder& ToolBarBuilder);
	void AddMenuBar(FMenuBarBuilder& MenuBarBuilder);

	void FillMenu(FMenuBuilder& MenuBuilder);

	TSharedRef<SDockTab> SpawnTab(const FSpawnTabArgs& TabSpawnArgs);
	
	void MakeDataTableStruct();
	void MakeDataTableAsset();
	void CreateFolders();
};

