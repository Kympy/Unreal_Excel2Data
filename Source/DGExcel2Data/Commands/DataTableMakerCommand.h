#pragma once

class FDataTableMakerCommand : public TCommands<FDataTableMakerCommand>
{
	
public:
	FDataTableMakerCommand();

	virtual void RegisterCommands() override;
	
	TSharedPtr<FUICommandInfo> Cmd_MakeStruct;
	TSharedPtr<FUICommandInfo> Cmd_MakeAsset;
	TSharedPtr<FUICommandInfo> Cmd_CreateFolder;
};
