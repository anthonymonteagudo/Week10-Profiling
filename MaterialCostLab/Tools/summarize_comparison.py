"""Summarize per-launch medians from matched Unreal captures."""
import argparse
import csv
import json
import math
from pathlib import Path
from statistics import median

MODES = ("CPD", "MID", "Lean", "MasterOff", "MasterOn")
COLUMNS = {"frame": "FrameTime", "gpu": "GPUTime", "game": "GameThreadTime", "draws": "RHI/DrawCalls"}
START, STOP = 192, 576

def read_launch(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))[START:STOP]
    if len(rows) != STOP - START:
        raise ValueError(f"{path.name}: incomplete timing window")
    result = {}
    for key, column in COLUMNS.items():
        values = [float(row[column]) for row in rows]
        if any(not math.isfinite(v) or v < 0 for v in values):
            raise ValueError(f"{path.name}: invalid {column}")
        result[key] = median(values)
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    report = {}
    for mode in MODES:
        files = sorted(args.directory.glob(f"*-{mode}-Front.csv"))
        if len(files) != 3:
            parser.error(f"expected three {mode} launches, found {len(files)}")
        runs = [read_launch(file) for file in files]
        report[mode] = {key: round(median(r[key] for r in runs), 3) for key in COLUMNS}
        report[mode]["launches"] = [{k: round(v, 3) for k, v in r.items()} for r in runs]
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
