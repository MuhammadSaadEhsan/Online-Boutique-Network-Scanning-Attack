import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json

BASE_URL = "http://localhost:8080"
MAX_PAGES = 20
DELAY = 1.5

visited = set()
discovered = set()

def crawl(url):
    try:
        r = requests.get(url, timeout=5)
    except:
        return

    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup.find_all(["a", "form"]):
        link = tag.get("href") or tag.get("action")
        if not link:
            continue

        full = urljoin(BASE_URL, link)
        path = urlparse(full).path

        if path.startswith("/") and path not in visited:
            discovered.add(path)

queue = [BASE_URL]

while queue and len(visited) < MAX_PAGES:
    current = queue.pop(0)
    if current in visited:
        continue

    visited.add(current)
    crawl(current)
    time.sleep(DELAY)

    for p in list(discovered):
        full = urljoin(BASE_URL, p)
        if full not in visited:
            queue.append(full)

with open("discovered_endpoints.json", "w") as f:
    json.dump(sorted(discovered), f, indent=2)

print("[+] Discovered endpoints:")
for p in sorted(discovered):
    print(" ", p)
