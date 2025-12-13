import json
import subprocess

def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True)

endpoints_raw = run("kubectl get endpoints -o json")
endpoints = json.loads(endpoints_raw)

output = []

for ep in endpoints["items"]:
    subsets = ep.get("subsets", [])
    addresses = []

    for s in subsets:
        for addr in s.get("addresses", []):
            addresses.append(addr.get("ip"))

    output.append({
        "service": ep["metadata"]["name"],
        "backend_ips": addresses
    })

with open("02-network-mapping/output/endpoints.json", "w") as f:
    json.dump(output, f, indent=2)

print("[+] Endpoint mapping complete")
