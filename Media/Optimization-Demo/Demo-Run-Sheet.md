# Week 10: live optimization demonstration

Open the accompanying gallery for all 28 actual captures and their original PNGs. The room is Hane Studios' furnished Cigar Room, with deliberately inefficient classroom settings. The project is UE 5.7.4, DX12 SM6. These are demonstration images, not a controlled before/after performance result.

## Core demonstration order

1. **Lit room and second angle.** Establish furniture, warm light, books, glass and close-up detail that must survive optimization. Confirm Lounge_Unoptimized and keep its reference unchanged.
2. **stat unit → stat gpu.** Start with frame/game/draw/RHI/GPU evidence and actual render resolution. Use `stats.MaxPerGroup 8` for a readable queue overview; restore 25 later. Identify the next question rather than declaring the largest label a fix.
3. **Timing Insights.** Open the included Lounge-SM6 trace in UE 5.7 Insights. Click a gameplay frame, drag a time-ruler interval, then press F. Show graphics/compute overlap and nested events. Hide GPU tracks and inspect CPU idle/waits. The capture uses t.MaxFPS 60, so pacing waits are expected. Its inclusive totals are not a serial frame sum.
4. **Light Mixer.** Window → Light Mixer; inspect the 33 lights, their radii and intensities. Search Interior Fill. Explain selection/solo/mute, then restore visibility before comparison. Change one candidate only in a duplicate map.
5. **Light Complexity → VSM cache → Lit.** Connect overlapping influence to the actual attenuation controls. Read the VSM legend instead of assigning generic good/bad colors. The SM6 run reports local-light overflow; investigate coverage and required lights before increasing limits. High-resolution debug captures also produced page-pool warnings; those allocations are not steady low-resolution benchmarks.
6. **Nanite mask → clusters → triangles → overdraw.** Confirm the path, inspect geometry and then check GPU work. Distinguish Nanite rendering, fallback meshes and collision. The source window mesh has translucent material assignments that produce native Nanite warnings: inspect representation compatibility rather than globally removing glass.
7. **Material buffers and graph.** Compare Unlit/Base Color, Detail Lighting, Roughness and World Normal with Lit. Use complexity views as inspection leads; their models are not timings. Open M_Glass, inspect the actual graph, then Stats/Platform Stats for the target and pass. The graph capture shows entry points, not a full target-statistics readout.
8. **Render Resource Viewer.** Inspect named allocations and filters. The captured filtered editor total is not all VRAM or packaged game memory.
9. **Custom overlay → dashboard → overlay off.** Follow a rule to an actor/property and state a falsifiable hypothesis. Show the 376 candidates as leads, then return to Lit, disable all diagnostic overlays and capture a matched baseline before editing.

## Capture and reset notes

- Clean viewport images are 1920×1080 at the recorded cameras. Native editor/Insights images retain their actual UI dimensions. The stat HUD shows an 866×550 editor render view. Do not compare these numbers directly.
- The real trace is a standalone editor runtime at 1280×720, 100% screen percentage, 60 FPS cap, 900 CSV frames, named events and CPU/GPU/frame/bookmark/loading/counter channels. It includes startup and ran alongside the editor, so use it for navigation and evidence interpretation. Record a separate minimal capture for timing claims.
- The full PNGs retain original pixels. The material graph has an explicitly recorded crop that excludes the clipped lower table/taskbar. No UI or data was generated to impersonate Unreal.
- The earlier lounge timing logs say SM5. Retain their numeric results only as historical SM5 fallback evidence; they do not validate the intended SM6 Nanite/VSM path. The current starter and complete lab explicitly request PCD3D_SM6. Restart after changing shader formats and verify the startup log.
- Capture scripts do not save assets/maps. Restore Audit Camera, Lit, Nanite/VSM visualizations off, the custom overlay off, `stat none`, and `stats.MaxPerGroup 25` before a timing run.

## Primary references

- [Epic Light Mixer](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-the-light-mixer-in-unreal-engine?application_version=5.7)
- [Epic viewport modes](https://dev.epicgames.com/documentation/en-us/unreal-engine/viewport-modes-in-unreal-engine?application_version=5.7)
- [Epic Timing Insights controls](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-reference-in-unreal-engine-5?application_version=5.7)
- [Epic Virtual Shadow Maps](https://dev.epicgames.com/documentation/en-us/unreal-engine/virtual-shadow-maps-in-unreal-engine?application_version=5.7)

Rendered environment imagery: Hane Studios Cigar Room, acquired through Fab. This capture pack distributes screenshots, not licensed source assets. The private full classroom project and raw trace remain separate from the public starter.
