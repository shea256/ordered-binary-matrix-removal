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
report = json.loads((ROOT / status['verification_report']).read_text())
assert len(report['pattern']) == status['pattern_size'] == 4
assert all(len(row) == 4 and set(row) <= {0,1} for row in report['pattern'])
assert status['anchor_size'] == 2 and status['host_coefficient'] == 14
assert report['anchor'] == [[0, 1], [1, 0]]
repair = json.loads((ROOT / status['repair_verification_report']).read_text())
assert sum(row['leaf_choices_checked'] for row in repair['flipped_parent_zero_set']) == 510
proof = (ROOT / status['proof_file']).read_text()
manuscript = (ROOT / 'manuscript.md').read_text()
assert manuscript[manuscript.index('## Statement'):] == proof[proof.index('## Statement'):].replace('../verification/', 'verification/')
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
