#!/usr/bin/env python3
"""Build the partial Lean development and audit every exported theorem.

Requires Lean/Lake from the pinned toolchain on PATH. This verifies the
stated lemmas; it does not upgrade them to an end-to-end removal theorem.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "formal"
ALLOWED_AXIOMS = {"propext", "Quot.sound", "Classical.choice"}


def run(*args):
    result = subprocess.run(args, cwd=FORMAL, check=True, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout, end="", flush=True)
    return result.stdout


def main():
    version = run("lake", "env", "lean", "--version").strip()
    assert "version 4.34.1," in version, version
    run("lake", "build")
    files = sorted((FORMAL / "OrderedRemoval").glob("*.lean"))
    names = []
    for path in files:
        source = path.read_text()
        namespace = re.search(r"^namespace (\S+)$", source, re.M).group(1)
        names += [namespace + "." + name for name in
                  re.findall(r"^theorem (\w+)", source, re.M)]
        assert not re.search(r"^\s*(?:axiom|opaque|unsafe)\b|\b(?:sorry|admit|native_decide)\b", source)
    assert names
    driver = FORMAL / ".lake" / "axiom-audit.lean"
    driver.write_text("import OrderedRemoval\n" +
                      "".join("#print axioms " + name + "\n" for name in names))
    output = run("lake", "env", "lean", str(driver))
    axioms = {}
    for name in names:
        match = re.search(r"'" + re.escape(name) +
                          r"' depends on axioms: \[([^\]]*)\]", output)
        if match:
            used = sorted(x.strip() for x in match.group(1).split(",") if x.strip())
        else:
            assert "'" + name + "' does not depend on any axioms" in output, name
            used = []
        assert set(used) <= ALLOWED_AXIOMS, (name, used)
        axioms[name] = used
    # This replays imported constants as well as our own declarations in a
    # fresh Lean kernel environment. It is not a different proof assistant.
    replay = run("lake", "env", "leanchecker", "--fresh", "-v", "OrderedRemoval")
    source_files = files + [FORMAL / "OrderedRemoval.lean", FORMAL / "lean-toolchain",
                            FORMAL / "lakefile.toml", FORMAL / "lake-manifest.json"]
    receipt = {
        "status": "partial_formalization",
        "end_to_end_removal_theorem_formalized": False,
        "lean_version": version,
        "theorem_count": len(names),
        "axioms": axioms,
        "kernel_replay": replay.strip(),
        "sources": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in source_files},
    }
    out = ROOT / ".context"
    out.mkdir(exist_ok=True)
    (out / "formal-checks-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"{len(names)} Lean theorems audited; fresh kernel replay passed.")
    print("Coverage is partial. Concrete host connections and the final theorem remain unformalized.")


if __name__ == "__main__":
    main()
