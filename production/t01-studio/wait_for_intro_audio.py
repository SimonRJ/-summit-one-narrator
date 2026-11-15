"""Start rendering once every Voice C scene is present across two recording runs."""

import argparse
import json
from pathlib import Path
import subprocess
import time


ROOT = Path(__file__).resolve().parents[2]


def lane_scenes(plan):
    weighted = []
    for lesson in plan["lessons"]:
        script = json.loads((ROOT / f"production/scripts/{lesson}.json").read_text())
        allowed = plan.get("scenes", {}).get(lesson)
        for scene in script["scenes"]:
            if allowed is None or scene["n"] in allowed:
                weighted.append((len(scene["narration"].split()), (lesson, scene["n"])))
    workers = min(len(weighted), plan.get("workers", 19))
    lanes = [set() for _ in range(workers)]
    sizes = [0] * workers
    for weight, scene in sorted(weighted, key=lambda pair: -pair[0]):
        lane = min(range(workers), key=sizes.__getitem__)
        lanes[lane].add(scene)
        sizes[lane] += weight
    return {f"intro-voice-lane-{i}": scenes for i, scenes in enumerate(lanes, 1)}


def have_recorded(repo, run, lanes):
    raw = subprocess.check_output(
        ["gh", "api", f"repos/{repo}/actions/runs/{run}/artifacts?per_page=100"], text=True,
    )
    artifacts = json.loads(raw)["artifacts"]
    return set().union(*(lanes[entry["name"]] for entry in artifacts
                         if not entry["expired"] and entry["name"] in lanes))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo")
    parser.add_argument("primary", type=int)
    parser.add_argument("retry", type=int)
    args = parser.parse_args()
    retry = json.loads((ROOT / "production/t01-studio/intro_narration_plan.json").read_text())
    first_lanes = lane_scenes({"lessons": [f"S{i:03}" for i in range(1, 6)]})
    retry_lanes = lane_scenes(retry)
    required = set().union(*first_lanes.values())
    for _ in range(120):
        try:
            found = have_recorded(args.repo, args.primary, first_lanes) | have_recorded(args.repo, args.retry, retry_lanes)
        except subprocess.CalledProcessError:
            print("The artifact listing was temporarily unavailable.", flush=True)
        else:
            print(f"{len(found & required)} of {len(required)} required Voice C scenes are ready.", flush=True)
            if required <= found:
                return
        time.sleep(20)
    raise TimeoutError("Voice C scene coverage is still incomplete")


if __name__ == "__main__":
    main()
