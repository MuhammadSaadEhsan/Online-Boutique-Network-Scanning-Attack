import json

with open("response_correlation.json") as f:
    corr = json.load(f)

THRESHOLD = 0.4  # small difference = shared backend

clusters = []

for pair, value in corr.items():
    if value < THRESHOLD:
        a, b = pair.split("<->")
        clusters.append([a, b])

with open("inferred_topology.json", "w") as f:
    json.dump({
        "clusters": clusters,
        "logic": "Endpoints with correlated latency inferred as shared backend"
    }, f, indent=2)

print("[+] Inferred attacker-side topology generated")
