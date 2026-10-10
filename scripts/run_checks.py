#!/usr/bin/env python3
"""Run exact checks and compare deterministic outputs with references."""
import json, platform, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
out = ROOT / ".context"
out.mkdir(exist_ok=True)
receipt = {"python": platform.python_version(), "platform": platform.platform(), "checks": []}
for name in ("compression", "adversarial"):
    start = time.monotonic()
    result = subprocess.run([sys.executable, str(ROOT / "verification" / ("check_" + name + ".py"))], check=True, capture_output=True, text=True)
    report = json.loads(result.stdout)
    (out / (name + "-report.json")).write_text(result.stdout)
    expected = json.loads((ROOT / "verification" / "reference" / (name + "-report.json")).read_text())
    assert report == expected, name + " reference differs"
    receipt["checks"].append({"name": name, "reference_matches": True, "elapsed_seconds": round(time.monotonic()-start, 3)})
    print(name + ": exact checks and reference comparison passed", flush=True)
subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_repository.py")], check=True)
(out / "checks-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print("All checks passed. Finite checks are not a universal theorem or independent review.")
