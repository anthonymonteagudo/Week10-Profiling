# Week 10 · Unreal performance profiling

- [Download the editable Unreal 5.7 texture demos](https://github.com/anthonymonteagudo/Week10-Profiling/releases/tag/week10-ue57-texture-demos-v1)
- [Student lab](Student-Lab.md)
- [Lecture slides](Week10-Slides.pptx)
- [Capture comparison](Tools/compare_captures.py)
- [Frame-budget report](Tools/report_perf_budget.py)
- [Texture mask packer](Tools/pack_masks.py) and [practice inputs](Tools/DemoInputs)

For the texture demos, extract the release ZIP and open Week10ProfilingLab.uproject. The project opens ArrayDemo. Use Unreal Engine 5.7 for the assessment lab. Ask your instructor for the assigned DemoScene case and make a writable copy before making edits. Open the project, launch Standalone Game, and use the Audit Camera.

For an offline comparison of two matching Unreal CSV Profiler captures, run:

```powershell
python Tools/compare_captures.py "<baseline.csv>" "<retest.csv>"
```

The texture packer requires Python and Pillow. From the repository root, run:

```powershell
python Tools/pack_masks.py Tools/DemoInputs/AO.png Tools/DemoInputs/Roughness.png Tools/DemoInputs/Metallic.png Packed_ORM.png
```
