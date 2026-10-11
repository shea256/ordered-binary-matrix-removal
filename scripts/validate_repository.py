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
literal = json.loads((ROOT / status['literal_verification_report']).read_text())
assert [x['copies'] for x in literal['literal_censuses']] == [128, 18944, 1687552, 123207680, 128]
assert all(x['copies_outside_zero_set'] == 0 for x in literal['literal_censuses'])
reviewer = json.loads((ROOT / status['reviewer_verification_report']).read_text())
assert [x['h'] for x in reviewer['checks']] == list(range(1, 8))
review = status['separate_agent_review']
assert (ROOT / review['report']).is_file() and review['independent_peer_review'] is False
formal = status['formalization']
assert formal['status'] == 'partial' and formal['concrete_anchor_classification_formalized'] is True
audit = json.loads((ROOT / formal['audit']).read_text())
assert audit['end_to_end_removal_theorem_formalized'] is False
assert audit['theorem_count'] == len(audit['axioms']) == formal['named_theorems']
assert 'OrderedRemoval.Concrete.matrix_anchor_counts' in audit['axioms']
for flag in ('zero_cell_localization_formalized', 'dummy_last_row_formalized',
             'zero_set_cardinality_bound_formalized'):
    assert formal[flag] is True and audit[flag] is True, flag
for name in ('Copy.zero_localization', 'matrix_zero_localization',
             'Copy.last_row_dummy', 'card_zeroCells_le'):
    assert 'OrderedRemoval.Concrete.' + name in audit['axioms'], name
assert all(set(info['axioms']) <= {'propext', 'Quot.sound', 'Classical.choice'}
           for info in audit['all_declarations'].values())
assert all(set(used) <= {'propext', 'Quot.sound', 'Classical.choice'} for used in audit['axioms'].values())
for name, expected in audit['sources'].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
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
    if any(part in ('.git', '.context', '.lake', 'upstream') for part in path.relative_to(ROOT).parts):
        continue
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if target.startswith(('https:', 'http:', '#', 'mailto:')):
            continue
        assert (path.parent / target.split('#')[0].strip('<>')).exists(), (path.name, target)
        links += 1
assert (ROOT / 'manuscript.pdf').read_bytes().startswith(b'%PDF-')
print(f'Package integrity passed: {links} local links; manuscript hashes; candidate status.')
