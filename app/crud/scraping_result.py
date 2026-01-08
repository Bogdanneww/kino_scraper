import json
from pathlib import Path

FILE = Path("storage/results.json")


def save_result(data: dict):
    FILE.parent.mkdir(exist_ok=True)

    if FILE.exists():
        existing = json.loads(FILE.read_text())
    else:
        existing = []

    existing.append(data)
    FILE.write_text(json.dumps(existing, indent=2, ensure_ascii=False))
