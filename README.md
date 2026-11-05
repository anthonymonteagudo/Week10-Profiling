# Week 10: profiling and optimization

## Start here

1. [Set up the UE 5.7 furnished lounge lab](Unreal/README.md). The [starter ZIP](https://github.com/anthonymonteagudo/Week10-Profiling/releases/tag/week10-ue57-optimization-lab-v4) contains our project tools and setup; obtain the free Fab environment separately.
2. Follow the [student lab and evidence worksheet](Student-Lab.md).
3. Use the [single Week 10 slide deck](Week10-Slides.pptx) and [optimization study guide](Optimization-Study-Guide.md).

The lab opens Lounge_Unoptimized, a furnished interior with deliberately introduced production mistakes. Keep its reference map unchanged and test one reversible change. The content-only editor plugin adds **Tools > Week 10 Optimization** for a custom viewport overlay and a searchable local dashboard. Disable the overlay before timing. Findings are candidates rather than proven savings.

![The actual furnished lounge](Media/Lounge.png)

## Supporting tools and demonstrations

- [Capture comparison](Tools/compare_captures.py) and [frame-budget report](Tools/report_perf_budget.py) process Unreal CSVs. Run `python Tools/compare_captures.py --help` for options.
- [Read-only inventory](Tools/audit_optimization_candidates.py) is an optional simple Python rule example; the lab plugin is the main audit workflow.
- [Texture mask packer](Tools/pack_masks.py) and [practice inputs](Tools/DemoInputs) require Python and Pillow. Run `python Tools/pack_masks.py Tools/DemoInputs/AO.png Tools/DemoInputs/Roughness.png Tools/DemoInputs/Metallic.png Packed_ORM.png`.
- [Material, debris and Niagara comparison projects](https://github.com/anthonymonteagudo/Week10-Profiling/releases/tag/week10-ue57-comparison-demos-v2): UE 5.7 Windows editor binaries and C++ source are supplied. Rebuild with the Windows C++ toolchain if your engine build does not match. These are separate instructor-led demonstrations.
- [Editable texture demo release](https://github.com/anthonymonteagudo/Week10-Profiling/releases/tag/week10-ue57-texture-demos-v1) opens ArrayDemo and is separate from the optimization lab.

Use the local dashboard generated from your own open map. The lecture's private hosted dashboard is a historical snapshot and is not a live view of your project. Instructor answer keys and the complete licensed classroom working copy are distributed separately.

## Material and shader logic

The deck now includes the shader-cost sequence at 81–97. The [study guide](Optimization-Study-Guide.md#material-and-shader-logic) supplies optimization decisions, graph recipes, two runnable experiments and a results worksheet. Use the updated comparison-project release for DynamicZero/MasterOff and UVPixel/UVVertex.

Browse the [material lab source and experiment instructions](MaterialCostLab/README.md). Generated material assets are supplied in the v2 comparison release.

The consolidated deck has 152 slides. Optional article/04 investigations cover first-use PSO hitches, Nanite/fallback/WPO checks, compile/cook budgets, trace counters and calibrated quality tiers. The main lounge activity is slide 113.

## Demo captures

[Open the 28-capture gallery](Media/Optimization-Demo/index.html) or [download the screenshot pack](https://github.com/anthonymonteagudo/Week10-Profiling/releases/tag/week10-demo-captures-v1). It covers the furnished room, Light Mixer, Timing Insights, stat unit/GPU, material buffers, Nanite, VSM cache, GPU resources and the custom audit. Each image includes its question, live steps and interpretation limits. The v4 lab explicitly uses DX12 SM6; earlier lounge timing results used SM5 fallback rendering.

The 28 captures are embedded directly in the deck. The main sequence runs through 126; reference comparisons and the complete numbered walkthroughs are 127–152. Materials/textures/shader logic occupy 64–97, and the custom audit appears before the break and lab.
