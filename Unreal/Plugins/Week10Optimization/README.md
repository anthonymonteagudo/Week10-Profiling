# Week 10 Optimization editor tools

Open the UE 5.7 project. PythonScriptPlugin and EditorScriptingUtilities must be enabled. This content-only plugin needs no C++ compile. The project and the student assessment both contain it.

Use **Tools → Week 10 Optimization**:

- **Validate and Generate Dashboard:** scan the loaded editor world, write `Saved/Week10Optimization/report.json` and a self-contained `index.html`, and open the page.
- **Toggle Custom Optimization View:** mark candidate component bounds over the current editor viewport. Enable viewport Realtime. Blue means information, amber means review and red means error. Toggle to refresh cached bounds after edits.
- **Disable Custom Optimization View:** unregister the drawing callback. Remaining marks expire within 0.25 seconds. Materials and level properties are never changed. A world change disables the view.
- **Open Last Dashboard:** open the most recent report.

This is a custom editor overlay, not an additional engine shader ViewMode enum. It works over the current viewport. Debug geometry is excluded from some high-resolution screenshot paths; capture the actual editor viewport when illustrating the overlay. Disable it before runtime timing.

The dashboard filters findings, records the actual property and policy, supplies a selection command for the Unreal Python console, exposes rule coverage and documented exceptions, and compares finding identities with an imported baseline. Imported JSON stays in the browser. The hosted version is a snapshot, not a live editor bridge.

Rules are configured in `Content/Python/audit_rules.json`. They are teaching thresholds rather than universal frame budgets. Findings cover local-light radius, authored distance cutoff, movable shadow casting, dense conventional/fallback render data, empty material slots, Niagara Effect Type availability and projected translucent bounds from Audit Camera. Projected bounds are only a candidate screen-overlap test; they do not count shaded pixels. Unsupported checks are recorded as unavailable.

An actor tag such as `OptAudit.Ignore.LIGHT_RADIUS` records an intentional exception for that rule. Add it only after documenting the reason. The finding remains visible with exception status. No automatic fixes run.

To attach explicit historical capture evidence in Unreal Python:

```python
import week10_optimization as opt
opt.run_audit(False, [r"C:\captures\baseline.csv", r"C:\captures\retest.csv"], start=190, stop=395)
```

The data-row window is zero-based and excludes `stop`. It must be complete and finite. Median, nearest-rank p95 and over-budget frame counts are calculated per file. Build, machine, camera, resolution, quality and warm-up conditions must be checked separately. A content flag is not a measured saving.

Scope is the loaded editor world. Runtime-spawned actors, unloaded cells, actual live particle counts and complete GPU residency are outside this scan. A clear Reference report is a known-good fixture under these rules, not a certification of untested features.

To refresh the assessment plugin from its canonical source, run `python Tools/install_optimization_tools.py` from the parent profiling project. Validate with `Tools/validate_optimization_tools.py` in a UE Python commandlet and `python Tools/test_report_writer.py` outside Unreal.

Additional lounge rules inspect Always shadow-cache invalidation and groups of 8+ distinct material-instance assets with the same immediate parent and no exposed scalar/vector/texture/static-switch overrides. Other property differences require manual comparison. Neither rule proves a runtime saving.

The JSON export now records an editor console snapshot (screen percentage, dynamic resolution mode, Nanite pixel error, sharpening, Detail Mode, selected quality groups and PSO-precache flag). These are global editor-process values, not effective per-view resolution or proof of a packaged configuration. Inventory separates light components with Affects World on/off; only enabled components enter light-policy findings. Visible light icons are not a count of effective lights.
