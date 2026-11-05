"""Add equivalent-output shader experiments without changing the C++ runtime loader."""
from pathlib import Path
import runpy,unreal as ue
ctx={}
exec(compile(Path(__file__).with_name('build_materials.py').read_text().split('for label in')[0], 'build_materials.py', 'exec'),ctx)
material,node,constant,custom,finish=[ctx[k] for k in ('material','node','constant','custom','finish')]
edit=ue.MaterialEditingLibrary;assets=ue.EditorAssetLibrary
mat=material('M_DynamicZero')
uv=node(mat,ue.MaterialExpressionTextureCoordinate,-700,180)
weight=node(mat,ue.MaterialExpressionScalarParameter,-700,-100);weight.set_editor_property('parameter_name','RippleWeight');weight.set_editor_property('default_value',0.0)
color=custom(mat,[('UV',uv),('Weight',weight)],'''
float2 p=UV*11.0;float wave=0;
[unroll] for(int i=1;i<=24;++i){p+=.18*sin(p.yx*(.32*i)+float2(.75,1.4));wave+=sin(p.x+p.y+.31*i);}
float3 ripple=lerp(float3(.04,.13,.34),float3(.29,.68,.88),saturate(.5+wave/12.0));
return lerp(float3(.13,.34,.58),ripple,Weight);
''',-350,0)
finish(mat,color)
tex=assets.load_asset('/Game/Lab/T_UVChecker') if assets.does_asset_exist('/Game/Lab/T_UVChecker') else None
if not tex:
 task=ue.AssetImportTask();task.set_editor_property('filename',str(Path(__file__).with_name('Inputs')/'UV-Checker.png'));task.set_editor_property('destination_path','/Game/Lab');task.set_editor_property('destination_name','T_UVChecker');task.set_editor_property('automated',True);task.set_editor_property('save',True);ue.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);tex=assets.load_asset('/Game/Lab/T_UVChecker')
assert tex

for vertex in [False,True]:
 mat=material('M_UVVertex' if vertex else 'M_UVPixel')
 uv=node(mat,ue.MaterialExpressionTextureCoordinate,-850,0)
 scale=node(mat,ue.MaterialExpressionMultiply,-650,0);scale.set_editor_property('const_b',8.0);assert edit.connect_material_expressions(uv,'',scale,'A')
 offset=node(mat,ue.MaterialExpressionConstant2Vector,-650,150);offset.set_editor_property('r',.23);offset.set_editor_property('g',.17)
 add=node(mat,ue.MaterialExpressionAdd,-440,0);assert edit.connect_material_expressions(scale,'',add,'A');assert edit.connect_material_expressions(offset,'',add,'B')
 sample=node(mat,ue.MaterialExpressionTextureSample,-140,0);sample.set_editor_property('texture',tex)
 if vertex:
  interpolator=node(mat,ue.MaterialExpressionVertexInterpolator,-360,-180)
  assert edit.connect_material_expressions(add,'',interpolator,str(edit.get_material_expression_input_names(interpolator)[0]))
  assert edit.connect_material_expressions(interpolator,'',sample,'UVs')
 else:assert edit.connect_material_expressions(add,'',sample,'UVs')
 assert edit.connect_material_property(sample,'RGB',ue.MaterialProperty.MP_EMISSIVE_COLOR)
 edit.recompile_material(mat);assert assets.save_loaded_asset(mat)
ue.log('SHADER_EXPERIMENT_ASSETS_PASS')
