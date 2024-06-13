
using UnrealBuildTool;

public class DGExcel2Data : ModuleRules
{
	public DGExcel2Data(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
		});
        PrivateDependencyModuleNames.AddRange(new string[] {
            "Slate",
            "SlateCore", 
            "EditorStyle"
        });
	}
}