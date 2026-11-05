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


## Material and shader logic

A material optimization must reduce relevant work while preserving a stated visual requirement. Start with the expensive pass or screen region, then open the material actually assigned to that draw. Counted graph nodes, compiled instructions, texture memory, shader variants and measured GPU milliseconds answer different questions.

### Diagnose before rewriting

1. In the scene, compare Frame/Game/Draw/GPU and identify the limiting work. Use a relevant Lit GPU pass rather than assuming a high material instruction count limits Frame.
2. Open the actual Material or instance. In **Stats / Platform Stats**, select the target API, feature level and quality. Record pixel and vertex instruction counts, sample/sampler counts when provided, relevant pass and compiler errors. Different permutations and vertex factories can have different programs. Inspect generated shader code when a feature-removal hypothesis is unclear.
3. Use Shader Complexity and Quad Overdraw to locate coverage or overlap candidates. Colors do not model every texture/cache operation or rendering path. Instruction types differ in cost. Return to Lit for timing.
4. Duplicate the candidate asset or map, change one thing, warm shaders and content, and repeat. Compare close and distant views, motion, silhouettes, roughness, glass, shadows and texture residency. An image that simply lost the feature is a different quality tier, not automatically an equivalent optimization.

### Controls and tradeoffs

| Suspected work | Candidate change | What can invalidate the result? |
|---|---|---|
| Repeated texture fetches | Reuse a sample with matching UV/mip/sampler behavior; remove an unnecessary layer. | Different coordinates or mip selection require different fetches; the compiler may already reuse work. |
| Several scalar mask maps | Pack compatible masks and extract channels from one sample. | Different resolution/filtering needs, compression damage, or wrong sRGB/data interpretation. |
| Sampler-state pressure | Use supported shared sampler settings where wrapping/filtering match. | Fewer sampler states do not mean fewer texture fetches; platform support differs. |
| Heavy procedural noise/math | Remove unneeded layers, simplify a justified approximation, or bake stable detail into a lookup. | A lookup spends texture memory/bandwidth; baking may lose animation, detail or filtering quality. |
| Feature visually weighted to zero | Use a static-disabled variant when runtime switching is unnecessary. | A runtime Lerp/zero scalar may retain the work. A static switch adds compiled-variant management and cannot change in play. |
| Repeated affine UV transform | Test Customized UVs or Vertex Interpolator. | Vertex/interpolator cost, precision and dense meshes; nonlinear math may interpolate differently. |
| Translucent or masked coverage | Tighten surface coverage, reduce justified overlap or layers. | Lost transparency/cutout shape, sorting/refraction changes, or different shadow/depth behavior. |
| WPO / Pixel Depth Offset | Simplify the actual path or introduce a validated distance policy. | Deformation, depth, bounds, velocity and shadow artifacts; Nanite does not erase this work. |
| Many material instances | Share genuinely matching state or use CPD for per-primitive values. | This addresses parameter/submission behavior, not automatic pixel-shader simplification. Compare all overrides. |
| Excess shader variants | Reduce unnecessary static feature combinations and usage, inspect Material Analyzer and cook data. | Compile time, PSO preparation, storage and runtime GPU time are separate budgets. |

Multiplication/addition are not a universal replacement for every power, divide or trigonometric operation. Inspect what the compiler emitted; constant folding or algebraic simplification may already remove the apparent difference. Material Functions organize code, and Custom HLSL enables expression, but neither automatically makes a shader faster. An If node is not proof that both sides stop executing efficiently: compiled branching, coherence and target hardware matter.

For vertex placement, an affine transform such as `UV * 8 + (0.23, 0.17)` can be evaluated per vertex and interpolated without changing the ideal UV field. A sine, normalization or other nonlinear transform generally cannot be moved the same way on a coarse mesh without changing the result. Customized UVs expose a main-node input; Vertex Interpolator is the route used by the supplied UVVertex asset. The texture is still sampled in the pixel stage in this experiment.

Use the simplest shading model and blend behavior that meets the visual requirement. Unlit can be appropriate for a screen or stylized effect; making a physically lit sofa Unlit changes the requirement. On Nanite surfaces, inspect material shading, masked coverage and WPO independently of cluster geometry cost. On Substrate or a different feature level, re-evaluate the active material path rather than transferring this unlit test's result unchanged.

### Shader practice: two equivalent-output experiments

