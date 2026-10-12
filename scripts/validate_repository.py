#!/usr/bin/env python3
"""Validate package integrity; does not certify mathematics."""
import hashlib, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
for name in ('README.md','BASELINE.md','ATTEMPT.md','RESULT.md','RUNLOG.md','HANDOFF.md','ATTRIBUTION.md','NOTICE','LICENSE','manuscript.md','manuscript.pdf','tex/manuscript.tex'):
    assert (ROOT / name).is_file(), name
current = json.loads((ROOT / 'results/current.json').read_text())
assert current['status'] == 'candidate' and current['independent_review'] is False
assert current['new_result_formalized'] is True
assert (current['pattern_rows'],current['pattern_columns']) == (3,3)
assert current['pattern'] == [[0,1,1],[1,0,1],[1,1,0]]
assert current['normalization_exponent'] == 6
assert current['host_coefficient'] == 8
crown = current['formalization']
assert crown['applies_to_current_pattern'] is True
assert crown['applies_to_current_host'] is False
assert crown['formal_host']['n'] == '(14h+2)m'
assert crown['formal_host']['anchor_block_size'] == '2m on each axis'
assert crown['formal_host']['copy_count_upper_bound'] == '2 m n^4'
assert current['exact_copy_count'] == '7*m^4'
assert current['exact_repair_equality_claimed'] is False
report33 = json.loads((ROOT/current['verification_report']).read_text())
assert report33['pattern'] == current['pattern']
assert [x['copies'] for x in report33['records']] == [7*2**(4*h) for h in range(1,8)]
assert all(x['noncanonical_copies'] == x['unlocalized_copies'] == 0
           for x in report33['records'])
review33 = json.loads((ROOT/current['reviewer_verification_report']).read_text())
assert [x['copies'] for x in review33['records']] == [x['copies'] for x in report33['records'][:6]]
assert all(x['physical_copies'] == x['copies'] for x in review33['records'][:3])
assert (ROOT/current['separate_agent_review']['report']).is_file()
crown_audit = json.loads((ROOT/crown['audit']).read_text())
assert crown['status'] == crown_audit['status'] == 'crown_removal_theorem_formalized'
assert crown_audit['pattern'] == ['011','101','110']
assert crown_audit['written_host']['exact_count_formalized'] is False
assert crown_audit['end_to_end_removal_theorem_formalized'] is True
assert crown['final_removal_theorem_formalized'] is True
for flag in ('arbitrarily_small_epsilon_formalized',
             'arbitrarily_large_hosts_at_fixed_epsilon_formalized',
             'coarse_copy_count_formalized','arbitrary_repair_bound_formalized',
             'zero_cell_localization_formalized'):
    assert crown[flag] is True and crown_audit[flag] is True, flag
for flag in ('exact_copy_count_formalized', 'exact_repair_equality_formalized'):
    assert crown[flag] is False and crown_audit[flag] is False, flag
assert crown['named_theorems'] == crown_audit['theorem_count'] == len(crown_audit['axioms']) == 573
assert crown['checked_declarations'] == crown_audit['declaration_count'] == len(crown_audit['all_declarations']) == 2163
crown_modules = {'.'.join(p.relative_to(ROOT/'formal').with_suffix('').parts)
                 for p in (ROOT/'formal/OrderedRemoval').rglob('*.lean')}
assert set(crown_audit['kernel_replay']) == crown_modules
assert crown['modules_replayed'] == len(crown_modules) == 92
assert crown_audit['capstone'] == crown['capstone']
assert crown['capstone'] in crown_audit['axioms']
assert all(set(info['axioms']) <= {'propext','Quot.sound','Classical.choice'}
           for info in crown_audit['all_declarations'].values())
