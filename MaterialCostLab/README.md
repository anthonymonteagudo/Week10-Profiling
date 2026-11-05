# Week 10 Â· Material cost lab

This isolated UE 5.7 C++ project creates a test scene at runtime. Build MaterialCostLabEditor for Win64 Development using the Visual Studio C++ toolchain. The project contains the material assets. Tools/build_materials.py can regenerate them using the Editor Python startup script.

```powershell
$ue = 'C:/Program Files/Epic Games/UE_5.7/Engine/Binaries/Win64/UnrealEditor.exe'
$project = (Resolve-Path ./MaterialCostLab.uproject).Path
& $ue $project -game -MaterialMode=CPD
```

Use MID, Lean, MasterOff or MasterOn in place of CPD to select a different treatment.

## Match the tests

- CPD and MID use the same 336 cubes, same camera, same scalar sequence and same color formula. CPD writes the scalar to index 0 per primitive and shares a material. MID creates one dynamic material instance per mesh component and writes the scalar as a material parameter. Dynamic instancing is enabled for both treatments.
- Lean, MasterOff and MasterOn render the same unlit plane with the same framing. Lean emits a constant. MasterOff uses a static switch to select the same constant and compile out the optional ripple. MasterOn uses the same graph design with the switch default enabled. The ripple performs deliberately expensive pixel math for teaching. This test does not measure shader compile time or package size.

From the project folder:

```powershell
.\Tools\Capture-Comparison.ps1 -Kind Visual -OutputDirectory Saved/MaterialVisual-01
.\Tools\Capture-Comparison.ps1 -Kind Timing -OutputDirectory Saved/MaterialTiming-01
python Tools/summarize_comparison.py Saved/MaterialTiming-01
```

Use fresh output directories. The timing runner rotates treatment order and records three launches for each mode without screenshots. Summaries use Unreal CSV rows 192–575 per launch. The test uses Standalone at 2560 × 1440, uncapped with VSync off. Raw captures are local.


## Material and shader logic experiments

The expanded project also accepts `-MaterialMode=DynamicZero`, `UVPixel` and `UVVertex`. No C++ change or rebuild is needed to add these modes: the existing runtime loader selects their material assets.

- **Feature removal:** DynamicZero uses a runtime scalar RippleWeight = 0 to blend the procedural ripple out. MasterOff compiles the feature branch out with a Static Switch. Both intend the same flat color. Inspect target Platform Stats and compare the actual output and GPU timing. A zero scalar is not a compile-time promise that the feature was removed.
- **Stage placement:** UVPixel transforms UVs by `UV * 8 + (0.23, 0.17)` before the texture sample in the pixel graph. UVVertex passes the same affine transform through a Vertex Interpolator before sampling. The same checker, plane and camera make alignment differences visible. Interpolators/vertex work cost something; a tiny UV operation may show no meaningful frame saving. Nonlinear operations need a separate tessellation/quality test.

Run a visual check and a separate repeated timing capture with fresh output directories:

```powershell
.\Tools\Capture-Shader-Logic.ps1 -Kind Visual -Experiment Feature -OutputDirectory Saved/Shader-Feature-Visual
.\Tools\Capture-Shader-Logic.ps1 -Kind Timing -Experiment Feature -OutputDirectory Saved/Shader-Feature-Timing
.\Tools\Capture-Shader-Logic.ps1 -Kind Visual -Experiment UV -OutputDirectory Saved/Shader-UV-Visual
.\Tools\Capture-Shader-Logic.ps1 -Kind Timing -Experiment UV -OutputDirectory Saved/Shader-UV-Timing
```

Each timing experiment launches A, B, B, A, A, B at 2560×1440. Analyze rows 192–575 inclusive, separately per launch, and record quality/API settings. Timing runs do not take screenshots. The original Capture-Comparison and its five-mode summary are unchanged.

Open `/Game/Lab/M_DynamicZero`, `M_MasterOff`, `M_UVPixel` and `M_UVVertex` in the Material Editor for Stats, Platform Stats and generated code. Match feature level, pass and quality. Run `Tools/build_shader_experiments.py` via Unreal Editor Python to regenerate the added graphs and owned checker texture. It leaves the original five graphs intact and uses their shared generator helpers; use a copy before editing examples.

The [student study guide](https://github.com/anthonymonteagudo/Week10-Profiling/blob/main/Optimization-Study-Guide.md#material-and-shader-logic) supplies the worksheet, optimization checklist and image-quality tests. This unlit conventional-material lab isolates concepts; it does not certify Substrate, mobile or Nanite shader performance.
