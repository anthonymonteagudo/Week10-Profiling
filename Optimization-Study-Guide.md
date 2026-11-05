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


## Looman articles and 04 investigations

Use these as optional follow-ups to the main lounge lab. Choose the question your evidence supports; preserve the baseline and change one variable.

### Read the source in its engine context

The supplied 04 video shows Dark Ruins in UE 5.5. The [Far Far West article](https://tomlooman.com/unreal-engine-optimization-farfarwest/) describes another project in UE 5.7. Their timings do not predict our lounge's result. The classroom project remains UE 5.7.

| Engine reading | What to carry into your investigation |
|---|---|
| [5.5 highlights](https://tomlooman.com/unreal-engine-5-5-performance-highlights/) | MegaLights was experimental in the source video's context. |
| [5.6 highlights](https://tomlooman.com/unreal-engine-5-6-performance-highlights/) | GPU Profiler 2.0 exposes graphics/compute queue work; overlapping events are not a serial sum. |
| [5.7 highlights](https://tomlooman.com/unreal-engine-5-7-performance-highlights/) | Matches this lab. ShaderTypeStats.csv helps compare shader permutation/code growth after cooking; it is not total VRAM usage. MegaLights is Beta. |
| [5.8 highlights](https://tomlooman.com/unreal-engine-5-8-performance-highlights/) | Further reading, including changed feature status. Do not upgrade the classroom project to reproduce an unrelated feature. |

### First-use hitches and PSOs

A compiled shader, a graphics API pipeline state object (PSO) and the cost of drawing with it are different. A driver cache can hide pipeline creation on a repeated route; restarting the process alone does not establish a cold cache. A hitch may also be loading, streaming or gameplay. Use an Insights trace to identify the work before selecting a remedy.

For an advanced investigation, use a **packaged Development build** on the target RHI, fixed quality settings and a documented first-encounter route. Record the cache conditions and repeat the route. Check PSO misses/late preparation, frame spikes, loading time and visible proxy/pop-in behavior. `stat psoprecache` needs a non-editor build; launching UnrealEditor with `-game` does not satisfy that requirement. Do not clear shared system caches as a classroom shortcut. Precaching prepares supported states before use; bundled caches cover recorded states, so route/quality/pass coverage matters. A successful editor launch is not proof of packaged coverage. This lab supplies no measured PSO-coverage result. Read [PSO precaching and bundled PSOs](https://tomlooman.com/unreal-engine-psocaching/); its Advanced Shader Delivery section is for 5.8.4+, outside the 5.7 setup.

### Nanite, materials and representations

- Increasing `r.Nanite.MaxPixelsPerEdge` permits coarser geometry. Compare cluster/VisBuffer evidence, then check silhouettes and transitions in Lit. Restore the baseline after a diagnostic extreme.
- Evaluate WPO indicates where the material path is active. Green is not a universal error color. Confirm the deformation need, actual function and shadow cost before bypassing work.
- A material contact-shadow function, a light's Contact Shadow Length and VSM invalidation are separate controls.
- Nanite rendering, fallback geometry and the representation used by collision queries are separate. Check each consumer before reducing a fallback; Auto is not a universal repair.

The [production case](https://tomlooman.com/unreal-engine-optimization-farfarwest/) offers masked-foliage, decal and water examples. Carry over the diagnostic question and quality test, then measure your own workload.

### Runtime, iteration and quality budgets

A static-disabled branch may remove runtime work while creating another compiled variant. Measure GPU/pass cost, compile duration, cooked shader bytes and PSO preparation separately. In 5.7 compare ShaderTypeStats.csv from matched target cooks; packaging/chunk duplication can affect size. Remove renderer permutations only when the feature is genuinely unused across the project, then rebuild and test affected content. The older [shader compilation article](https://tomlooman.com/unreal-engine-optimize-shader-compile-time/) supplies the principle; its checkbox choices are not a preset for this project.

Hardware benchmark results are CPU/GPU performance indices, not a guaranteed scene FPS. Calibrate scalability thresholds using representative minimum and recommended devices, test the actual game route, and allow player override. Run selection at a planned setup/menu stage, outside timed capture windows. Detail Mode can exclude intentionally expendable components; keep required cues and interactions. In the installed UE 5.7 defaults, Effects quality maps Detail Mode to 0/1/1/3/3; verify your project's overrides. Read [hardware-based graphics selection](https://tomlooman.com/unreal-engine-optimal-graphics-settings/).

### Record enough context to explain a trace

A counter records a quantity; a CPU scope records CPU execution; a GPU event records GPU work. Add bookmarks/regions for route and quality changes, and enable the relevant trace channels. Keep detailed diagnostic captures separate from minimal timing runs. Read [counters and traces](https://tomlooman.com/unreal-engine-profiling-stat-commands/) and [optimization on a budget](https://tomlooman.com/unreal-engine-optimization-talk/).

The lab audit JSON includes `editor_console_snapshot` for screen percentage, dynamic resolution, Nanite error, sharpening, Detail Mode, quality groups and PSO precaching. These are global values from the editor process, **not** effective per-view/post-process values, measured dynamic resolution or packaged runtime state. Resolve defaults/sentinels (such as 0 or -1) in the actual view before interpreting them. Record output dimensions, internal scene percentage and upscaler separately. At 3840×2160 output, 50% of each dimension gives 1920×1080 internal rendering; resizing the viewport changes the workload. Sharpening cannot restore missing geometric or temporal detail.

The inventory distinguishes lights with Affects World enabled from disabled components. Editor icons alone do not establish active light influence. Disabled components may still occupy memory.

### When a promising number is inconclusive

The 04 source's lens-flare A/B output reports about 16.03 versus 16.10 ms and explicitly flags a 27% chance of noise. That screenshot does not establish a saving. Repeat independent launches, inspect distributions and preserve the image requirement. Do not add together the video's separate experiments: several treatments are reset between tests.


## Rendering configuration correction from the live capture rehearsal

The 5 November live walkthrough found that the earlier lounge timing launches used DX12 **SM5**, as recorded in their raw startup logs. Nanite was therefore using fallback rendering, and those runs do not validate the intended SM6 Nanite/VSM path. Keep the earlier fill-shadow numbers as historical evidence of that SM5 configuration only; the cache experiment does not establish VSM-cache performance. Do not compare those numbers directly with the new SM6 images/trace.

The current lab explicitly requests DX12 with PCD3D_SM6 in DefaultEngine.ini. Restart the editor after changing shader formats and verify the startup log says SM6 before demonstrating Nanite or VSM. The live SM6 walkthrough also reports a VSM local-light overflow and translucent material assignments on a Nanite window mesh. These are real inspection leads in the intentionally inefficient scene, not instructions to increase a budget or globally remove glass. Inspect relevant lights and split/use appropriate mesh representations before retesting image quality. The new screenshots/trace demonstrate tools, not a controlled performance improvement.


## Gnomon Part 04: material workflow checks

The current deck places materials/textures/shader logic at 68–103. Use the packed-mask example at 82, actual glass graph at 87, source stats snapshots at 88 and instance-override example at 98 with the existing runnable experiments. The main furnished-lounge lab is 121. These follow-ups do not add requirements inside its thirty-minute block.

An unchecked material-instance override inherits the parent value. To remove a compiled feature, inspect its static-switch branch and target variant. A runtime scalar zero can change the image while retaining work, and a shared packed texture may still supply roughness or occlusion after emissive work disappears. Keep the channel layout, mip behavior, color interpretation and compression compatible when swapping packed maps. Group related parameters so another artist can use the instance correctly.

Record target, pass and feature state with compiled statistics. Several edits separate the workshop's 117- and 131-instruction snapshots; they are not a matched timing comparison or proof of one node's cost. Sampler denominators depend on the target/path. A constant Power expression may already simplify, while Fully Rough, blend mode, Unlit or domain changes can alter required appearance. Verify target code and the image before accepting a rewrite.

`r.Streaming.PoolSize` controls a runtime memory budget. It does not resize source or cooked texture files. `stat streaming` reports distinct categories including wanted mips, residency and NonStreaming Mips; the latter is not every texture in use. Check the texture's built format/mips, actual pool pressure, scalability/device policy and target memory before changing a budget. Restore the previous value after a diagnostic experiment.

References: [Epic material parameters](https://dev.epicgames.com/documentation/unreal-engine/material-parameter-expressions-in-unreal-engine), [material properties](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-material-properties), [streaming configuration](https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-streaming-configuration-in-unreal-engine), [streaming metrics](https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-streaming-metrics-in-unreal-engine). Source frames are credited in the presentation notes.


## Shipped-game optimization examples

These nine examples appear beside the corresponding concepts in the single deck. Developer results belong to their stated engine, content and hardware. Each case is an idea to test, with a quality or interaction requirement to preserve.

| Slide | Game and technique | Developer source / reading pointer |
|---|---|---|
| 17 | Factorio: cache the work that stays valid | [Developer breakdown](https://www.factorio.com/blog/post/fff-323) — Water animation — Game integration, paragraphs on prepare render and per-chunk draw orders |
| 42 | DOOM: narrow each surface’s light list | [Developer breakdown](https://www.advances.realtimerendering.com/s2016/Siggraph2016_idTech6.pdf) — PDF pages 4–9: Data Structure for Lighting & Shading / Preparing Clustered Structure |
| 54 | Fortnite: replace distant groups with a proxy | [Developer breakdown](https://www.unrealengine.com/tech-blog/unreal-engine-improvements-for-fortnite-battle-royale) — Building and Rendering a Large Map, HLOD/Simplygon and overnight commandlet paragraphs |
| 67 | Fortnite: more leaf geometry can cost less | [Developer breakdown](https://www.unrealengine.com/tech-blog/bringing-nanite-to-fortnite-battle-royale-in-chapter-4) — Trees — Construction; images show final foliage and its triangle visualization |
| 90 | Horizon: spend samples where clouds exist | [Developer breakdown](https://www.advances.realtimerendering.com/s2017/Nubis%20-%20Authoring%20Realtime%20Volumetric%20Cloudscapes%20with%20the%20Decima%20Engine%20-%20Final%20.pdf) — PDF pages 97–98, printed slides 99–100: Ray-March Optimizations |
| 96 | Tsushima: let many systems share one wind | [Developer breakdown](https://blog.playstation.com/2021/01/12/how-stunning-visual-effects-bring-ghost-of-tsushima-to-life/) — Wind, paragraphs beginning ‘The grass and pampas fields’ through local displacement |
| 106 | Fortnite: bake branch motion into a texture | [Developer breakdown](https://www.unrealengine.com/tech-blog/bringing-nanite-to-fortnite-battle-royale-in-chapter-4) — Trees — Wind animation / Distance culling |
| 111 | Uncharted 4: make the card fit each frame | [Developer breakdown](https://www.advances.realtimerendering.com/other/2016/naughty_dog/NaughtyDog_TechArt_Final.pdf) — PDF pages 124–127, especially 127: Particle Optimizations |
| 126 | Fortnite: move first-use work into loading | [Developer breakdown](https://www.unrealengine.com/tech-blog/game-engines-and-shader-stuttering-unreal-engines-solution-to-the-problem) — PSO precaching / The driver cache |

For each case: identify the repeated or unnecessary work, the replacement representation, the cost moved elsewhere, and one test that could reject it. The class projects demonstrate their documented techniques; they do not implement every production feature above. The Uncharted bounds-aware flipbook and Fortnite branch-transform bake are references, while the supplied debris demo uses per-vertex VAT offsets and a fixed flipbook card.


## Complete source index

Start with **Tom Looman**, Prof. Monteagudo’s recommended follow-up: the [free performance article index](https://tomlooman.com/categories/#performance-optimization) and [Complete Game Optimization course](https://tomlooman.com/courses/unrealengine-optimization/). The course is paid; the article index is freely readable. Gnomon workshop access is separate. These are references, not additional purchases required for the lab.

This index consolidates the deck’s cited links, the assessed Looman companion reading, and visual credits. Slide numbers refer to this 162-slide revision. The lab uses UE 5.7; historical UE4/UE5.1 cases and newer-version articles retain their own context. Source observations are separate from our course measurements.

### Tom Looman — start here

- [Complete Game Optimization for Unreal Engine 5 — course (paid)](https://tomlooman.com/courses/unrealengine-optimization/) — Course/source collection or assessed companion reading.
- [Performance & Optimization — free article index](https://tomlooman.com/categories/#performance-optimization) — Course/source collection or assessed companion reading.
- [Unreal engine 5 5 performance highlights](https://tomlooman.com/unreal-engine-5-5-performance-highlights/) — Course/source collection or assessed companion reading.
- [Unreal engine 5 6 performance highlights](https://tomlooman.com/unreal-engine-5-6-performance-highlights/) — Course/source collection or assessed companion reading.
- [Unreal engine 5 7 performance highlights](https://tomlooman.com/unreal-engine-5-7-performance-highlights/) — Slides 100.
- [Unreal engine 5 8 performance highlights](https://tomlooman.com/unreal-engine-5-8-performance-highlights/) — Course/source collection or assessed companion reading.
- [Unreal engine optimal graphics settings](https://tomlooman.com/unreal-engine-optimal-graphics-settings/) — Slides 129.
- [Unreal engine optimization farfarwest](https://tomlooman.com/unreal-engine-optimization-farfarwest/) — Slides 66, 75, 129, 135.
- [Unreal engine optimization talk](https://tomlooman.com/unreal-engine-optimization-talk/) — Slides 22, 23, 56, 135.
- [Unreal engine optimize shader compile time](https://tomlooman.com/unreal-engine-optimize-shader-compile-time/) — Slides 100.
- [Unreal engine profiling stat commands](https://tomlooman.com/unreal-engine-profiling-stat-commands/) — Slides 22.
- [Unreal engine psocaching](https://tomlooman.com/unreal-engine-psocaching/) — Slides 28, 125.

### Gnomon Workshop / Rodrigo Brea

- [Optimization for Games: Settings, Materials, Textures & Commands — supplied Parts 01–04 (subscription workshop)](https://www.thegnomonworkshop.com/workshops/optimization-for-games-settings-materials-textures-commands) — Course/source collection or assessed companion reading.

### Epic Games — engine documentation

- [Customized uvs in unreal engine materials](https://dev.epicgames.com/documentation/unreal-engine/customized-uvs-in-unreal-engine-materials) — Slides 93.
- [Fbx static mesh pipeline in unreal engine — UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine?application_version=5.7) — Slides 50.
- [How to create a gpu sprite effect in niagara for unreal engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/how-to-create-a-gpu-sprite-effect-in-niagara-for-unreal-engine) — Slides 158.
- [Lumen global illumination and reflections in unreal engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine) — Slides 37, 38.
- [Material parameter expressions in unreal engine](https://dev.epicgames.com/documentation/unreal-engine/material-parameter-expressions-in-unreal-engine) — Slides 98.
- [Material parameter expressions in unreal engine — UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/material-parameter-expressions-in-unreal-engine?application_version=5.7) — Slides 92, 97, 99.
- [Nanite technical details — UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-technical-details?application_version=5.7) — Slides 59, 62, 63.
- [Nanite virtualized geometry in unreal engine — UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-virtualized-geometry-in-unreal-engine?application_version=5.7) — Slides 95.
- [Performance guidelines for artists and designers — UE 4.27](https://dev.epicgames.com/documentation/unreal-engine/performance-guidelines-for-artists-and-designers?application_version=4.27) — Slides 85, 89, 91.
- [Render resource viewer in unreal engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/render-resource-viewer-in-unreal-engine) — Slides 30.
- [Stat commands in unreal engine — UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/stat-commands-in-unreal-engine?application_version=5.7) — Slides 10, 76.
- [Static light mobility in unreal engine — UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/static-light-mobility-in-unreal-engine?application_version=5.7) — Slides 34, 35, 38.
- [Stationary light mobility in unreal engine — UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/stationary-light-mobility-in-unreal-engine?application_version=5.7) — Slides 34, 36.
- [Texture streaming configuration in unreal engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-streaming-configuration-in-unreal-engine) — Slides 77.
- [Texture streaming metrics in unreal engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-streaming-metrics-in-unreal-engine) — Slides 77.
- [Timing insights in unreal engine 5 — UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/timing-insights-in-unreal-engine-5?application_version=5.7) — Slides 27.
- [Unreal engine material analyzer tool](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-material-analyzer-tool) — Slides 97.
- [Unreal engine material editor ui](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-material-editor-ui) — Slides 86, 89, 91, 99.
- [Unreal engine material properties](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-material-properties) — Slides 99.
- [Unreal insights reference in unreal engine 5 — UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-reference-in-unreal-engine-5?application_version=5.7) — Slides 14.
- [Using the light mixer in unreal engine — UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-the-light-mixer-in-unreal-engine?application_version=5.7) — Slides 39.
- [Using transparency in unreal engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-transparency-in-unreal-engine) — Slides 94.
- [Viewport modes in unreal engine](https://dev.epicgames.com/documentation/unreal-engine/viewport-modes-in-unreal-engine) — Slides 86, 94.
- [Viewport modes in unreal engine — UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/viewport-modes-in-unreal-engine?application_version=5.7) — Slides 33, 69, 70, 72.
- [Virtual shadow maps in unreal engine — UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/virtual-shadow-maps-in-unreal-engine?application_version=5.7) — Slides 34, 36, 37, 38, 44, 45, 46, 95.

### Tool and platform references

- [Labs vertex animation textures 3.0.html](https://www.sidefx.com/docs/houdini/nodes/out/labs--vertex_animation_textures-3.0.html) — Slides 105.
- [Ue5](https://documentation.simplygon.com/SimplygonSDK_10.4.169.0/ue5/) — Slides 52, 53.
- [Unreal engine performance guide](https://gpuopen.com/learn/unreal-engine-performance-guide/) — Slides 20.

### Shipped-game developer publications

- [DOOM (2016) — PDF pages 4–9: Data Structure for Lighting & Shading / Preparing Clustered Structure](https://www.advances.realtimerendering.com/s2016/Siggraph2016_idTech6.pdf) — Slides 42.
- [Factorio — Water animation — Game integration, paragraphs on prepare render and per-chunk draw orders](https://www.factorio.com/blog/post/fff-323) — Slides 17.
- [Fortnite Battle Royale — Building and Rendering a Large Map, HLOD/Simplygon and overnight commandlet paragraphs](https://www.unrealengine.com/tech-blog/unreal-engine-improvements-for-fortnite-battle-royale) — Slides 54.
- [Fortnite Battle Royale — PSO precaching / The driver cache](https://www.unrealengine.com/tech-blog/game-engines-and-shader-stuttering-unreal-engines-solution-to-the-problem) — Slides 126.
- [Fortnite Chapter 4 — Trees — Wind animation / Distance culling](https://www.unrealengine.com/tech-blog/bringing-nanite-to-fortnite-battle-royale-in-chapter-4) — Slides 67, 106.
- [Ghost of Tsushima — Wind, paragraphs beginning ‘The grass and pampas fields’ through local displacement](https://blog.playstation.com/2021/01/12/how-stunning-visual-effects-bring-ghost-of-tsushima-to-life/) — Slides 96.
- [Horizon Zero Dawn — PDF pages 97–98, printed slides 99–100: Ray-March Optimizations](https://www.advances.realtimerendering.com/s2017/Nubis%20-%20Authoring%20Realtime%20Volumetric%20Cloudscapes%20with%20the%20Decima%20Engine%20-%20Final%20.pdf) — Slides 90.
- [Uncharted 4 — PDF pages 124–127, especially 127: Particle Optimizations](https://www.advances.realtimerendering.com/other/2016/naughty_dog/NaughtyDog_TechArt_Final.pdf) — Slides 111.

### Video sources cited in the lecture

- [Lecture video cited on slides 16](https://www.youtube.com/watch?v=vnbARZHccpQ) — Slides 16.
- [Lecture video cited on slides 24, 26, 43, 44, 45, 47, 57, 58, 64, 112, 129, 135](https://www.youtube.com/watch?v=c2MH20OPSw0) — Slides 24, 26, 43, 44, 45, 47, 57, 58, 64, 112, 129, 135.
- [Lecture video cited on slides 40, 43, 45](https://www.youtube.com/watch?v=1uFR9lXrpyQ) — Slides 40, 43, 45.

### Lab environment and course evidence

- [Hane Studios — Cigar Room Environment (Fab source for our furnished lounge)](https://www.fab.com/listings/4da78da6-44b3-4adf-8883-219fe17b44d4) — Slides 3, 4, 5, 14, 15, 16, 30, 39, 41, 46, 49, 60, 61, 65, 71, 72, 73, 74, 87, 118, 119, 121.

### Visual credits — original media

- [Source image: Ghost-VFX-FI.jpg](https://blog.playstation.com/tachyon/2021/01/Ghost-VFX-FI.jpg?resize=1088%2C612&crop_strategy=smart) — Slides 96.
- [Source image: Unreal+Engine/blogAssets/2017/OCTOBER+2017/Fortnite+Battle+Royale+UE+Improvements/FNBR_SocialRangerTower-770x433-a1b2112ca6bf4445b2c912c3036fff21ca8193cb.jpg](https://cdn2.unrealengine.com/Unreal+Engine%2FblogAssets%2F2017%2FOCTOBER+2017%2FFortnite+Battle+Royale+UE+Improvements%2FFNBR_SocialRangerTower-770x433-a1b2112ca6bf4445b2c912c3036fff21ca8193cb.jpg) — Slides 54.
- [Source image: fff-323-noise.png](https://cdn.factorio.com/assets/img/blog/fff-323-noise.png) — Slides 17.
- [Source image: nanite-in-fortnite-chapter-4-tree-geometry-1920x1080-a3c53a79ee70.png](https://cdn2.unrealengine.com/nanite-in-fortnite-chapter-4-tree-geometry-1920x1080-a3c53a79ee70.png?resize=1&w=1920) — Slides 106.
- [Source image: nanite-in-fortnite-chapter-4-triangle-counts-1920x1080-90a3059197d2.jpg](https://cdn2.unrealengine.com/nanite-in-fortnite-chapter-4-triangle-counts-1920x1080-90a3059197d2.jpg?resize=1&w=1920) — Slides 67.
- [Source image: nanite-in-fortnite-chapter-4-triangle-counts-nanite-1920x1080-be5844e3497b.jpg](https://cdn2.unrealengine.com/nanite-in-fortnite-chapter-4-triangle-counts-nanite-1920x1080-be5844e3497b.jpg?resize=1&w=1920) — Slides 67.

### Course experiments and captures

The Week 10 material/CPD, shader logic, Live/VAT/Flipbook debris and Niagara comparisons, the custom overlay/dashboard and native lounge captures are course-authored evidence. Use the [project README](README.md), [lab worksheet](Student-Lab.md), [capture gallery](Media/Optimization-Demo/index.html), and [comparison project releases](https://github.com/anthonymonteagudo/Week10-Profiling/releases/tag/week10-ue57-comparison-demos-v2). Their results retain the stated launch conditions; third-party game results are not performance guarantees for this lab.