for name, expected in crown_audit['sources'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected, name
assert (ROOT/crown['semantic_review']).is_file()
# Preserve source binding for the original finite, review and formal checkpoints.
for checkpoint in ('three-by-three-checks-receipt', 'three-by-three-assurance', 'crown-formal-model-report'):
    data = json.loads((ROOT/'verification/reference'/f'{checkpoint}.json').read_text())
    hashes = data.get('hashes', data.get('sources', {}))
    assert hashes, checkpoint
    for name, expected in hashes.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected, (checkpoint, name)
# The rectangular theorem remains a separately scoped historical certificate.
previous = json.loads((ROOT/current['previous_result']).read_text())
assert (previous['pattern_rows'], previous['pattern_columns']) == (3,4)
assert previous['normalization_exponent'] == 7
assert previous['formalization']['applies_to_current_host'] is True
report34=json.loads((ROOT/previous['verification_report']).read_text())
assert report34['pattern'] == previous['pattern']
assert [x['copies'] for x in report34['results']] == [1632,101888,4743168,197525504,7757365248,293769052160]
assert all(x['bad_localization_copies']==0 for x in report34['results'])
review34=json.loads((ROOT/previous['reviewer_verification_report']).read_text())
assert [x['copies'] for x in review34['census']] == [x['copies'] for x in report34['results'][:4]]
assert (ROOT/previous['separate_agent_review']['report']).is_file()
# The rectangular certificate has its own scope and immutable source binding.
rect=previous['formalization']
rect_audit=json.loads((ROOT/rect['audit']).read_text())
assert rect['status']==rect_audit['status']=='rectangular_removal_theorem_formalized'
assert rect_audit['pattern']==['1001','1010','0111']
for flag in ('arbitrarily_small_epsilon_formalized',
             'arbitrarily_large_hosts_at_fixed_epsilon_formalized',
             'coarse_copy_count_formalized','arbitrary_repair_bound_formalized',
             'zero_cell_localization_formalized'):
    assert rect[flag] is True and rect_audit[flag] is True, flag
assert rect_audit['end_to_end_removal_theorem_formalized'] is True
assert rect['final_removal_theorem_formalized'] is True
assert rect['exact_copy_count_formalized'] is False
assert rect['exact_repair_equality_formalized'] is False
assert rect['named_theorems']==rect_audit['theorem_count']==len(rect_audit['axioms'])
assert rect['checked_declarations']==rect_audit['declaration_count']==len(rect_audit['all_declarations'])
rect_modules={'.'.join(p.relative_to(ROOT/'formal').with_suffix('').parts)
              for p in (ROOT/'formal/OrderedRemoval').rglob('*.lean')
              if 'Crown' not in p.parts}
assert set(rect_audit['kernel_replay'])==rect_modules
assert rect['modules_replayed']==len(rect_modules)
assert 'OrderedRemoval.Rectangular.no_polynomial_removal_bound' in rect_audit['axioms']
assert all(set(info['axioms']) <= {'propext','Quot.sound','Classical.choice'}
           for info in rect_audit['all_declarations'].values())
for name, expected in rect_audit['sources'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected, name
assert (ROOT/rect['semantic_review']).is_file()
# The existing Lean certificate concerns the previous host order. Retain its
# integrity checks without relabeling it as a certificate for the refinement.
status = json.loads((ROOT / current['formalization']['historical_metadata']).read_text())
assert status['status'] == 'candidate'
assert status['independent_review'] is False and status['new_result_formalized'] is True
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
assert formal['status'] == 'qualitative_removal_theorem_formalized'
assert formal['concrete_anchor_classification_formalized'] is True
audit = json.loads((ROOT / formal['audit']).read_text())
assert audit['end_to_end_removal_theorem_formalized'] is True
assert formal['final_removal_theorem_formalized'] is True
assert formal['exact_copy_count_formalized'] is False and audit['exact_copy_count_formalized'] is False
assert formal['canonical_sampler_bound_formalized'] is False and audit['canonical_sampler_bound_formalized'] is False
assert audit['theorem_count'] == len(audit['axioms']) == formal['named_theorems']
assert audit['declaration_count'] == len(audit['all_declarations']) == formal['checked_declarations']
assert 'OrderedRemoval.Concrete.matrix_anchor_counts' in audit['axioms']
for flag in ('zero_cell_localization_formalized', 'dummy_last_row_formalized',
             'zero_set_cardinality_bound_formalized', 'coarse_copy_count_formalized',
             'arbitrary_repair_bound_formalized'):
    assert formal[flag] is True and audit[flag] is True, flag
for name in ('Copy.zero_localization', 'matrix_zero_localization',
             'Copy.last_row_dummy', 'card_zeroCells_le'):
    assert 'OrderedRemoval.Concrete.' + name in audit['axioms'], name
for name in ('fixedH_eq_H4', 'exists_optimal_repair', 'Concrete.copyCount_le',
             'OrderedHost.hammingDistance_ge', 'concrete_host_bounds',
             'counterexample_sequence', 'no_polynomial_removal_bound',
             'no_polynomial_removal_bound_arbitrary_repairs'):
    assert 'OrderedRemoval.' + name in audit['axioms'], name
assert len(audit['kernel_replay']) == len(list((ROOT / 'formal/OrderedRemoval').glob('*.lean')))
assert (ROOT / formal['removal_semantic_review']).is_file()
removal = json.loads((ROOT / status['removal_reviewer_verification_report']).read_text())
assert [r['maximum_guard_frequency'] for r in removal['records']] == [2, 4, 8, 16]
assert all(r['unprotected_leaf_diagonal_frequency'] == r['required_upper_bound'] ** 2
           for r in removal['records'])
assert all(set(info['axioms']) <= {'propext', 'Quot.sound', 'Classical.choice'}
           for info in audit['all_declarations'].values())
assert all(set(used) <= {'propext', 'Quot.sound', 'Classical.choice'} for used in audit['axioms'].values())
for name, expected in audit['sources'].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
proof = (ROOT / current['proof_file']).read_text()
manuscript = (ROOT / 'manuscript.md').read_text()
body = proof[proof.index('## 1. Statement'):proof.index('## 8. Verification scope')]
body = body.replace('../verification/', 'verification/').replace('../BASELINE.md', 'BASELINE.md')
assert manuscript[manuscript.index('## 1. Statement'):manuscript.index('## 8. Verification and formal theorem')] == body
receipt = json.loads((ROOT / 'results/paper_build.json').read_text())
for name, expected in receipt['artifacts'].items():
    data = (ROOT / name).read_bytes()
    assert len(data) == expected['bytes']
    assert hashlib.sha256(data).hexdigest() == expected['sha256'], name
# Keep the README graphic attached and synchronized with the selected result.
figure = json.loads((ROOT / 'assets/pattern-size-history.json').read_text())
assert figure['current_result_id'] == current['result_id']
assert figure['pattern_shapes'][-1] == [current['pattern_rows'], current['pattern_columns']]
events = json.loads((ROOT / 'assets/pattern-size-events.json').read_text())['events']
event_by_id = {event['id']: event for event in events}
assert event_by_id['erebos-4']['shape'] == [current['baseline_pattern_rows'], current['baseline_pattern_columns']]
assert figure['event_ids'] == [event['id'] for event in events]
assert figure['pattern_shapes'] == [event['shape'] for event in events]
assert figure['timestamps'] == sorted(event['timestamp'] for event in events)
assert figure['timestamps'] == [event['timestamp'] for event in events]
assert figure['x_scale'] == 'linear UTC time'
assert figure['entries'] == [rows * columns for rows, columns in figure['pattern_shapes']]
assert figure['current_theorem_formalized'] == current['new_result_formalized']
assert figure['y_scale'] == 'logarithmic'
for name, expected in figure['artifacts'].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
assert re.search(r'!\[[^\]]*\]\(assets/pattern-size-history\.png\)', (ROOT / 'README.md').read_text())
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
