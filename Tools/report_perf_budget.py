"""Report a frame-time budget check from independent Unreal CSV captures."""

import argparse
import json
import math
from pathlib import Path
from statistics import median

from compare_captures import read_window


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("captures", type=Path, nargs="+")
    parser.add_argument("--build-id", required=True)
    parser.add_argument("--device", required=True)
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--fps", type=float, default=60)
    parser.add_argument("--start", type=int, default=190)
    parser.add_argument("--stop", type=int, default=395)
    args = parser.parse_args()
    if not math.isfinite(args.fps) or args.fps <= 0 or not 0 <= args.start < args.stop:
        parser.error("require a positive finite FPS target and 0 <= start < stop")
    if len({path.resolve() for path in args.captures}) != len(args.captures):
        parser.error("supply each independent capture once")

    budget = 1000 / args.fps
    runs = []
    try:
        for path in args.captures:
            frame = sorted(read_window(path, args.start, args.stop)["FrameTime"])
            if frame[0] <= 0:
                raise ValueError(f"{path.name} contains a non-positive frame duration")
            p95 = frame[math.ceil(0.95 * len(frame)) - 1]
            runs.append({
                "capture": path.name,
                "median_ms": round(median(frame), 3),
                "p95_ms": round(p95, 3),
                "over_budget_frames": sum(value > budget for value in frame),
                "p95_exceeds_budget": p95 > budget,
            })
    except (OSError, ValueError) as error:
        parser.error(str(error))

    misses = sum(run["p95_exceeds_budget"] for run in runs)
    if len(runs) < 3:
        status = "insufficient_repeats"
    elif misses == len(runs):
        status = "over_budget"
    elif misses:
        status = "mixed_retest"
    else:
        status = "within_budget"
    print(json.dumps({
        "build": args.build_id, "device": args.device, "scenario": args.scenario,
        "budget_ms": round(budget, 3), "rows": [args.start, args.stop],
        "frames_per_run": args.stop - args.start, "status": status, "runs": runs,
    }, indent=2))


if __name__ == "__main__":
    main()
