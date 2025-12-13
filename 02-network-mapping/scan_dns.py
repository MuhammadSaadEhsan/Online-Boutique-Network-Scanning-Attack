import json
import subprocess

def run(cmd):
    subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

# Get any running pod
pods_json = subprocess.check_output("kubectl get pods -o json", shell=True, text=True)
pods = json.loads(pods_json)

probe_pod = None
for pod in pods["items"]:
    if pod["status"]["phase"] == "Running":
        probe_pod = pod["metadata"]["name"]
        break

if not probe_pod:
    raise Exception("No running pod found for DNS scan")

# Get all services
services_json = subprocess.check_output("kubectl get svc -o json", shell=True, text=True)
services = json.loads(services_json)

dns_map = {}

for svc in services["items"]:
    name = svc["metadata"]["name"]
    run(f"kubectl exec {probe_pod} -- nslookup {name}")
    dns_map[name] = "RESOLVABLE"

with open("02-network-mapping/output/dns_map.json", "w") as f:
    json.dump(dns_map, f, indent=2)

print(f"[+] DNS scan complete using pod: {probe_pod}")
