#!/usr/bin/env python3
"""Build and audit the 3×3 removal theorem with full quantifiers and its dependencies."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FORMAL = ROOT / "formal"
ALLOWED_AXIOMS = {"propext", "Quot.sound", "Classical.choice"}


def run(*args, echo=True):
    result = subprocess.run(args, cwd=FORMAL, check=False, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if echo or result.returncode:
        print(result.stdout, end="", flush=True)
    result.check_returncode()
    return result.stdout


def main():
    version = run("lake", "env", "lean", "--version").strip()
    assert "version 4.34.1," in version, version
    run("lake", "build", "OrderedRemoval", "OrderedRemoval.Rectangular.Complete",
        "OrderedRemoval.Crown.Complete")
    files = sorted((FORMAL / "OrderedRemoval").rglob("*.lean"))
    source_names = {}
    for path in files:
        source = path.read_text()
        module = ".".join(path.relative_to(FORMAL).with_suffix("").parts)
        source_names[module] = re.findall(
            r"^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected)\s+)?theorem\s+(\S+)",
            source, re.M)
        assert not re.search(r"^\s*(?:axiom|opaque|unsafe)\b|\b(?:sorry|admit|native_decide)\b", source)
    # Discover compiled declarations by their owning module, including nested
    # namespaces, dotted theorem names, and private/generated declarations.
    # Cache moduleNames: constructing the array inside the loop is expensive.
    driver = FORMAL / ".lake" / "crown-axiom-audit.lean"
    driver.write_text('''import OrderedRemoval
import OrderedRemoval.Rectangular.Complete
import OrderedRemoval.Crown.Complete
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
    for name in ("Copy.first_row_anchor", "Copy.last_col_anchor", "Copy.middle_col_nonanchor",
                 "Copy.zero_localization", "copyCount_le", "concrete_repair_lower_bound",
                 "concrete_host_bounds", "blowup_copyCount_le", "blowup_repair_normalized",
                 "no_polynomial_removal_bound"):
        assert "OrderedRemoval.Crown." + name in axioms, name
    # Replay each local module into its imported environment, sequentially to
    # bound memory. This checks local proof terms again; it does not replay all
    # of Mathlib into a fresh environment or use a different proof assistant.
    replays = {}
    for module in sorted(source_names):
        print(f"Kernel replay: {module}", flush=True)
        replays[module] = run("lake", "env", "leanchecker", "-v", module, echo=False).strip()
    source_files = [Path(__file__).resolve()] + files + [FORMAL / "OrderedRemoval.lean", FORMAL / "lean-toolchain",
                            FORMAL / "lakefile.toml", FORMAL / "lake-manifest.json"]
    receipt = {
        "status": "crown_removal_theorem_formalized",
        "pattern": ["011", "101", "110"],
        "end_to_end_removal_theorem_formalized": True,
        "capstone": "OrderedRemoval.Crown.no_polynomial_removal_bound",
        "formal_host": {"m": "2^h", "n": "(14h+2)m",
                        "anchor_block_size": "2m on each axis",
                        "copy_count_upper_bound": "2 m n^4",
                        "arbitrary_repair_lower_bound": "m^2",
                        "density_normalization": "n^6"},
        "written_host": {"n": "(8h+2)m", "anchor_block_size": "m on each axis",
                         "exact_count": "7m^4", "exact_count_formalized": False},
        "new_module_count": sum(".Crown." in module for module in source_names),
        "new_named_theorem_count": sum(name.startswith("OrderedRemoval.Crown.") for name in axioms),
        "new_declaration_count": sum(info["module"].startswith("OrderedRemoval.Crown.")
                                     for info in declarations.values()),
        "arbitrarily_small_epsilon_formalized": True,
        "arbitrarily_large_hosts_at_fixed_epsilon_formalized": True,
        "coarse_copy_count_formalized": True,
        "arbitrary_repair_bound_formalized": True,
        "zero_cell_localization_formalized": True,
        "exact_copy_count_formalized": False,
        "exact_repair_equality_formalized": False,
        "independent_peer_review": False,
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
    (out / "crown-formal-checks-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"{len(axioms)} named Lean theorems; {len(declarations)} declarations audited; module kernel replay passed.")
    print("The 3×3 theorem includes arbitrarily small epsilon and arbitrarily large hosts at that same epsilon. The proof uses doubled anchor blocks; the written 7m^4 count and repair equality are outside the certificate.")


if __name__ == "__main__":
    main()
