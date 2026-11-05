"""Editor tools: audit loaded content, inspect a temporary overlay, export evidence.

No asset/property changes, automatic fixes, shader replacements or asset saves.
The overlay draws short-lived primitives and unregisters its callback when disabled.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,time,webbrowser,math
import unreal
from week10_report import write_dashboard,summarize_capture

_overlay_handle=None
_overlay_world=None
_last_report=None
_last_dashboard=None
_next_overlay_draw=0.0


def prop(obj,name,default=None):
    try:return obj.get_editor_property(name)
    except Exception:return default


def vec(v):return [float(v.x),float(v.y),float(v.z)]


def scan_world():
    started=time.perf_counter()
    config=json.loads((Path(__file__).parent/'audit_rules.json').read_text(encoding='utf-8'))
    world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    if not world:raise RuntimeError('Open a map in the editor before running the audit.')
    actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
    mesh_editor=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
    findings=[];overlay=[];inventory={'actors':len(actors),'lights':0,'meshes':0,'niagara':0,'translucent_components':0,'unique_mesh_assets':0}
    checks={'LIGHT_RADIUS':0,'LIGHT_DISTANCE':0,'MOVABLE_SHADOW':0,'MESH_DENSITY':0,'FALLBACK_DENSITY':0,'EMPTY_MATERIAL':0,'NIAGARA_EFFECT_TYPE':0,'TRANSLUCENT_STACK':0,'SHADOW_CACHE_ALWAYS':0,'MATERIAL_DUPLICATES':0}
    coverage=[];mesh_cache={};translucent=[];material_groups={}
    def finding(actor,component,rule,severity,observed,limit,reason,next_check,asset=None):
        tags={str(t) for t in prop(actor,'tags',[])}
        ignored=f'OptAudit.Ignore.{rule}' in tags
        uid=f'{rule}|{component.get_path_name()}'
        findings.append({'id':uid,'rule':rule,'severity':severity,'status':'exception' if ignored else 'review','actor':actor.get_actor_label(),'actor_path':actor.get_path_name(),'component':component.get_path_name(),'asset':asset,'observed':observed,'policy':limit,'reason':reason,'next_check':next_check})
        if not ignored:
            origin,extent,_=unreal.SystemLibrary.get_component_bounds(component)
            overlay.append({'actor':actor.get_actor_label(),'actor_path':actor.get_path_name(),'center':vec(origin),'extent':[max(8,v) for v in vec(extent)],'severity':severity,'rule':rule})
    for actor in actors:
        for c in actor.get_components_by_class(unreal.LightComponent):
            inventory['lights']+=1
            if not prop(c,'affects_world',True):continue
            if isinstance(c,unreal.LocalLightComponent):
                radius=prop(c,'attenuation_radius',0.0);distance=prop(c,'max_draw_distance',0.0)
                checks['LIGHT_RADIUS']+=1;checks['LIGHT_DISTANCE']+=1
                if radius>config['light_radius_cm']:
                    finding(actor,c,'LIGHT_RADIUS','warning',radius,config['light_radius_cm'],'Large authored influence radius in cm.','Isolate light; preserve focal/contact quality; compare the relevant Lit GPU pass.')
                if distance==0:
                    finding(actor,c,'LIGHT_DISTANCE','info',distance,'Authored distance cutoff is nonzero unless intentionally exempt','No authored max distance. Engine screen-size culling may still operate.','Walk the intended route; test Max Draw Distance and fade with gameplay cues intact.')
            checks['MOVABLE_SHADOW']+=1
            if prop(c,'cast_shadows',False) and prop(c,'mobility')==unreal.ComponentMobility.MOVABLE:
                finding(actor,c,'MOVABLE_SHADOW','warning','Movable, casts shadows','Inspect significance and shadow-cache behavior','Potential recurring light/shadow workload.','Check shadow/contact requirements and cached pages; time the relevant pass before editing.')
        for c in actor.get_components_by_class(unreal.StaticMeshComponent):
            mesh=prop(c,'static_mesh')
            if not mesh:continue
            inventory['meshes']+=1;key=mesh.get_path_name()
            if key not in mesh_cache:
                count=mesh.get_num_lods() if hasattr(mesh,'get_num_lods') else (mesh_editor.get_lod_count(mesh) if mesh_editor else unreal.EditorStaticMeshLibrary.get_lod_count(mesh))
                triangles=mesh.get_num_triangles(0) if count>0 else None
                settings=prop(mesh,'nanite_settings')
                mesh_cache[key]={'nanite':bool(prop(settings,'enabled',False)) if settings else False,'lods':count,'triangles':triangles}
            data=mesh_cache[key];triangles=data['triangles']
            checks['SHADOW_CACHE_ALWAYS']+=1
            if prop(c,'shadow_cache_invalidation_behavior')==unreal.ShadowCacheInvalidationBehavior.ALWAYS:
                finding(actor,c,'SHADOW_CACHE_ALWAYS','warning','Always invalidate','Auto unless animation requires forced invalidation','Forces shadow-cache invalidation even without known transform/material changes.','Inspect motion and WPO. Test Auto on static props; compare VSM work and moving-view shadows.',key)

            checks['MESH_DENSITY']+=1;checks['FALLBACK_DENSITY']+=1
            if triangles is not None and triangles>config['mesh_lod0_triangles'] and not data['nanite']:
                finding(actor,c,'MESH_DENSITY','warning',triangles,config['mesh_lod0_triangles'],'Dense conventional LOD0 render data.','Inspect silhouette, LOD transitions, platform support and measured geometry cost.',key)
            if triangles is not None and triangles>config['fallback_triangles'] and data['nanite']:
                finding(actor,c,'FALLBACK_DENSITY','warning',triangles,config['fallback_triangles'],'Nanite-enabled asset still has dense conventional render/fallback data.','Inspect fallback target, ray-tracing path and collision users. This is not the count of visible Nanite triangles.',key)
            for index in range(c.get_num_materials()):
                checks['EMPTY_MATERIAL']+=1
                material=c.get_material(index)
                if material is None:
                    finding(actor,c,'EMPTY_MATERIAL','warning',f'Slot {index}: None','Authored material or documented default','Empty slot uses an engine/default result.','Check that the intended surface appearance survived import and reimport.',key)
                    continue

                checks['MATERIAL_DUPLICATES']+=1
                if isinstance(material,unreal.MaterialInstanceConstant):
                    parent=prop(material,'parent')
                    # Inspect exposed parameter overrides. Other material property differences require manual review.
                    overrides=any(prop(material,n,[]) for n in ['scalar_parameter_values','vector_parameter_values','texture_parameter_values','static_switch_parameter_values'])
                    if parent and not overrides:
                        material_groups.setdefault(parent.get_path_name(),[]).append((actor,c,material.get_path_name()))
                base=material.get_base_material()
                if prop(base,'blend_mode') in [unreal.BlendMode.BLEND_TRANSLUCENT,unreal.BlendMode.BLEND_ADDITIVE,unreal.BlendMode.BLEND_ALPHA_COMPOSITE]:
                    translucent.append((actor,c,material.get_path_name()));break
        if hasattr(unreal,'NiagaraComponent'):
            for c in actor.get_components_by_class(unreal.NiagaraComponent):
                inventory['niagara']+=1
                try:asset=c.get_asset()
                except Exception:asset=prop(c,'asset')
                if not asset:
                    coverage.append({'actor':actor.get_actor_label(),'check':'NIAGARA_EFFECT_TYPE','status':'unavailable','reason':'System asset unavailable to Python.'});continue
                checks['NIAGARA_EFFECT_TYPE']+=1
                # Reflection can distinguish unsupported property access from an empty value.
                try:effect_type=asset.get_editor_property('effect_type')
                except Exception:
                    coverage.append({'actor':actor.get_actor_label(),'check':'NIAGARA_EFFECT_TYPE','status':'unavailable','reason':'Effect Type not exposed in this build.'});continue
                if effect_type is None:
                    finding(actor,c,'NIAGARA_EFFECT_TYPE','warning','None','Assigned Effect Type or documented override policy','System has no shared Effect Type.','Inspect system/emitter/renderer overrides; test bounds, update frequency and cull reaction.',asset.get_path_name())
    for parent,items in material_groups.items():
        distinct=len({item[2] for item in items})
        if distinct>=8:
            seen=set()
            for actor,c,material_path in items:
                if c.get_path_name() in seen:continue
                seen.add(c.get_path_name())
                finding(actor,c,'MATERIAL_DUPLICATES','info',distinct,'Inspect 8+ no-override children sharing one parent','Repeated equivalent material-instance assets may prevent sharing.','Compare parameters, switches and overrides; test reusing parent and inspect draw submissions. Nanite/material paths can limit the result.',parent)
    # Project component bounds into the authored Audit Camera. This approximates
    # possible screen coverage; it is not a rasterized pixel-overdraw measurement.
    inventory['translucent_components']=len(translucent);inventory['unique_mesh_assets']=len(mesh_cache)
    checks['TRANSLUCENT_STACK']=len(translucent)
    cameras=[a for a in actors if isinstance(a,unreal.CameraActor)]
    camera=next((a for a in cameras if 'audit' in a.get_actor_label().lower()),cameras[0] if cameras else None)
    def screen_rect(component):
        if not camera:return None
        origin,extent,_=unreal.SystemLibrary.get_component_bounds(component)
        rotation=camera.get_actor_rotation();location=camera.get_actor_location()
        forward=unreal.MathLibrary.get_forward_vector(rotation);right=unreal.MathLibrary.get_right_vector(rotation);up=unreal.MathLibrary.get_up_vector(rotation)
        lens=camera.get_component_by_class(unreal.CameraComponent);tan=math.tan(math.radians(lens.field_of_view)/2);aspect=lens.aspect_ratio
        points=[]
        for x in [-1,1]:
            for y in [-1,1]:
                for z in [-1,1]:
                    point=unreal.Vector(origin.x+x*extent.x,origin.y+y*extent.y,origin.z+z*extent.z)-location
                    depth=point.dot(forward)
                    if depth<=1:return None
                    points.append((point.dot(right)/(depth*tan),point.dot(up)*aspect/(depth*tan)))
        rect=[max(-1,min(p[0] for p in points)),max(-1,min(p[1] for p in points)),min(1,max(p[0] for p in points)),min(1,max(p[1] for p in points))]
        return rect if rect[0]<rect[2] and rect[1]<rect[3] else None
    rectangles={c.get_path_name():screen_rect(c) for _,c,_ in translucent}
    for actor,c,mat in translucent:
        a=rectangles[c.get_path_name()]
        if not a:continue
        intersecting=sum(bool(b and a[0]<=b[2] and b[0]<=a[2] and a[1]<=b[3] and b[1]<=a[3]) for b in rectangles.values())
        if intersecting>=config['translucent_actor_warning_count']:
            finding(actor,c,'TRANSLUCENT_STACK','warning',intersecting,config['translucent_actor_warning_count'],'Projected translucent bounds overlap from '+camera.get_actor_label()+', including this component.','Inspect actual surfaces and pixel overlap; compare Lit translucency timing. Projected bounds are only a broad-phase candidate.',mat)
    if translucent and not camera:coverage.append({'actor':'World','check':'TRANSLUCENT_STACK','status':'unavailable','reason':'No authored CameraActor available for projection.'})
    # One box per actor, highest severity; never rescan content on the tick callback.
    severity={'info':0,'warning':1,'error':2};boxes={}
    for item in overlay:
        old=boxes.get(item['actor_path'])
        if not old or severity[item['severity']]>severity[old['severity']]:boxes[item['actor_path']]=item
    return {'schema_version':1,'title':'Week 10 Optimization Audit','created_utc':datetime.now(timezone.utc).isoformat(),'engine':unreal.SystemLibrary.get_engine_version(),'project':Path(unreal.Paths.project_dir()).name,'map':world.get_path_name(),'scope':'Loaded editor world only. Unloaded cells and runtime-spawned actors are excluded. Editor Niagara counts are not live particle counts.','interpretation':'Policy findings identify inspection candidates. They do not measure runtime milliseconds or prove a bottleneck.','inventory':inventory,'checks':checks,'coverage':coverage,'rules':config,'findings':findings,'overlay':list(boxes.values())[:config['overlay_max_actors']],'overlay_total':len(boxes),'scan_ms':1000*(time.perf_counter()-started),'captures':[]}


def run_audit(open_browser=True,capture_paths=None,start=190,stop=395):
    global _last_report,_last_dashboard
    _last_report=scan_world()
    _last_report['captures']=[summarize_capture(p,start,stop) for p in (capture_paths or [])]
    folder=Path(unreal.Paths.project_saved_dir()).resolve()/'Week10Optimization'
    _last_dashboard=write_dashboard(_last_report,folder)
    unreal.log(f"Week 10 optimization: {len(_last_report['findings'])} candidates; {_last_dashboard}")
    if open_browser:webbrowser.open(_last_dashboard.as_uri())
    return _last_report


def _draw_overlay(delta=0.0):
    global _overlay_world,_next_overlay_draw
    world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    if world != _overlay_world:
        disable_overlay();return
    now=time.monotonic()
    if now<_next_overlay_draw:return
    _next_overlay_draw=now+.20
    colors={'info':unreal.LinearColor(.1,.7,1,1),'warning':unreal.LinearColor(1,.55,.08,1),'error':unreal.LinearColor(1,.1,.15,1)}
    for item in (_last_report or {}).get('overlay',[]):
        unreal.SystemLibrary.draw_debug_box(world,unreal.Vector(*item['center']),unreal.Vector(*item['extent']),colors[item['severity']],duration=.25,thickness=3.0,depth_priority=unreal.DrawDebugSceneDepthPriorityGroup.FOREGROUND)


def enable_overlay():
    global _overlay_handle,_overlay_world,_next_overlay_draw
    if _overlay_handle is not None: disable_overlay()
    run_audit(False)
    _overlay_world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    _next_overlay_draw=0.0
    _overlay_handle=unreal.register_slate_post_tick_callback(_draw_overlay)
    unreal.log('Custom Optimization View enabled. Blue = information; amber = review; red = error. Bounds are cached; toggle to refresh after edits. Turn on viewport Realtime. Disable before profiling.')
    return _last_report


def disable_overlay():
    global _overlay_handle,_overlay_world
    if _overlay_handle is not None:unreal.unregister_slate_post_tick_callback(_overlay_handle)
    _overlay_handle=None;_overlay_world=None
    unreal.log('Custom Optimization View disabled. Marks expire within 0.25 seconds. No materials or scene properties were changed.')


def toggle_overlay():
    if _overlay_handle is None:return enable_overlay()
    disable_overlay()


def open_dashboard():
    folder=Path(unreal.Paths.project_saved_dir()).resolve()/'Week10Optimization/index.html'
    if not folder.exists():run_audit(False)
    webbrowser.open(folder.as_uri())


def select_actor(actor_path):
    subsystem=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for actor in subsystem.get_all_level_actors():
        if actor.get_path_name()==actor_path:
            subsystem.set_selected_level_actors([actor]);return True
    unreal.log_warning('Actor is not loaded in the current editor world.');return False


def register_menu():
    menus=unreal.ToolMenus.get()
    owner='Week10Optimization'
    menus.unregister_owner_by_name(owner)
    root=menus.extend_menu('LevelEditor.MainMenu.Tools')
    menu=root.add_sub_menu(owner,'Week10Optimization','Week10OptimizationMenu','Week 10 Optimization','Audit candidates, inspect the custom view, and generate a dashboard.')
    for name,label,call in [('Audit','Validate and Generate Dashboard','run_audit()'),('View','Toggle Custom Optimization View','toggle_overlay()'),('Restore','Disable Custom Optimization View','disable_overlay()'),('Dashboard','Open Last Dashboard','open_dashboard()')]:
        entry=unreal.ToolMenuEntry(name=owner+name,type=unreal.MultiBlockType.MENU_ENTRY)
        entry.set_label(label)
        entry.set_string_command(unreal.ToolMenuStringCommandType.PYTHON,'',f'import week10_optimization; week10_optimization.{call}')
        menu.add_menu_entry('Optimization',entry)
    menus.refresh_all_widgets()
    unreal.log('Week 10 Optimization menu registered under Tools.')
