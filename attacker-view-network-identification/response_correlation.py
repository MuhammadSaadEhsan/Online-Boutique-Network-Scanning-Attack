import json
import statistics
from itertools import combinations

with open("raw_observations.json") as f:
    data = json.load(f)

latencies = {
    k: [x["latency"] for x in v if isinstance(x["latency"], (int, float))]
    for k, v in data.items()
}

correlation = {}

for a, b in combinations(latencies.keys(), 2):
    diffs = [
        abs(latencies[a][i] - latencies[b][i])
        for i in range(min(len(latencies[a]), len(latencies[b])))
    ]
    correlation[f"{a}<->{b}"] = round(statistics.mean(diffs), 3)

with open("response_correlation.json", "w") as f:
    json.dump(correlation, f, indent=2)

print("[+] Response correlation calculated")
