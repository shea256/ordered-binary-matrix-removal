#!/usr/bin/env python3
"""Rehash the optional pinned cache. This does not build Lean."""
import hashlib, json
from pathlib import Path
root = Path(__file__).resolve().parent
manifest = json.loads((root / "source_manifest.json").read_text())
for f in manifest["files"]:
    data = (root / "upstream" / f.get("local_path", f["path"])).read_bytes()
    assert len(data) == f["bytes"]
    assert hashlib.sha256(data).hexdigest() == f["sha256"], f["path"]
print(json.dumps({"source_hashes_checked": len(manifest["files"]),
                  "upstream_commit": manifest["upstream_commit"],
                  "lean_build_performed": False}, indent=2))
