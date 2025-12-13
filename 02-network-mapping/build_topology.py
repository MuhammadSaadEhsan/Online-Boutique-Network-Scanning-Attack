import json
import subprocess
from collections import defaultdict

def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True)

services = json.loads(run("kubectl get svc -o json"))
pods = json.loads(run("kubectl get pods -o json"))

service_names = {s["metadata"]["name"] for s in services["items"]}

# Dependency graph: who depends on whom
depends_on = defaultdict(set)
depended_by = defaultdict(set)

for pod in pods["items"]:
    pod_name = pod["metadata"]["name"]
    pod_service = pod_name.rsplit("-", 2)[0]  # generic heuristic

    for c in pod["spec"]["containers"]:
        for env in c.get("env", []):
            val = env.get("value", "")
            for svc in service_names:
                if svc.upper() in val.upper():
                    depends_on[pod_service].add(svc)
                    depended_by[svc].add(pod_service)

# Compute importance score
importance = {}
justification = {}

for svc in service_names:
    inbound_services = sorted(depended_by.get(svc, []))
    outbound_services = sorted(depends_on.get(svc, []))

    reasons = []

    if inbound_services:
        reasons.append(
            f"Depended on by {len(inbound_services)} service(s): {', '.join(inbound_services)}"
        )

    if outbound_services:
        reasons.append(
            f"Depends on {len(outbound_services)} downstream service(s): {', '.join(outbound_services)}"
        )

    if len(inbound_services) >= 3:
        reasons.append("Acts as shared network dependency (choke point)")

    justification[svc] = reasons


output = {
    "depends_on": {k: list(v) for k, v in depends_on.items()},
    "depended_by": {k: list(v) for k, v in depended_by.items()},
    "importance_score": importance,
    "justification": justification
}

with open("02-network-mapping/output/topology.json", "w") as f:
    json.dump(output, f, indent=2)

print("[+] Network topology inferred")
print("[+] Ranked services:")

for svc, score in sorted(importance.items(), key=lambda x: x[1], reverse=True):
    print(f"{svc:25} score={score}")
