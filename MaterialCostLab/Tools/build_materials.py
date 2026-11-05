"""Create the isolated material lab assets with Unreal Editor Python."""
import unreal as ue

ROOT = "/Game/Lab"
assets = ue.EditorAssetLibrary
tools = ue.AssetToolsHelpers.get_asset_tools()
edit = ue.MaterialEditingLibrary

def material(name):
    path = f"{ROOT}/{name}"
    mat = assets.load_asset(path) if assets.does_asset_exist(path) else tools.create_asset(
        name, ROOT, ue.Material, ue.MaterialFactoryNew())
    assert mat, name
    edit.delete_all_material_expressions(mat)
    mat.set_editor_property("shading_model", ue.MaterialShadingModel.MSM_UNLIT)
    mat.set_editor_property("two_sided", True)
    return mat

def node(mat, cls, x, y):
    return edit.create_material_expression(mat, cls, x, y)

def constant(mat, value, x, y):
    item = node(mat, ue.MaterialExpressionConstant3Vector, x, y)
    item.set_editor_property("constant", ue.LinearColor(*value, 1))
    return item

def custom(mat, inputs, code, x, y):
    item = node(mat, ue.MaterialExpressionCustom, x, y)
    item.set_editor_property("output_type", ue.CustomMaterialOutputType.CMOT_FLOAT3)
    item.set_editor_property("code", code)
    properties = []
    for name, _ in inputs:
        prop = ue.CustomInput()
        prop.set_editor_property("input_name", name)
        properties.append(prop)
    item.set_editor_property("inputs", properties)
    for name, source in inputs:
        assert edit.connect_material_expressions(source, "", item, name), name
    return item

def finish(mat, source):
    assert edit.connect_material_property(source, "", ue.MaterialProperty.MP_EMISSIVE_COLOR)
    edit.recompile_material(mat)
    assert assets.save_loaded_asset(mat)

for label in ("CPD", "MID"):
    mat = material("M_" + label)
    parameter = node(mat, ue.MaterialExpressionScalarParameter, -540, 0)
    parameter.set_editor_property("parameter_name", "Variation")
    parameter.set_editor_property("use_custom_primitive_data", label == "CPD")
    parameter.set_editor_property("primitive_data_index", 0)
    color = custom(mat, [("Variation", parameter)],
                   "return lerp(float3(.035,.18,.57),float3(.75,.29,.025),Variation);", -230, 0)
    finish(mat, color)

base = (.13, .34, .58)
mat = material("M_Lean")
finish(mat, constant(mat, base, -330, 0))
for enabled in (False, True):
    mat = material("M_MasterOn" if enabled else "M_MasterOff")
    uv = node(mat, ue.MaterialExpressionTextureCoordinate, -680, 170)
    ripple = custom(mat, [("UV", uv)], """
    float2 p=UV*11.0;
    float wave=0;
    [unroll] for(int i=1; i<=24; ++i)
    {
        p += 0.18 * sin(p.yx * (0.32*i) + float2(0.75,1.4));
        wave += sin(p.x + p.y + 0.31*i);
    }
    return lerp(float3(.04,.13,.34),float3(.29,.68,.88),saturate(.5+wave/12.0));
    """, -410, 170)
    switch = node(mat, ue.MaterialExpressionStaticSwitchParameter, -170, 0)
    switch.set_editor_property("parameter_name", "EnableRipple")
    switch.set_editor_property("default_value", enabled)
    names=edit.get_material_expression_input_names(switch)
    ue.log_warning(f"LAB_SWITCH_INPUTS {names}")
    assert len(names) == 2, names
    assert edit.connect_material_expressions(ripple, "", switch, str(names[0]))
    assert edit.connect_material_expressions(constant(mat, base, -410, -30), "", switch, str(names[1]))
    finish(mat, switch)
ue.log_warning("MATERIAL_LAB_ASSETS_READY")
