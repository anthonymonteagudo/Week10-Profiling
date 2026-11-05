"""Build the faulty lab from the locally installed Fab Cigar Room. Source remains untouched."""
from pathlib import Path
import json,unreal as u
levels=u.get_editor_subsystem(u.LevelEditorSubsystem);actors=u.get_editor_subsystem(u.EditorActorSubsystem);assets=u.EditorAssetLibrary
assert u.EditorLoadingAndSavingUtils.load_map('/Game/Cigar_room/Maps/Cigar_room')
assert not assets.does_asset_exist('/Game/OptimizationLab/Lounge_Reference'), 'Lab already exists. Use a fresh project copy to rebuild; your edits were preserved.'
assert not assets.does_asset_exist('/Game/OptimizationLab/Lounge_Unoptimized'), 'Lab already exists; your edits were preserved.'
# Fixed camera is identical in both variants; editor / debug camera provides exploration.
for a in actors.get_all_level_actors():
 if isinstance(a,u.CameraActor):a.set_editor_property('auto_activate_for_player',u.AutoReceiveInput.DISABLED)
a=actors.spawn_actor_from_class(u.CameraActor,u.Vector(545,-105,270),u.Rotator(pitch=-7,yaw=155,roll=0));a.set_actor_label('Audit Camera');a.set_editor_property('auto_activate_for_player',u.AutoReceiveInput.PLAYER0);a.get_component_by_class(u.CameraComponent).set_field_of_view(80)
u.EditorLevelLibrary.set_level_viewport_camera_info(a.get_actor_location(),a.get_actor_rotation())
assert u.EditorLoadingAndSavingUtils.save_map(u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(),'/Game/OptimizationLab/Lounge_Reference')
assert u.EditorLoadingAndSavingUtils.save_map(u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world(),'/Game/OptimizationLab/Lounge_Unoptimized')
assert u.EditorLoadingAndSavingUtils.load_map('/Game/OptimizationLab/Lounge_Unoptimized')
faults=[]
local=[]
for actor in list(actors.get_all_level_actors()):
 for c in actor.get_components_by_class(u.LocalLightComponent):
  record={'actor':actor.get_actor_label(),'component':c.get_name(),'fault':'oversized movable shadowed light','before':{'radius':c.get_editor_property('attenuation_radius'),'shadows':c.get_editor_property('cast_shadows'),'mobility':str(c.get_editor_property('mobility'))}}
  c.set_mobility(u.ComponentMobility.MOVABLE);c.set_attenuation_radius(1800);c.set_cast_shadows(True);c.set_editor_property('max_draw_distance',0.0)
  local.append((actor,c));faults.append(record)
# Redundant fill lights: common accumulated lighting-pass work, subtle image contribution.
for i,(owner,c) in enumerate(local[:12]):
 a=actors.spawn_actor_from_class(u.PointLight,c.get_world_location()+u.Vector(12,8,-10));a.set_actor_label('Interior Fill '+str(i+1));a.set_folder_path('Interior/Fill Lights')
 d=a.get_component_by_class(u.PointLightComponent);d.set_mobility(u.ComponentMobility.MOVABLE);d.set_intensity(float(c.get_editor_property('intensity'))*.06);d.set_attenuation_radius(1600);d.set_cast_shadows(True);d.set_light_color(c.get_light_color())
 faults.append({'actor':a.get_actor_label(),'fault':'redundant overlapping shadowed fill','reference':'actor absent'})
# Preserve real set dressing. Force full detail and retain distant small props.
count=0
for a in actors.get_all_level_actors():
 if not isinstance(a,u.StaticMeshActor):continue
 c=a.static_mesh_component;mesh=c.get_editor_property('static_mesh')
 if not mesh or not mesh.get_path_name().startswith('/Game/Cigar_room/'):continue
 if any(x in a.get_actor_label().lower() for x in ['book','bottle','glass','cigar','lighter','vase','lamp','bourbon']):
  c.set_editor_property('shadow_cache_invalidation_behavior',u.ShadowCacheInvalidationBehavior.ALWAYS);c.set_editor_property('forced_lod_model',0);c.set_editor_property('min_draw_distance',0.0);c.set_editor_property('ld_max_draw_distance',0.0)
  # Separate material instance assets reproduce per-prop material proliferation.
  for slot in range(c.get_num_materials()):
   mat=c.get_material(slot)
   if not mat:continue
   name=f'MI_InteriorProp_{count:03}_{slot}'
   instance=assets.load_asset('/Game/OptimizationLab/Materials/'+name) if assets.does_asset_exist('/Game/OptimizationLab/Materials/'+name) else u.AssetToolsHelpers.get_asset_tools().create_asset(name,'/Game/OptimizationLab/Materials',u.MaterialInstanceConstant,u.MaterialInstanceConstantFactoryNew())
   u.MaterialEditingLibrary.set_material_instance_parent(instance,mat);assert assets.save_loaded_asset(instance);c.set_material(slot,instance)
  faults.append({'actor':a.get_actor_label(),'fault':'unnecessary Always shadow invalidation; no distance policy; unique material instances','reference':'use Lounge_Reference actor properties'})
  count+=1
assert count>10
assert levels.save_current_level()
import week10_optimization as tool
report=tool.run_audit(False)
folder=Path(u.Paths.project_saved_dir()).resolve()/'LabSetup';folder.mkdir(parents=True,exist_ok=True)
(folder/'Fault-Key.json').write_text(json.dumps({'source':'https://www.fab.com/listings/4da78da6-44b3-4adf-8883-219fe17b44d4','map':'/Game/OptimizationLab/Lounge_Unoptimized','faults':faults,'inventory':report['inventory'],'audit_candidates':len(report['findings']),'note':'Faults are teaching edits. Reference is original vendor layout plus camera, not a certified performance target. Measure actual costs.'},indent=2),encoding='utf-8')
u.log('FAB_LOUNGE_BUILD_PASS')


