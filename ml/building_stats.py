import json

def analyze_buildings(json_path):

    with open(json_path) as f:
        data = json.load(f)

    buildings = data["features"]["lng_lat"]

    counts = {
        "no-damage": 0,
        "minor-damage": 0,
        "major-damage": 0,
        "destroyed": 0
    }

    for b in buildings:

        subtype = b["properties"].get("subtype","no-damage")

        if subtype not in counts:
            subtype = "no-damage"

        counts[subtype] += 1

    return counts
