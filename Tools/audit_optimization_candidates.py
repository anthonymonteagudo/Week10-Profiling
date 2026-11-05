"""Read-only loaded-world inventory for Week 10. Run in Unreal 5.7's Python console.

Only writes a JSON report under Saved/Week10Audit. It never saves or changes assets.
An audit flag is an investigation candidate, not proof of a performance problem.
"""
import json
from pathlib import Path
import unreal


def property_value(obj, name):
    try:
        value = obj.get_editor_property(name)
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return str(value)
    except Exception:
        return {"unavailable": name}


def audit_world():
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
    lights, meshes, effects = [], [], []
    for actor in actors:
        identity = {"actor": actor.get_actor_label(), "actor_path": actor.get_path_name()}
        for component in actor.get_components_by_class(unreal.LightComponent):
            fields = ["cast_shadows", "affects_world", "mobility"]
            if isinstance(component, unreal.LocalLightComponent):
                fields += ["attenuation_radius", "max_draw_distance", "max_distance_fade_range"]
            values = {key: property_value(component, key) for key in fields}
            candidates = []
            if values.get("max_draw_distance") == 0:
                candidates.append("No authored distance cutoff: inspect intended view range and light significance.")
            if values.get("cast_shadows") is True:
                candidates.append("Shadow caster: inspect contact requirements and cache invalidation before editing.")
            lights.append({**identity, "component": component.get_path_name(), "observed": values, "candidates": candidates})
        for component in actor.get_components_by_class(unreal.StaticMeshComponent):
            mesh = component.get_editor_property("static_mesh")
            if mesh is None:
                continue
            values = {key: property_value(component, key) for key in ["cast_shadow", "evaluate_world_position_offset", "world_position_offset_disable_distance"]}
            values["collision_enabled"] = str(component.get_collision_enabled())
            asset = {key: property_value(mesh, key) for key in ["lod_group", "light_map_resolution", "light_map_coordinate_index"]}
            try:
                settings = mesh.get_editor_property("nanite_settings")
                asset["nanite_enabled"] = settings.get_editor_property("enabled")
                asset["fallback_percent_triangles"] = settings.get_editor_property("fallback_percent_triangles")
            except Exception:
                asset["nanite_settings"] = {"unavailable": "Inspect Nanite Settings in Static Mesh Editor"}
            meshes.append({**identity,"component":component.get_path_name(),"mesh":mesh.get_path_name(),"observed":values,"asset":asset})
        if hasattr(unreal, "NiagaraComponent"):
            for component in actor.get_components_by_class(unreal.NiagaraComponent):
                effects.append({**identity,"component":component.get_path_name(),"active":component.is_active(),"note":"Editor-world active state is not a runtime system or particle count. Inspect the system's Effect Type and runtime stats."})
    report = {"scope":"Loaded editor world only. Unloaded cells and runtime-spawned objects are excluded.",
              "interpretation":"Properties identify candidates. Use matching runtime timings and visual checks to approve a change.",
              "engine":unreal.SystemLibrary.get_engine_version(),"actor_count":len(actors),"lights":lights,"mesh_components":meshes,"niagara_components":effects}
    folder=Path(unreal.Paths.project_saved_dir())/'Week10Audit'
    folder.mkdir(parents=True,exist_ok=True)
    file=folder/'Optimization-Candidates.json'
    file.write_text(json.dumps(report,indent=2),encoding='utf-8')
    unreal.log(f"Week 10 audit: {len(lights)} lights, {len(meshes)} mesh components, {len(effects)} Niagara components. {file}")
    return report


if __name__ == '__main__':
    audit_world()
