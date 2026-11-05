# Optimization lab: furnished lounge

Investigate a real furnished environment for a **60 FPS target (16.67 ms per frame)**. Find one cost, test one change, and recommend whether to keep it. Preserve the warm interior lighting, furniture layout, readable books and reflective/translucent glass.

## Before class

Use Unreal Engine **5.7**. Follow the [project setup](Unreal/README.md) or open the complete classroom project supplied by your instructor. The public starter requires the free Fab Cigar Room Environment. Allow time for first-launch shader compilation. No C++ build is required for this lab.

## 0–8 minutes: establish a baseline

1. Open **Lounge_Unoptimized** under Content > OptimizationLab. Duplicate it for your edits. Keep the original and **Lounge_Reference** unchanged. Reference preserves the source treatment; it is not a certified optimized answer.
2. Explore in the editor. Use **Play > Standalone Game** for timing. Audit Camera selects a fixed view. In game, `ToggleDebugCamera` enables exploration; toggle it off and relaunch before matched captures.
3. Choose 1280×720 or another resolution your machine supports. Record resolution, scalability, screen percentage, RHI, hardware and warm-up. Use `r.SetRes 1280x720w`, `r.ScreenPercentage 100`, `r.VSync 0` and `t.MaxFPS 0`. Wait for shaders and streaming to settle.
4. In Lit, use `stat unit` and record three readings of Frame, Game, Draw and GPU. If GPU tracks Frame, inspect `stat gpu`. If CPU tracks Frame, investigate the corresponding thread or wait in Unreal Insights. A cap or an unstable capture must be resolved before interpreting savings.

Three readings are a spot check. For a stronger comparison, the supplied Capture-Lounge script makes three independent CSV launches. Its analysis window is rows 300–849 inclusive. See project setup for the command. Use matched launches rather than pooling all frames.

## 8–22 minutes: diagnose and test

Use **Tools > Week 10 Optimization > Validate and Generate Dashboard**. It reports loaded editor content and candidates, not GPU milliseconds. Use the custom optimization overlay, Light Complexity, Shader Complexity, Wireframe or the relevant shadow visualization to inspect a specific lead. Debug views change rendering: return to Lit and disable the overlay before timing.

Write a hypothesis before editing:

> If we change ___, we expect ___ to fall because ___. We will check that ___ remains correct in both the fixed view and a second angle.

Test one reversible change in your duplicate. Inspect the actual actor/component properties and the relevant render path. Save the map, relaunch Standalone and repeat the same conditions. Do not remove the room or hide quality regressions to meet budget. An empty dashboard is not proof that the level is optimized.

## 22–30 minutes: retest and recommend

| Evidence | Your team |
|---|---|
| Hardware, engine/build, RHI, map, resolution, quality, warm-up and capture window | |
| Required visual quality and second viewpoint | |
| Baseline Frame / Game / Draw / GPU readings in ms | |
| Supporting GPU pass or CPU track; exact actor/component | |
| Hypothesis and single change | |
| Retest readings in ms; per-launch median and p95 if CSVs are available | |
| Difference in median Frame and headroom against 16.67 ms | |
| Same-view before/after screenshots; second-view quality check | |
| Keep, revise or reject; uncertainty and the next discriminating test | |

A difference within observed launch variation is inconclusive. Explain what the experiment supports. Report recovered headroom separately from whether the frame meets budget. A valid failed hypothesis is useful evidence.

## Debrief questions

1. A 21.0 ms frame must recover how much time to reach 60 FPS?
2. GPU falls from 20.0 to 15.0 ms while Frame stays at 17.4 ms. What would you inspect next?
3. Why can a light with no authored distance cutoff still be culled? Why is a large radius only a lead?
4. How does Lumen affect a proposed switch to Static lighting? What must be true before a baked comparison is valid?
5. Why might changing Forced LOD have no useful effect on a Nanite mesh with only one conventional LOD?
6. Your audit flags a property but timing does not change. What conclusion is supported, and what would you measure next?

Use the [single Week 10 deck](Week10-Slides.pptx) and [optimization study guide](Optimization-Study-Guide.md) for profiler, view mode, lighting, Nanite, material, Niagara and asset workflow references. The material, debris and Niagara comparison projects are separate demonstrations; their historical timings are not this lounge's baseline.
