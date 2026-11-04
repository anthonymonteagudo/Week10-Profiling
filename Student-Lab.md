# Week 10 Optimization Triage War Room

You are reviewing a small gallery for a 60 FPS target, or **16.67 ms per frame**. Your team will test one change and decide whether it should ship. In the lighting case, preserve the shape of the blue sphere and its contact shadow. In the glass case, keep the blue sphere and amber trim readable through the glass.

## 0–8 minutes · Baseline

Open your writable copy of `Week10Assessment.uproject` in Unreal Engine 5.7. Use Reference to establish the intended view, then open your assigned Lighting or Glass map under Content → Assessment. In the Play menu choose Standalone Game. The level opens on Audit Camera. Stay in that view. In the console use `r.SetRes 2560x1440w`, `r.ScreenPercentage 100`, `r.VSync 0` and `t.MaxFPS 0`. If your screen requires a smaller window, use 1280×720 for both runs and record that choice. Record your machine and scalability settings. Use the same mode and settings for both measurements. Allow shader compilation to finish and wait for timings to stabilize. In the console, run `stat unit` and record three readings a few seconds apart. Compare Frame, Game, Draw and GPU across those readings. If results cluster near a cap or vary substantially, record that before interpreting the result.

Use `stat gpu` to look for a costly rendering pass if GPU time tracks Frame. If Game or Draw tracks Frame, examine the appropriate thread in Unreal Insights or use instructor-provided capture evidence. Shader Complexity and Light Complexity help you decide where to inspect. They are visual diagnostics, so confirm any suspected cost with timing.

## 8–22 minutes · Diagnosis and change

Pick one cost supported by a timing signal and a specific scene observation. Write your hypothesis before editing. Use this format.

> If we change ___, we expect ___ to fall because ___. We will check that ___ remains visible in the comparison view.

If you already have a Week 7 audit tool, adapt one read-only rule to report a suspect actor or component. Include its identity, the property observed and the threshold or policy used. Try the rule on one intentional exception or known-good actor before trusting it. You can also inspect Details and the Outliner by hand.

Take a baseline screenshot, close the game window and make one reversible change in the editor. Save the level before relaunching Standalone Game for the retest. Actors created for the exercise are under Showroom.

## 22–30 minutes · Retest and recommendation

Use the same view and settings. Record three new readings, compare their median and range, and capture the same view again. Treat three readings as a quick check. Use a per-frame CSV to estimate p95. Save your recommendation even if your change failed. A difference smaller than the observed spread may need a longer capture.

| Evidence | Your team |
|---|---|
| Capture conditions and visual requirement | |
| Baseline Frame / Game / Draw / GPU in ms, three readings each | |
| Suspected cost and supporting pass, actor or property | |
| Hypothesis and one change | |
| Retest Frame / Game / Draw / GPU in ms, three readings each | |
| Difference in median Frame time and headroom or shortfall against 16.67 ms | |
| Before and after screenshots and visible impact | |
| Keep, revise or reject, with the next measurement you would take | |

For the art director, point to what changed in the image and where a player would notice. For the engineering lead, name the cost that changed, how repeatable the result was and whether the frame met budget.

## Budget warm-up

A 60 FPS target gives you 16.67 ms. If a frame takes 21.0 ms, how much time must you recover? If the GPU estimate falls from 20.0 to 15.0 ms but Frame settles at 17.4 ms, what would you measure next?

## Exit ticket

Name one additional measurement you would take and the decision that measurement would inform.


## Evidence warm-up

For each scene, name the first check and the evidence that would change your mind.

1. A steady slow frame appears when the camera fills with layered glass. Game stays similar while GPU rises.
2. Walking into a new room produces a brief hitch. Once the player stops, the frame returns to budget.
3. A texture pool warning appears while the frame stays within budget. Distant signs become blurry.

Keep the performance requirement and the quality requirement separate. In the third example, the warning and degraded image matter even when FPS stays on target.


## Optional Unreal Python starter

Run this in the Unreal Editor Python console while the level is open and the game window is closed. It lists currently loaded actors. Add a rule that inspects the properties relevant to your hypothesis.

