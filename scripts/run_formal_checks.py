#!/usr/bin/env python3
"""Build and audit the qualitative 4×4 removal theorem and its dependencies."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "formal"
ALLOWED_AXIOMS = {"propext", "Quot.sound", "Classical.choice"}


def run(*args, echo=True):
    result = subprocess.run(args, cwd=FORMAL, check=True, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if echo:
        print(result.stdout, end="", flush=True)
    return result.stdout


def main():
    version = run("lake", "env", "lean", "--version").strip()
    assert "version 4.34.1," in version, version
    run("lake", "build")
    files = sorted((FORMAL / "OrderedRemoval").glob("*.lean"))
    source_names = {}
    for path in files:
        source = path.read_text()
        module = "OrderedRemoval." + path.stem
        source_names[module] = re.findall(
            r"^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected)\s+)?theorem\s+(\S+)",
            source, re.M)
        assert not re.search(r"^\s*(?:axiom|opaque|unsafe)\b|\b(?:sorry|admit|native_decide)\b", source)
    # Discover compiled declarations by their owning module, including nested
    # namespaces, dotted theorem names, and private/generated declarations.
    # Cache moduleNames: constructing the array inside the loop is expensive.
    driver = FORMAL / ".lake" / "axiom-audit.lean"
    driver.write_text('''import OrderedRemoval
import Lean.Util.CollectAxioms
open Lean in
run_cmd do
  let env ← getEnv
  let modules := env.header.moduleNames
  for (name, ci) in env.constants.toList do
    let some idx := env.getModuleIdxFor? name | continue
    let mod := modules[idx.toNat]!
    if (`OrderedRemoval).isPrefixOf mod then
      let axioms ← collectAxioms name
      let kind := if ci.isTheorem then "theorem" else "declaration"
      IO.println s!"AUDIT\\t{mod}\\t{name}\\t{kind}\\t{String.intercalate "," (axioms.toList.map toString)}"
''')
    output = run("lake", "env", "lean", str(driver), echo=False)
    declarations = {}
    for line in output.splitlines():
        if not line.startswith("AUDIT\t"):
            continue
        _, module, name, kind, raw = line.split("\t")
        used = sorted(filter(None, raw.split(",")))
        assert set(used) <= ALLOWED_AXIOMS, (name, used)
        declarations[name] = {"module": module, "kind": kind, "axioms": used}
    assert declarations, output
    axioms = {}
    for module, names in source_names.items():
        for short in names:
            matches = [name for name, info in declarations.items()
                       if info["module"] == module and info["kind"] == "theorem"
                       and name.endswith("." + short)]
            assert len(matches) == 1, (module, short, matches)
            name = matches[0]
            axioms[name] = declarations[name]["axioms"]
    assert "OrderedRemoval.Concrete.Copy.anchor_counts" in axioms
    assert "OrderedRemoval.Concrete.matrix_anchor_counts" in axioms
    for name in ("Copy.zero_localization", "matrix_zero_localization",
                 "Copy.last_row_dummy", "card_zeroCells_le"):
        assert "OrderedRemoval.Concrete." + name in axioms
    for name in ("fixedH_eq_H4", "exists_optimal_repair", "Concrete.copyCount_le",
                 "OrderedHost.hammingDistance_ge", "concrete_host_bounds",
                 "counterexample_sequence", "no_polynomial_removal_bound",
                 "no_polynomial_removal_bound_arbitrary_repairs"):
        assert "OrderedRemoval." + name in axioms, name
    # Replay each local module into its imported environment, sequentially to
    # bound memory. This checks local proof terms again; it does not replay all
    # of Mathlib into a fresh environment or use a different proof assistant.
    replays = {}
    for module in sorted(source_names):
        replays[module] = run("lake", "env", "leanchecker", "-v", module).strip()
    source_files = files + [FORMAL / "OrderedRemoval.lean", FORMAL / "lean-toolchain",
                            FORMAL / "lakefile.toml", FORMAL / "lake-manifest.json"]
    receipt = {
        "status": "qualitative_removal_theorem_formalized",
        "end_to_end_removal_theorem_formalized": True,
        "coarse_copy_count_formalized": True,
        "arbitrary_repair_bound_formalized": True,
        "exact_copy_count_formalized": False,
        "canonical_sampler_bound_formalized": False,
        "concrete_anchor_classification_formalized": True,
        "zero_cell_localization_formalized": True,
        "dummy_last_row_formalized": True,
        "zero_set_cardinality_bound_formalized": True,
        "lean_version": version,
        "theorem_count": len(axioms),
        "declaration_count": len(declarations),
        "axioms": dict(sorted(axioms.items())),
        "all_declarations": dict(sorted(declarations.items())),
        "kernel_replay_scope": "each project module into its imported environment",
        "kernel_replay": replays,
        "sources": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in source_files},
    }
    out = ROOT / ".context"
    out.mkdir(exist_ok=True)
    (out / "formal-checks-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"{len(axioms)} named Lean theorems; {len(declarations)} declarations audited; module kernel replay passed.")
    print("The qualitative 4×4 removal theorem is formalized end to end. The sharper exact copy formula and canonical sampler bound are not formalized.")


if __name__ == "__main__":
    main()
