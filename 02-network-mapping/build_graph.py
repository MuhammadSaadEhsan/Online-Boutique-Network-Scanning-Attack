import json

with open("02-network-mapping/output/topology.json") as f:
    topo = json.load(f)

depends_on = topo["depends_on"]
importance = topo["importance_score"]

dot = []
dot.append("digraph KubernetesTopology {")
dot.append("  rankdir=LR;")
dot.append("  node [shape=box, style=rounded];")

# Nodes with size based on importance
for svc, score in importance.items():
    size = 1 + (score / 10)
    dot.append(f'  "{svc}" [width={size}, height=0.6];')

# Edges
for src, targets in depends_on.items():
    for tgt in targets:
        dot.append(f'  "{src}" -> "{tgt}";')

dot.append("}")

with open("02-network-mapping/output/topology.dot", "w") as f:
    f.write("\n".join(dot))

print("[+] topology.dot generated")
