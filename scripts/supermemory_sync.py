#!/usr/bin/env python3
"""Upsert documentation files from this GitHub repo into SuperMemory Team Brain."""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.supermemory.ai/v3/documents"
MAX_CHARS = 80000
SPACE = os.environ.get("SUPERMEMORY_CONTAINER_TAG", "sm_org_shared")
PREFIX = os.environ.get("SUPERMEMORY_ID_PREFIX", "repo")
API_KEY = os.environ.get("SUPERMEMORY_API_KEY", "")
ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "dist", "build", "vendor", "__pycache__", ".venv", "venv", ".next", "coverage", "out"}
EXTS = {".md", ".mdx", ".markdown", ".txt", ".yaml", ".yml"}
SKIP_NAMES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock"}

def custom_id(rel: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_:-]", "_", rel.replace("/", "_"))
    return f"{PREFIX}:{slug}"[:100]
def iter_files():
    out = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if p.name in SKIP_NAMES:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() not in EXTS:
            continue
        if ".github" in p.parts and p.suffix.lower() in {".yml", ".yaml"}:
            continue
        out.append(p)
    return sorted(out)

def payload_for(path: Path):
    rel = path.relative_to(ROOT).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
    text = text.strip()
    if not text:
        return None
    body = f"SOURCE: {PREFIX}/{rel}\nUPDATED: from git workflow\n---\n{text}"
    if len(body) > MAX_CHARS:
        body = body[: MAX_CHARS - 20] + "\n...[truncated]"
    return {"content": body, "containerTag": SPACE, "customId": custom_id(rel), "metadata": {"source": PREFIX, "path": rel, "kind": "os-extract"}}

def post(doc):
    data = json.dumps(doc).encode("utf-8")
    req = urllib.request.Request(API, data=data, method="POST", headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")

def main() -> int:
    dry = "--dry-run" in sys.argv
    if not API_KEY and not dry:
        print("SUPERMEMORY_API_KEY secret is empty — skip ingest.", file=sys.stderr)
        return 0
    files = iter_files()
    if not files:
        print("No documentation files found — skip ingest.")
        return 0
    posted = 0
    for path in files:
        doc = payload_for(path)
        if not doc:
            continue
        if dry:
            print(f"dry-run {doc['customId']} -> {SPACE}")
            posted += 1
            continue
        status, body = post(doc)
        if status >= 400:
            print(f"HTTP {status} for {doc['customId']}: {body}", file=sys.stderr)
            return 1
        try:
            parsed = json.loads(body)
            doc_id = parsed.get("id") or parsed.get("data", {}).get("id") or "?"
        except Exception:
            doc_id = "?"
        print(f"upsert {doc['customId']} -> {doc_id} queued")
        posted += 1
    print(f"Posted {posted} document(s) to {SPACE}.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
