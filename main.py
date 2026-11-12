#!/usr/bin/env python3
"""
roblox-up-and-coming-forecast-01 entry.

Reads /input/history.ndjson (+ task.json), writes /output/forecast.json.

Model (measured on the practice window: baseline -43.51 -> this -41.29):
  - The Up-and-Coming chart reorders a stable pool and churns its lower ranks,
    so "no change" is overconfident. We keep the close order but calibrate the
    stay probability down and leave a tail. Rank re-ranking by player-count
    growth was measured and proved harmful on the archive data, so we do not
    do it; the close rank is the strongest signal.
"""
import json, os

INPUT_DIR = os.environ.get("MAKEFUN_INPUT_DIR", "/input")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

P_STAY = 0.4
P_NBR = 0.15
P_TAIL = 0.06
P_FIRST_NEXT = 0.3

def main():
    task = json.load(open(os.path.join(INPUT_DIR, "task.json")))
    places = task["places"]

    reads = []
    for line in open(os.path.join(INPUT_DIR, "history.ndjson")):
        line = line.strip()
        if not line:
            continue
        reads.append(json.loads(line))
    reads.sort(key=lambda d: d["at"])

    last = reads[-1]
    chart = sorted(last.get("up_and_coming") or [], key=lambda r: r["rank"])
    order = [int(r["universe_id"]) for r in chart]

    probabilities = []
    append = probabilities.append
    for place in range(1, places + 1):
        k = place - 1
        if k >= len(order):
            break
        append({"universe_id": order[k], "place": place, "p": P_STAY})
        if place == 1:
            if len(order) > 1:
                append({"universe_id": order[1], "place": place, "p": P_FIRST_NEXT})
            continue
        if k - 1 >= 0:
            append({"universe_id": order[k-1], "place": place, "p": P_NBR})
        if k + 1 < len(order):
            append({"universe_id": order[k+1], "place": place, "p": P_NBR})
        if k + 2 < len(order):
            append({"universe_id": order[k+2], "place": place, "p": P_TAIL})

    out = {"probabilities": probabilities, "top10": order[:places]}
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, task.get("output", "forecast.json")), "w") as f:
        json.dump(out, f)

if __name__ == "__main__":
    main()