import unreal as u,json
from pathlib import Path
out={}
for name in ['DynamicZero','MasterOff','UVPixel','UVVertex']:
 m=u.EditorAssetLibrary.load_asset('/Game/Lab/M_'+name);assert m
 s=u.MaterialEditingLibrary.get_statistics(m)
 out[name]={'pixel_instructions':s.num_pixel_shader_instructions,'vertex_instructions':s.num_vertex_shader_instructions,'interpretation':'Editor API snapshot; zero can mean unavailable. Verify target Platform Stats.'}
Path(u.Paths.project_saved_dir(),'ShaderLogic/Editor-Stats.json').write_text(json.dumps(out,indent=2))
u.log('SHADER_STATS_SNAPSHOT_PASS')
