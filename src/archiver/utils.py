import requests
from typing import List


def load_blocklist(url: str) -> List[str]:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    lines = response.text.splitlines()

    patterns = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append("*." + line.lower())
        patterns.append(line.lower())
    return patterns