Download the [expanded comparison projects](https://github.com/anthonymonteagudo/Week10-Profiling/releases/tag/week10-ue57-comparison-demos-v2) and open MaterialCostLab in UE 5.7. Windows editor modules are included; rebuild with the Windows C++ toolchain if the engine build does not match. These tests are separate from the furnished Fab lounge.

**A: remove unused feature logic.** Open `/Game/Lab/M_DynamicZero` and `/Game/Lab/M_MasterOff`. DynamicZero blends a 24-iteration procedural ripple with the flat color using the runtime scalar RippleWeight, default zero. MasterOff statically selects the flat branch. Predict whether the compiled pixel program differs; inspect target stats and code, then verify that the intended output is the same. MasterOn intentionally shows the ripple and changes the picture; it is not the equivalent-output control.

**B: choose the shader stage.** Open `/Game/Lab/M_UVPixel` and `/Game/Lab/M_UVVertex`. Both sample T_UVChecker with the same affine coordinate transform. UVVertex passes that transform through Vertex Interpolator. Inspect stage statistics and compare alignment, seams and filtering. The transform is deliberately small; no guaranteed overall frame saving is implied. As a separate extension, try nonlinear distortion on a coarse versus dense mesh and state the quality difference.

From the MaterialCostLab project folder, use fresh output directories:

```powershell
.\Tools\Capture-Shader-Logic.ps1 -Kind Visual -Experiment Feature -OutputDirectory Saved/Feature-Visual
.\Tools\Capture-Shader-Logic.ps1 -Kind Timing -Experiment Feature -OutputDirectory Saved/Feature-Timing
.\Tools\Capture-Shader-Logic.ps1 -Kind Visual -Experiment UV -OutputDirectory Saved/UV-Visual
.\Tools\Capture-Shader-Logic.ps1 -Kind Timing -Experiment UV -OutputDirectory Saved/UV-Timing
```

The timing order is A, B, B, A, A, B. Analyze CSV rows 192–575 inclusive (384 frames), separately per launch. Timing runs contain no screenshots. Match hardware, engine, API, resolution, screen percentage, quality, camera and warm-up. Use milliseconds and compare variation; collect a more relevant pass capture when the overall difference is inconclusive.

| Record | Your experiment |
|---|---|
| Required image and hypothesis | |
| Material assets, target/API/quality and compiled pass | |
| A/B pixel and vertex instructions; sample/sampler counts | |
| A/B per-launch median and p95 Frame/GPU | |
| Same-view image difference, motion and second-view checks | |
| What work changed; what remains uncertain | |
| Keep/revise/reject and next test | |

**Transfer to the lounge:** choose one material on a significant visible surface, duplicate it and its assignment locally, and test one justified feature or sampling change. Preserve the original Fab parent. If profiling instead points to shadows, geometry or CPU waits, report that material logic is not the leading optimization for that capture.

### Worked snapshot and interpretation

The local UE 5.7 editor API snapshot reported DynamicZero / MasterOff pixel instruction counts of **236 / 67**, and UVPixel / UVVertex counts of **69 / 68**. Vertex counts were 140 / 136 and 140 / 140 respectively. These are editor aggregates for the loaded compiled assets, not a per-pass GPU duration or a portable platform budget. Verify the actual target permutation in Platform Stats.

Despite the instruction differences, three warmed standalone runs per treatment produced overlapping overall GPU medians: approximately 3.284–3.301 ms for the feature pair and 3.278–3.285 ms for the UV pair. The fixed-camera feature screenshots were identical; the UV pair had tiny rounding differences. The supported conclusion is that compiled work differs, while this workload did not demonstrate a reliable overall timing saving. That does not establish that the same change is irrelevant on a more shader-bound target.

### Primary references

- [Material Editor stats and generated code](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-material-editor-ui)
- [Static and runtime material parameters](https://dev.epicgames.com/documentation/en-us/unreal-engine/material-parameter-expressions-in-unreal-engine?application_version=5.7)
- [Customized UVs and interpolation](https://dev.epicgames.com/documentation/unreal-engine/customized-uvs-in-unreal-engine-materials)
- [Material Analyzer](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-material-analyzer-tool)
- [Viewport diagnostic modes](https://dev.epicgames.com/documentation/unreal-engine/viewport-modes-in-unreal-engine)

Use the engine/platform version of each reference. The older artist-performance guidance is a conceptual foundation; historical renderer-specific rules are not universal UE 5.7 prescriptions.
