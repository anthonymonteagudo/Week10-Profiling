import unreal as ue
for mode in ("Lean","MasterOff","MasterOn"):
    mat=ue.EditorAssetLibrary.load_asset("/Game/Lab/M_"+mode)
    assert mat
    stat=ue.MaterialEditingLibrary.get_statistics(mat)
    ue.log_warning(f"LAB_SHADER_STATS {mode} pixel={stat.num_pixel_shader_instructions} vertex={stat.num_vertex_shader_instructions}")
