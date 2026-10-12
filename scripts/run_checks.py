#!/usr/bin/env python3
"""Run exact checks and compare deterministic outputs with references."""
import json, platform, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
out = ROOT / ".context"
out.mkdir(exist_ok=True)
receipt = {"python": platform.python_version(), "platform": platform.platform(), "checks": []}
for name in ("compression", "adversarial", "refinement", "four", "four_repair", "four_literal", "four_reviewer", "four_localization", "four_removal", "optimized_order", "optimized_order_reviewer", "three_by_four", "three_by_four_reviewer", "asymmetric"):
    start = time.monotonic()
    result = subprocess.run([sys.executable, str(ROOT / "verification" / ("check_" + name + ".py"))], check=True, capture_output=True, text=True)
    report = json.loads(result.stdout)
    (out / (("asymmetric-template" if name == "asymmetric" else name.replace("_", "-")) + "-report.json")).write_text(result.stdout)
    expected = json.loads((ROOT / "verification" / "reference" / (("asymmetric-template" if name == "asymmetric" else name.replace("_", "-")) + "-report.json")).read_text())
    # The semantic reviewers record Python separately from mathematical output.
    if name in ("four_localization", "four_removal", "optimized_order_reviewer", "three_by_four_reviewer"):
        report = {k: v for k, v in report.items() if k != "python"}
        expected = {k: v for k, v in expected.items() if k != "python"}
    assert report == expected, name + " reference differs"
    receipt["checks"].append({"name": name, "reference_matches": True, "elapsed_seconds": round(time.monotonic()-start, 3)})
    print(name + ": exact checks and reference comparison passed", flush=True)
def deterministic(value):
    if isinstance(value, dict):
        return {k: deterministic(v) for k, v in value.items() if k != 'seconds'}
    if isinstance(value, list):
        return [deterministic(v) for v in value]
    return value

for name, source in (
    ('three-by-three-discovery', 'experiments/three_by_three_candidate.py'),
    ('three-by-three', 'verification/check_three_by_three.py'),
    ('three-by-three-reviewer', 'verification/check_three_by_three_reviewer.py'),
    ('wang-baseline', 'verification/check_wang_baseline.py'),
):
    start = time.monotonic()
    output = out / (name + '-report.json')
    result = subprocess.run([sys.executable, str(ROOT/source), '--output', str(output)],
                            check=True, capture_output=True, text=True)
    report = json.loads(output.read_text())
    expected = json.loads((ROOT/'verification/reference'/(name+'-report.json')).read_text())
    if name == 'three-by-three-reviewer':
        # Optional SAT repair searches are archived evidence, not part of this
        # standard-library reproduction of the complete finite census.
        expected.pop('exact_repair_distance', None)
    assert deterministic(report) == deterministic(expected), name + ' reference differs'
    receipt['checks'].append({'name': name, 'reference_matches': True,
                             'elapsed_seconds': round(time.monotonic()-start, 3)})
    print(name + ': exact checks and reference comparison passed', flush=True)
subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_repository.py")], check=True)
(out / "checks-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print("All checks passed. Finite checks are not a universal theorem or independent review.")
