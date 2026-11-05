# Week 10 Unreal optimization lab

Requires Unreal Engine 5.7 on Windows. This content-only project needs no C++ compile. Allow several minutes for initial shader compilation.

## One-time setup

1. Obtain the free [Cigar Room Environment by Hane Studios](https://www.fab.com/listings/4da78da6-44b3-4adf-8883-219fe17b44d4) in your Fab library.
2. Add it to `Week10Assessment.uproject` through the Epic Games Launcher/Fab workflow. Keep its original `Content/Cigar_room` path.
3. Close this project in Unreal. In PowerShell from this folder run `.Setup-Lab.ps1`. Use `-Engine 'D:/Epic/UE_5.7'` if needed. If you already have the Fab pack in another project, use `-FabProject 'D:/MyProject/MyProject.uproject'` instead of adding it again.
4. Open `Week10Assessment.uproject`. It now opens **Lounge_Unoptimized**. The setup creates its own maps and materials, preserves the source Fab map, and refuses to overwrite an existing lab.

The public starter contains course-authored scripts, configuration and the editor plugin. Fab assets are acquired separately. Do not move their folder or commit it to a public repository.

## In class

Read [the student lab](Student-Lab.md), duplicate Lounge_Unoptimized, and write a hypothesis before editing. In Standalone Game, Audit Camera supplies the matched view. Use editor navigation to inspect another angle; in game `ToggleDebugCamera` enables exploration and toggling it again returns to the comparison view. Keep the furniture, warm lighting, readable books and glass.

**Tools > Week 10 Optimization** generates a dashboard at `Saved/Week10Optimization/index.html` or toggles candidate bounds. Enable editor Realtime for the overlay; disable the overlay before timing. Findings are inspection leads rather than measured savings. The generated local dashboard is current; the lecture's hosted dashboard is a historical snapshot.

For a longer capture, run from this folder:

```powershell
.\Tools\Capture-Lounge.ps1 -OutputDirectory Saved/Baseline-01
```

It makes three separate 1280×720 standalone launches with screenshots disabled. Use a fresh output directory for each treatment. Close other capture scripts first. Frame analysis uses rows 300–849 inclusive. From the repository root, compare a matched pair with:

```powershell
python Tools/compare_captures.py Unreal/Saved/Baseline-01/run-1.csv Unreal/Saved/Retest-01/run-1.csv --start 300 --stop 850
```

Pass `-Map '/Game/OptimizationLab/YourDuplicate'` to capture an edited duplicate. Record machine, quality settings, RHI and any changes in the conditions table in the handout. Repeat the comparison for each launch rather than combining all frames and hiding variation.

## If something fails

- Missing Cigar_room map: add the Fab content to this project at its original path, then run setup.
- Script execution blocked: invoke `powershell -ExecutionPolicy Bypass -File .\Setup-Lab.ps1` for this reviewed script only; this does not change the machine policy.
- Wrong engine: use UE 5.7 and supply its installation path; older engines cannot read newer saved assets.
- Existing lab: open it. Use a fresh starter copy to rebuild; do not delete a student's working maps.
- Checkerboard material: wait for shaders, then inspect the actual material slot. Two empty source wine-bottle slots are documented source data, not a download failure.
- Unexpected camera: stop debug camera or piloting, close/relaunch Standalone, and verify Audit Camera.
- Near-identical timing: report the variation and collect a longer or more targeted trace. An inconclusive treatment is valid evidence.
