# Week 10 · Optimization study guide

Use **Week10-Slides.pptx** for the whole session. The lecture, measured examples and walkthrough appendix are all in that file. Use the existing Student Lab for the assessment activity and current Canvas instructions for formal requirements.

## The decision process

Write a quality requirement first. Capture a representative workload. Identify the limiting work. Predict what one change should affect, repeat under matching conditions, and decide using both the image and the timings. A memory reduction, fewer draw calls and a faster frame are different results.

Keep output resolution, screen percentage, scalability, camera, workload, renderer, machine and build comparable. Warm shaders and content before a steady test. Record caps. Capture motion when a still misses pop-in, shimmer, contact or responsiveness. If repeats vary as much as the proposed saving, report an inconclusive result.

## Asset data from Maya to Unreal

Choose a pivot that supports placement and grid snapping. Export only the intended assets with stable names, units and normals. Keep triangulation consistent with baked normals. After importing, check scale, pivot, UVs, vertex colors and collision; repeat after reimport. Import settings may differ between the FBX and Interchange workflows.

In the legacy FBX workflow, vertex-color **Replace** imports source data, **Ignore** preserves existing data and **Override** supplies a uniform override. Check the current importer before relying on those names. Protect vertex colors painted in Unreal.

Geometry LOD simplifies the mesh. Texture mips reduce texture resolution. A lightmap UV channel provides a layout for baked lighting. Inspect each separately. A project using fully dynamic lighting may not need the baked-lighting data shown in an older tutorial.

## Collision is an interaction representation

A single convex hull fills inward corners. Several convex hulls can approximate a concave shape while leaving a passage open. Use the simplest representation that preserves required player movement, traces and contact. Inspect Collision Enabled and channel responses: a trace-only object and a simulated rigid body need different policies.

Do not remove collision because the render mesh uses Nanite. Check fallback geometry and collision complexity separately. Test the action that must still work after an edit.

## Texture channels and memory

| Layout | R | G | B | Alpha |
|---|---|---|---|---|
| This lab ORM | Occlusion | Roughness | Metallic | Not required by this packer |
| Gnomon MRO example | Metallic | Roughness | Occlusion | Depends on the export |
| Week 9 MRAH | Metallic | Roughness | Ambient occlusion | Height |

Inspect each channel. Base Color normally uses sRGB. Numeric mask data uses linear interpretation; use the correct sampler and compression. Normal maps need normal-map interpretation. A map with an emissive channel substituted for metallic has a different contract even if it looks similar in the Content Browser.

Painter export templates and Designer's RGBA Merge make the contract repeatable. Padding extends useful border colors outside UV shells, helping prevent filtering bleed. Check the result at reduced mips and intended viewing distances.

Inspect resource size, mip settings, Max Texture Size, LOD Bias and runtime streaming pressure. Halving width and height gives roughly one quarter of the texels at the same format, but actual resource bytes also depend on format and mips. Raising the streaming pool spends more memory. It does not prove the assets are appropriately sized.

A constant non-metallic input may not need a texture channel. Adding alpha can change the compressed resource size. Choose the format and layout using the target platform's actual result.

Normal/roughness compositing can reduce distant specular shimmer. Set Composite Texture to the appropriate normal source and choose the actual roughness channel. Check a camera move under consistent lighting. This is an appearance change to assess, not a guaranteed frame-time saving.

## Lighting and shadow caching

Use Light Mixer to find placed lights and light components inside Blueprints. Inspect Attenuation Radius, Cast Shadows, Max Draw Distance and Max Distance Fade Range. A large influence volume may cost more than the visible contribution justifies. Test radius while preserving contact, focal contrast and readability.

Changing Use Inverse Squared Falloff is an artistic lighting change. Retune intensity and falloff deliberately. Do not treat the tutorial's values as defaults for every scene.

Walk across a light's fade boundary in both directions. Check each target quality tier. UE 5.7's `r.LightMaxDrawDistanceScale` can modify authored ranges. Essential gameplay lighting needs a different policy from ambient decoration.

WPO changes vertex positions in a material. A fixed light can still need fresh shadow pages when a caster deforms. Cached Page, Shadow Casters and Evaluate WPO are different diagnostic views: read the legend in the current mode. Confirm suspected improvements with matched Lit timing and motion. A cache override can freeze a shadow incorrectly.

## Nanite, foliage and decals

Inspect WPO, masking and Pixel Depth Offset separately. Opaque foliage cards can expose the full card shape. A distant improvement can fail in a close view or during a transition. Test near/far views and motion before changing evaluation distance or density.

Nanite Foliage's version-specific experimental status is separate from Nanite generally. Record the engine version and renderer used by the project.

A decal's cost depends on projection coverage, material and receiving surfaces. Related work may appear in multiple passes. Inspect the full scene and use actual timings. Remove optional decoration before gameplay or story cues, and check the fade in motion.

## Niagara and baked motion

CPU/GPU simulation target and Effect Type culling answer different questions. Compare simulation targets with matched output. Compare a culling policy with a record of the effects that disappeared. A GPU emitter can still have system and emitter work on the CPU.

For persistent ambience, choose a policy that reevaluates when the camera or importance changes. A spawn-only policy is suitable only when its behavior fits the effect. Bounds, frequency and cull reaction all affect the result. Test looking away, returning and crossing a boundary.

