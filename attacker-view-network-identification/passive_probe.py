import time
import requests
import json
import statistics

BASE_URL = "http://localhost:8080"

# ENDPOINTS = {
#     "home": "/",
#     "product": "/product/0PUK6V6EV0",
#     "cart": "/cart",
#     "checkout": "/checkout"
# }

with open("discovered_endpoints.json") as f:
    paths = json.load(f)

ENDPOINTS = {p.strip("/").replace("/", "_") or "root": p for p in paths}


SAMPLES = 5
DELAY = 2  # seconds (safe)
TIMEOUT = 3  # seconds per request

results = {k: [] for k in ENDPOINTS}

def probe(path):
    start = time.time()
    try:
        r = requests.get(BASE_URL + path, timeout=TIMEOUT)
        status = r.status_code
    except Exception as e:
        status = "error"
    latency = round(time.time() - start, 3)
    return latency, status

print("[*] Starting attacker-side passive probing")

for i in range(SAMPLES):
    print(f"[*] Sample round {i+1}/{SAMPLES}")
    for name, path in ENDPOINTS.items():
        latency, status = probe(path)
        print(f"    {name:10} latency={latency}s status={status}")
        results[name].append({
            "latency": latency,
            "status": status
        })
        time.sleep(DELAY)

with open("raw_observations.json", "w") as f:
    json.dump(results, f, indent=2)

print("[+] Passive probing complete")
print("[+] Results written to raw_observations.json")
