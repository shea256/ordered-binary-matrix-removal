#!/usr/bin/env python3
"""Validate package integrity; does not certify mathematics."""
import hashlib, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
for name in ('README.md','BASELINE.md','ATTEMPT.md','RESULT.md','RUNLOG.md','HANDOFF.md','ATTRIBUTION.md','NOTICE','LICENSE','manuscript.md','manuscript.pdf','tex/manuscript.tex'):
    assert (ROOT / name).is_file(), name
status = json.loads((ROOT / 'results/current.json').read_text())
assert status['status'] == 'candidate'
assert status['independent_review'] is False and status['new_result_formalized'] is False
report = json.loads((ROOT / 'verification/reference/compression-report.json').read_text())
assert len(report['anchor']['pattern']) == status['pattern_size'] == 15
receipt = json.loads((ROOT / 'results/paper_build.json').read_text())
for name, expected in receipt['artifacts'].items():
    data = (ROOT / name).read_bytes()
    assert len(data) == expected['bytes']
    assert hashlib.sha256(data).hexdigest() == expected['sha256'], name
links = 0
for path in ROOT.rglob('*.md'):
    if any(part in ('.git', '.context', 'upstream') for part in path.relative_to(ROOT).parts):
        continue
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if target.startswith(('https:', 'http:', '#', 'mailto:')):
            continue
        assert (path.parent / target.split('#')[0].strip('<>')).exists(), (path.name, target)
        links += 1
assert (ROOT / 'manuscript.pdf').read_bytes().startswith(b'%PDF-')
print(f'Package integrity passed: {links} local links; manuscript hashes; candidate status.')