The existing Niagara lab compares CPU/GPU targets and a separate spawn-only distance policy. Its measured distance test does not validate a visibility policy for persistent ambience. Pooling is a separate lifecycle experiment: compare allocation bursts, GC, retained memory and reset behavior.

Live simulation can react to new contact. VAT replays baked 3D motion. A flipbook replays rendered images and can lose depth from another view. The course's debris comparison shows why lower CPU cost can coexist with almost unchanged whole-frame time. Preserve the full explanation, image pair and timing context when using those slides.

## Choose one follow-up experiment

| Question | One controlled change | Evidence and acceptance check |
|---|---|---|
| Is a fill light too broad? | Reduce radius on a duplicate test group | Relevant GPU work and matched Lit contact/readability |
| Is unseen ambience still running? | Effect Type visibility policy with periodic evaluation | Active systems, CPU/GPU cost, return-to-view behavior |
| Is texture detail worth its residency? | One Max Texture Size or LOD Bias change | Resource/residency evidence, legible runes or signs |
| Is collision unnecessarily detailed? | Substitute simpler collision on a duplicate | Query/physics evidence and required passage/contact |
| Is WPO causing shadow work? | One duplicate material/component evaluation treatment | Cache state, relevant timing, motion and shadow accuracy |
| Does a load boundary hitch? | One preload or streaming-range treatment | Cold/warm traversal, Insights loading, memory and pop-in |

These extend the teaching examples; they add no new deadline or grading requirement. Keep the existing 30-minute assessment focused on the assigned Lighting or Glass case.

## Read-only audit tool

The assessment also has **Tools → Week 10 Optimization**. **Validate and Generate Dashboard** writes a self-contained webpage and JSON to `Saved/Week10Optimization`. Search or filter its findings, review check coverage and exceptions, copy a selection command into Unreal, or compare a matching baseline JSON. The web page reads imported JSON locally and does not control the editor or update itself.

**Toggle Custom Optimization View** draws temporary colored markers over the editor viewport: blue information, amber review, red error. Enable viewport Realtime; toggle after edits to refresh cached bounds. Map changes disable it, and remaining marks expire after disabling. This is a rule visualization rather than a shader-cost visualization. Disable it before timing.

The new profiler section distinguishes CPU threads, GPU queues and waits; pass-level estimates, frame-debugger state and memory evidence answer different questions. In UE 5.7, do not assume an older ProfileGPU popup workflow. Inspect log output and Unreal Insights for the installed version. Read inclusive/exclusive scope context, preserve the capture window, and keep median/p95 separate from individual hitch diagnosis.

Simplygon is an offline asset-processing workflow with reduction, remeshing, aggregation and material baking. Verify plugin, license and engine compatibility first. The course's existing local LOD triangle counts were generated with Unreal reduction, not Simplygon.

With the assessment map open and play stopped, run `Tools/audit_optimization_candidates.py` from Unreal's Python file runner. It writes `Saved/Week10Audit/Optimization-Candidates.json` and changes no assets. It records loaded actors, light properties, mesh properties and editor-world Niagara component state. Unloaded cells and runtime-spawned actors are outside its scope.

An absent distance cutoff or a shadow flag is a candidate, not a failed asset. Compare an intentional exception and use runtime timing before editing. The editor-world Niagara count is not a live particle count.

## Further study paths

- **Broad CPU/world investigation:** [Looman's JetBrains companion](https://tomlooman.com/unreal-engine-optimization-talk/). Start at the measured limiter, then choose ticks, collision, movement, culling, animation or streaming.
- **GPU production case:** [Far Far West companion](https://tomlooman.com/unreal-engine-optimization-farfarwest/). Compare foliage, decal and water decisions with the renderer and hardware in the article.
- **Niagara policy:** [Epic UE 5.7 scalability guidance](https://dev.epicgames.com/documentation/en-us/unreal-engine/scalability-and-best-practices-for-niagara?application_version=5.7). Connect system overhead, Effect Types and pooling to separate tests.
- **Asset pipeline:** [Epic FBX Static Mesh Pipeline](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine). Verify pivot, triangulation, collision and importer compatibility for your round trip.

Looman and Gnomon source timings describe their recordings. Only measurements explicitly identified as course-project captures describe the local course demonstrations.


## Baked and dynamic lighting

Static, Stationary and Movable describe mobility; Point, Spot, Rect and Directional describe light shape. In a compatible precomputed workflow, Static lighting is baked, Stationary combines baked indirect lighting with dynamic direct lighting, and Movable permits runtime changes. Baking trades per-frame lighting work for lightmap UV requirements, memory, storage and build time. Inspect Lightmap Density and check shadow detail; do not assume a bake is free overall.

Stationary lighting cannot move, and baked bounce does not track runtime color changes. Conventional baked shadow channels allow at most four overlaps, sometimes fewer depending on layout. Inspect Stationary Light Overlap. VSM instead evaluates Stationary direct lighting and shadows dynamically. Lumen GI disables baked lightmap contributions, so changing a light to Static can remove illumination rather than produce a valid optimization.

Before comparing strategies, inspect GI, Shadow Map Method, Allow Static Lighting and the world's Force No Precomputed Lighting. A baked test needs a compatible separate map and completed lighting build. The workshop has no completed baked counterpart. Start with one radius or shadow change, preserve the image, and measure the relevant GPU pass with the same camera.