```python
import unreal

actor_editor = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for actor in actor_editor.get_all_level_actors():
    unreal.log(f"{actor.get_class().get_name()}  {actor.get_path_name()}")
```

The scan covers loaded actors in the editor world. Load the relevant World Partition region before interpreting a missing result.



## Guided demo reference

- **Profiler and dashboard.** Start with Frame, Game, Draw and GPU in stat unit. If GPU appears limiting, use stat gpu to identify a pass. In the CSV or dashboard, compare the same steady interval for both runs. Timing columns use milliseconds. Draw calls count submissions. A change in draw calls is evidence about submitted work.
- **Shader Complexity.** Compare a single glass layer with overlapping layers in the editor view. The colors estimate shader work and can help locate costly screen regions. Return to Lit and check the suspected pass in a timed capture.
- **Simplygon LODs.** A level of detail is a mesh version selected as the object's projected size changes. Compare the generated triangle counts, then inspect the silhouette and transitions as the camera moves. Use GPU timing to check the effect on the tested workload.
- **Channel packing and arrays.** Channel packing puts several scalar masks in one image. For the class pack, read red as ambient occlusion, green as roughness and blue as metallic with sRGB off. A texture array groups compatible images into numbered slices. Use the same UV coordinates and switch the slice index to select a different image.

In the instructor project, `/Game/Week10Demo` contains the examples for these asset demos. In `SM_LOD_Demo`, force LOD0, LOD1 and LOD2, then compare the silhouette and return to Auto. This sample uses Unreal's conventional mesh reduction. In `T_Demo_ORM`, solo each channel and verify the circle, vertical gradient and half-image split. In the `ArrayDemo` level, the left and right planes use instances of the same material. Open the instances and find the scalar value that selects each stripe image.

During your retest, record which conditions you held constant. If the A and B timing ranges overlap substantially, repeat the runs before making a strong claim. Keep the matched screenshots so the team can assess the visual cost alongside the timings.

### Practice with the recorded glass captures

The worked instructor example uses the earlier showroom and its own Audit Camera. Use these values for the debrief. Compare your assigned case against your own baseline. A has overlapping glass panes. B retains one pane. The scene target is 60 FPS, which gives each frame about 16.67 ms.

| Metric | A | B |
|---|---:|---:|
| Median frame time | 15.88 ms | 6.80 ms |
| 95th-percentile frame time | 17.49 ms | 8.10 ms |
| Median GPU time | 15.33 ms | 5.98 ms |

The 95th percentile, or p95, is the frame time that roughly 95% of the captured frames met or beat.

1. Compare the median and p95 with the frame budget. Which one reveals that A still had slow frames?
2. Compare the focal display in the two screenshots your instructor shows. Describe one detail that changed for the viewer.
3. Decide whether to keep the edit for this view. Name a second camera position that could change your recommendation.

## From one A/B test to a nightly check

Sketch a run the next team could repeat. Record the build revision, machine and GPU driver, map and camera or replay, resolution, quality settings, warm-up condition, and which frames to capture. Save a CSV and a log per launch. Repeat on the same machine before interpreting the result.

| Example result at a 60 FPS target | What should the bot report? What would you do next? |
|---|---|
| p95 rises from about 10 ms to 13 ms on three matched runs | |
| One of three p95 results exceeds 16.67 ms | |
| The game exits before producing a CSV | |
| A fixed-camera run passes, but the game hitches when entering the next room | |

Start with stat unit and stat gpu for a live timing lead. Use Unreal Insights to examine work around a hitch. Use RenderDoc to identify a particular draw, texture, or pipeline state in a captured frame.

## Debrief the slow run in Timing Insights

At the worst row in the packaged run, Frame was 57.8 ms, GPU reported 6.1 ms, RenderThread was 57.7 ms and RHIThread was 53.2 ms. Which track would you open first? These times can overlap.

Your instructor will open a separate traced launch and select 5.108–5.138 seconds. Find the GameThread frame sync, render-thread visibility wait and RHI present wait. Compare when they begin and end. Write one statement the trace supports and one test that could help identify what caused the wait.
