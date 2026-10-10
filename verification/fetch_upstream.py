#!/usr/bin/env python3
"""Fetch pinned primary text sources and hash them (no binary downloads)."""
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

COMMIT = "fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb"
DEST = Path(__file__).resolve().parent / "upstream"
API = "https://api.github.com/repos/openai/math/contents/"
RAW = "https://raw.githubusercontent.com/openai/math/" + COMMIT + "/"
PREPRINT = "preprints/Polynomial-removal-fails-for-ordered-binary-matrices-September-25-2026/"


def retrieve(path):
    try:
        data = urllib.request.urlopen(RAW + path).read()
    except Exception as error:
        return {"path": path, "error": str(error)}
    # Preserve upstream Markdown as source text so repository link validation
    # does not mistake the partial snapshot for a complete upstream checkout.
    local_path = path + ".source" if path.endswith(".md") else path
    target = DEST / local_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {"path": path, "local_path": local_path,
            "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def main():
    expected = json.loads((DEST.parent / "source_manifest.json").read_text())
    assert expected["upstream_commit"] == COMMIT
    paths = [f["path"] for f in expected["files"]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        manifest = list(pool.map(retrieve, paths))
    for actual, reference in zip(manifest, expected["files"]):
        assert actual.get("sha256") == reference["sha256"], actual
        assert actual.get("bytes") == reference["bytes"], actual
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / "manifest.json").write_text(json.dumps({"upstream_commit": COMMIT,
        "retrieved_utc": datetime.now(timezone.utc).isoformat(), "files": manifest}, indent=2) + "\n")
    print(json.dumps({"downloaded": sum("sha256" in x for x in manifest),
                      "bytes": sum(x.get("bytes", 0) for x in manifest),
                      "errors": [x for x in manifest if "error" in x]}, indent=2))


if __name__ == "__main__":
    main()
