using UnrealBuildTool;
public class MaterialCostLabTarget : TargetRules
{
    public MaterialCostLabTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V6;
        ExtraModuleNames.Add("MaterialCostLab");
    }
}

