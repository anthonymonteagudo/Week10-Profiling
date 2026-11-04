"""Compare steady-state windows from two Unreal CSV Profiler captures."""

import argparse
import csv
import math
from pathlib import Path
from statistics import median

METRICS = ("FrameTime", "GPUTime", "GameThreadTime", "RenderThreadTime", "RHI/DrawCalls")
CAMERA = ("View/PosX", "View/PosY", "View/PosZ")


def read_window(path, start, stop):
    with path.open(encoding="utf-8-sig", newline="") as capture:
        rows = list(csv.DictReader(capture))
    window = rows[start:stop]
    if len(window) != stop - start:
        raise ValueError(f"{path.name} has fewer than {stop} data rows")
    values = {}
    for key in (*METRICS, *CAMERA):
        if key not in window[0]:
            continue
        try:
            samples = [float(row[key]) for row in window]
        except (TypeError, ValueError) as error:
            raise ValueError(f"{path.name} has missing or invalid {key} samples") from error
        if not all(math.isfinite(sample) for sample in samples):
            raise ValueError(f"{path.name} has non-finite {key} samples")
        values[key] = samples
    if "FrameTime" not in values:
        raise ValueError(f"{path.name} has no FrameTime column")
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("retest", type=Path)
    parser.add_argument("--start", type=int, default=190, help="first data row, zero-based")
    parser.add_argument("--stop", type=int, default=395, help="exclusive end data row")
    args = parser.parse_args()
    if not 0 <= args.start < args.stop:
        parser.error("require 0 <= start < stop")
    try:
        a, b = [read_window(path, args.start, args.stop) for path in (args.baseline, args.retest)]
    except (OSError, ValueError) as error:
        parser.error(str(error))

    if all(key in run for key in CAMERA for run in (a, b)):
        if any(max(a[key] + b[key]) - min(a[key] + b[key]) > 1.0 for key in CAMERA):
            parser.error("camera position moved within or between capture windows")
        print("Camera position matched within 1 Unreal unit per axis.")
    else:
        print("Camera position columns unavailable. Check capture screenshots.")
    print("Match camera orientation, resolution, scalability and workload separately.")
    print(f"Rows [{args.start}:{args.stop}] from {args.baseline.name} and {args.retest.name}")
    print("Metric                Unit    A median [min, max]      B median [min, max]      B - A")
    for key in METRICS:
        if key not in a or key not in b:
            print(f"{key:21} unavailable in at least one capture")
            continue
        before, after = a[key], b[key]
        unit = "calls" if key == "RHI/DrawCalls" else "ms"
        print(f"{key:21} {unit:5}   {median(before):7.2f} [{min(before):.2f}, {max(before):.2f}]"
              f"   {median(after):7.2f} [{min(after):.2f}, {max(after):.2f}]"
              f"   {median(after) - median(before):+.2f}")


if __name__ == "__main__":
    main()
