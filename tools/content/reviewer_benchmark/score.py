"""Score blind verdicts on original editorial calibration examples."""
import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
VERDICTS = {"ready", "unclear", "incorrect", "repeat"}


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Repeated JSON key {key!r}")
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)


def validate(entries, expected_ids):
    if not isinstance(entries, dict):
        raise ValueError("Expected a JSON object keyed by case ID")
    if set(entries) != expected_ids:
        missing = sorted(expected_ids - set(entries))
        extra = sorted(set(entries) - expected_ids)
        raise ValueError(f"Case IDs differ. Missing {missing}. Extra {extra}.")
    for case_id, entry in entries.items():
        if not isinstance(entry, dict) or not isinstance(entry.get("verdict"), str) or entry["verdict"] not in VERDICTS:
            raise ValueError(f"{case_id} needs one verdict from {sorted(VERDICTS)}")
        if not isinstance(entry.get("reason"), str) or not entry["reason"].strip():
            raise ValueError(f"{case_id} needs a reason with mathematical evidence")


def evaluate(key, response):
    validate(response, set(key))
    counts = {"exact": 0, "detected": 0, "misses": 0, "false_alarms": 0, "wrong_category": 0}
    differences = []
    for case_id, target in key.items():
        wanted = target["verdict"]
        actual = response[case_id]["verdict"]
        if wanted != "ready" and actual != "ready":
            counts["detected"] += 1
        if wanted == actual:
            counts["exact"] += 1
            continue
        if wanted == "ready":
            counts["false_alarms"] += 1
        elif actual == "ready":
            counts["misses"] += 1
        else:
            counts["wrong_category"] += 1
        differences.append(case_id)
    return counts, differences


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("response", type=Path, help="JSON written by the blind reviewer")
    args = parser.parse_args()
    try:
        packet = read_json(HERE / "packet.json")
        key = read_json(HERE / "key.json")
        validate(key, {case["id"] for case in packet["cases"]})
        response = read_json(args.response)
        counts, differences = evaluate(key, response)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    flawed = sum(item["verdict"] != "ready" for item in key.values())
    print(f"Exact verdicts {counts['exact']}/{len(key)}. Defects flagged {counts['detected']}/{flawed}. "
          f"Misses {counts['misses']}. False alarms {counts['false_alarms']}/{len(key) - flawed} clean cases. "
          f"Wrong defect category {counts['wrong_category']}.")
    for case_id in differences:
        print(f"{case_id}: expected {key[case_id]['verdict']}, received {response[case_id]['verdict']}.")
        print(f"  Reviewer: {response[case_id]['reason']}")
        print(f"  Reference: {key[case_id]['reason']}")
    return int(bool(differences))


if __name__ == "__main__":
    sys.exit(main())
