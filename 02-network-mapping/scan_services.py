import json
import subprocess

def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True)

services_raw = run("kubectl get svc -o json")
services = json.loads(services_raw)

output = []

for svc in services["items"]:
    ports = []
    for p in svc["spec"].get("ports", []):
        ports.append({
            "port": p.get("port"),
            "targetPort": p.get("targetPort"),
            "protocol": p.get("protocol")
        })

    output.append({
        "name": svc["metadata"]["name"],
        "type": svc["spec"]["type"],
        "clusterIP": svc["spec"].get("clusterIP"),
        "ports": ports
    })

with open("02-network-mapping/output/services.json", "w") as f:
    json.dump(output, f, indent=2)

print("[+] Service scan complete")
