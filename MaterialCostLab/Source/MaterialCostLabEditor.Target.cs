using UnrealBuildTool;
public class MaterialCostLabEditorTarget : TargetRules
{
    public MaterialCostLabEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V6;
        ExtraModuleNames.Add("MaterialCostLab");
    }
}

