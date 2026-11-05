using UnrealBuildTool;
public class MaterialCostLab : ModuleRules
{
    public MaterialCostLab(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PrivateDependencyModuleNames.AddRange(new[] { "Core", "CoreUObject", "Engine" });
    }
}
