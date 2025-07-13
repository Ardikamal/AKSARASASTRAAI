import json, os
from pathlib import Path

# cari path direktori static
BASE = Path(__file__).parent.parent
KATA = [w.strip().lower()
    for w in (BASE / "static/daftar_kata.txt")
        .read_text(encoding="utf-8")
        .splitlines()]

def handler(request):
    body = request.json()
    suf = body.get("akhiran", "").lower()
    hasil = [w for w in KATA if w.endswith(suf)]
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"hasil": hasil})
    }
