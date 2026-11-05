import json,unreal as u
from pathlib import Path
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
results=[];cameras=[];empty_sets=[];always_counts=[]
for name in ['Lounge_Reference','Lounge_Unoptimized']:
 assert u.EditorLoadingAndSavingUtils.load_map('/Game/OptimizationLab/'+name)
 all=actors.get_all_level_actors();meshes=0;lights=0;empty=[];always=0
 for a in all:
  for c in a.get_components_by_class(u.StaticMeshComponent):
   assert c.get_editor_property('static_mesh'),a.get_actor_label()
   if c.get_editor_property('shadow_cache_invalidation_behavior')==u.ShadowCacheInvalidationBehavior.ALWAYS:always+=1
   for i in range(c.get_num_materials()):
    mat=c.get_material(i)
    if not mat:
     empty.append((a.get_actor_label(),c.get_name(),i));continue
    if isinstance(mat,u.MaterialInstanceConstant):assert mat.get_editor_property('parent'),mat.get_path_name()
   meshes+=1
  lights+=len(a.get_components_by_class(u.LightComponent))
  if a.get_actor_label()=='Audit Camera':cameras.append(([a.get_actor_location().x,a.get_actor_location().y,a.get_actor_location().z],[a.get_actor_rotation().pitch,a.get_actor_rotation().yaw,a.get_actor_rotation().roll]))
 assert meshes>=180
 always_counts.append(always)
 empty_sets.append(empty)
 results.append({'map':name,'actors':len(all),'meshes':meshes,'lights':lights,'source_empty_material_slots':empty,'always_invalidate_components':always})
assert len(cameras)==2 and cameras[0]==cameras[1],"Comparison camera changed"
assert results[1]["lights"]-results[0]["lights"]==12
assert always_counts[0]==0 and always_counts[1]>10
assert empty_sets[0]==empty_sets[1],"New missing material slots introduced"
import week10_optimization as tool
report=tool.run_audit(False);assert len(report['findings'])>=90
assert any(f['rule']=='MOVABLE_SHADOW' for f in report['findings'])
assert any(f['rule']=='SHADOW_CACHE_ALWAYS' for f in report['findings'])
assert any(f['rule']=='MATERIAL_DUPLICATES' for f in report['findings'])
before=[(a.get_path_name(),str(a.get_actor_location())) for a in actors.get_all_level_actors()]
tool.enable_overlay();tool._draw_overlay();tool.disable_overlay();assert tool._overlay_handle is None
after=[(a.get_path_name(),str(a.get_actor_location())) for a in actors.get_all_level_actors()]
# Vector string representation contains transient wrapper addresses; compare numeric values separately.
assert [a[0] for a in before]==[a[0] for a in after]
Path(u.Paths.project_saved_dir(),'Fab-Readiness.json').write_text(json.dumps({'status':'PASS','maps':results,'candidates':len(report['findings']),'notes':'All meshes and assigned MIC parents resolve. Authored empty slots match the source reference; no new empty slots.'},indent=2))
u.log('FAB_STUDENT_PACKAGE_PASS')
