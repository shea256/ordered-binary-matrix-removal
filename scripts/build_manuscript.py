#!/usr/bin/env python3
"""Build the paper with pdfLaTeX; --regenerate-tex also needs Pandoc 3.6.4.

The Markdown is the mathematical source. Presentation transforms add a title
and abstract, promote section headings, typeset Unicode mathematics, and make
repository links usable from a downloaded PDF. Pandoc's citeproc resolves
citations from references.bib. The reviewed proof is untouched.
See tex/preamble.tex and README.md for the TeX packages.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/shea256/ordered-binary-matrix-removal/blob/master/"
READER = "markdown+tex_math_single_backslash-superscript-subscript"
SUPERSCRIPTS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ʰ", "0123456789+-h")
SUBSCRIPTS = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
SYMBOLS = {
    "−": "-", "×": r"\times ", "≥": r"\ge ", "≤": r"\le ",
    "≠": r"\ne ", "∈": r"\in ", "∉": r"\notin ", "∧": r"\land ",
    "∨": r"\lor ", "∪": r"\cup ", "∖": r"\setminus ",
    "σ": r"\sigma ", "π": r"\pi ", "ε": r"\epsilon ", "β": r"\beta ",
    "ℕ": r"\mathbb{N}", "ℝ": r"\mathbb{R}", "⌊": r"\lfloor ",
    "⌋": r"\rfloor ", "→": r"\to ", "↦": r"\mapsto ",
    "⊆": r"\subseteq ", "∩": r"\cap ", "∅": r"\emptyset ",
    "…": r"\ldots ",
}


def normalize_math(text):
    """Translate notation only inside math nodes, including multi-digit scripts."""
    # Literal set braces in the prose are punctuation, not TeX grouping braces.
    text = re.sub(r"∈\{([^{}]+)\}", lambda m: "∈\\{" + m[1] + r"\}", text)
    text = re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ʰ]+",
                  lambda m: "^{" + m[0].translate(SUPERSCRIPTS) + "}", text)
    text = re.sub(r"[₀₁₂₃₄₅₆₇₈₉]+",
                  lambda m: "_{" + m[0].translate(SUBSCRIPTS) + "}", text)
    text = "".join(SYMBOLS.get(char, char) for char in text)
    # In mathematical prose these are operators, not products of letters.
    text = re.sub(r"(?<![\\A-Za-z])max(?=\()", r"\\max", text)
    text = re.sub(r"(?<![\\A-Za-z])mod(?![A-Za-z])", r"\\bmod", text)
    # Preserve relation spacing when a formula directly follows a prose word.
    text = re.sub(r"^[<=>]", r"{}\g<0>", text)
    return text


def raw_block(text):
    return {"t": "RawBlock", "c": ["latex", text]}


def transform(node):
    if isinstance(node, list):
        return [transform(item) for item in node]
    if not isinstance(node, dict):
        return node
    node = {key: transform(value) for key, value in node.items()}
    kind = node.get("t")
    if kind == "Math":
        node["c"][1] = normalize_math(node["c"][1])
    elif kind == "Link":
        target = node["c"][2][0]
        parsed = urlsplit(target)
        if not parsed.scheme and not parsed.netloc and parsed.path:
            node["c"][2][0] = REPOSITORY + quote(parsed.path, safe="/")
            if parsed.fragment:
                node["c"][2][0] += "#" + parsed.fragment
    elif kind == "Code" and re.fullmatch(r"[A-Za-z0-9_./-]+", node["c"][1]):
        # xurl can break long qualified Lean names and commit hashes.
        return {"t": "RawInline", "c": ["latex", r"\nolinkurl{" + node["c"][1] + "}"]}
    elif kind == "Strong" and any(item.get("t") == "Math" for item in node["c"]):
        node["c"].insert(0, {"t": "RawInline", "c": ["latex", r"\boldmath "]})
    elif kind == "Header":
        level, attr, content = node["c"]
        if level != 2:
            raise ValueError("Expected a second-level manuscript section")
        if content and re.fullmatch(r"\d+\.", content[0].get("c", "")):
            content = content[2:]  # Remove the literal number and its space.
        else:
            attr[1].append("unnumbered")
        node["c"] = [1, attr, content]
    return node


def render_tex():
    source = (ROOT / "manuscript.md").read_text()
    front = source.split("\n\n", 2)
    credit = re.fullmatch(r"(.+), with Codex assistance\. (.+)\.", front[1])
    if credit is None:
        raise ValueError("Expected the manuscript author and date line")
    result = subprocess.run(
        ["pandoc", "-f", READER, "-t", "json"],
        input=source, check=True, capture_output=True, text=True,
    )
    doc = json.loads(result.stdout)
    title, author, *body = doc["blocks"]
    if title["t"] != "Header" or title["c"][0] != 1 or author["t"] != "Para":
        raise ValueError("Expected the manuscript title followed by author/date")
    if any(block["t"] != "Para" for block in body[:2]):
        raise ValueError("Expected two opening abstract paragraphs")
    title_content = transform(title["c"][2])
    doc["meta"] = {
        "title": {"t": "MetaInlines", "c": title_content},
        "pdftitle": {"t": "MetaString", "c": front[0][2:].replace(r"\(", "").replace(r"\)", "").replace("×", "x")},
        "author": {"t": "MetaString", "c": credit[1]},
        "date": {"t": "MetaString", "c": credit[2]},
    }
    blocks = (
        [raw_block(r"\begin{abstract}")]
        + transform(body[:2])
        + [raw_block(r"\end{abstract}")]
        + transform(body[2:])
    )
    doc["blocks"] = []
    for index, block in enumerate(blocks):
        if block["t"] == "Para" and index + 1 < len(blocks) and blocks[index + 1]["t"] == "Table":
            # Keep each short table with the sentence that introduces it.
            doc["blocks"].append(raw_block(r"\Needspace{9\baselineskip}"))
        doc["blocks"].append(block)
    rendered = subprocess.run(
        ["pandoc", "-f", "json", "-t", "latex", "--number-sections",
         "--citeproc", "--bibliography", str(ROOT / "references.bib"),
         "--csl", str(ROOT / "tex/references.csl"),
         "--metadata", "link-citations=true", "--fail-if-warnings",
         "--template", str(ROOT / "tex/template.tex")],
        input=json.dumps(doc), capture_output=True, text=True,
    )
    if rendered.returncode:
        raise SystemExit(rendered.stderr)
    return rendered.stdout


def build_pdf():
    with tempfile.TemporaryDirectory() as directory:
        for _ in range(3):
            run = subprocess.run(
                ["pdflatex", "-no-shell-escape", "-interaction=nonstopmode",
                 "-halt-on-error", "-output-directory=" + directory,
                 str(ROOT / "tex/manuscript.tex")],
                cwd=ROOT, capture_output=True, text=True, errors="replace",
            )
            if run.returncode:
                print(run.stdout[-6000:])
                raise SystemExit(run.returncode)
        warnings = [
            line for line in run.stdout.splitlines()
            if "Warning" in line or "Overfull" in line
        ]
        shutil.copyfile(Path(directory) / "manuscript.pdf", ROOT / "manuscript.pdf")
    version = subprocess.run(
        ["pdflatex", "--version"], check=True, capture_output=True, text=True
    ).stdout.splitlines()[0]
    receipt = {
        "engine": version, "passes": 3, "shell_escape": False,
        "warnings": warnings, "artifacts": {},
    }
    for name in (
        "manuscript.md", "references.bib", "tex/references.csl",
        "tex/manuscript.tex", "tex/preamble.tex", "tex/template.tex",
        "scripts/build_manuscript.py", "manuscript.pdf", "proofs/four-by-four.md",
        "proofs/optimized-order.md", "proofs/three-by-four.md", "proofs/three-by-three.md",
    ):
        data = (ROOT / name).read_bytes()
        receipt["artifacts"][name] = {
            "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)
        }
    (ROOT / "results/paper_build.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print("PDF built; receipt: results/paper_build.json")
    for warning in warnings:
        print(warning)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--regenerate-tex", action="store_true")
    parser.add_argument("--check-tex", action="store_true",
                        help="check the generated LaTeX without modifying artifacts")
    args = parser.parse_args()
    if args.check_tex:
        if render_tex() != (ROOT / "tex/manuscript.tex").read_text():
            raise SystemExit("Generated LaTeX is stale; run --regenerate-tex")
        print("Generated LaTeX matches the Markdown, template and presentation transforms.")
        return
    if args.regenerate_tex:
        (ROOT / "tex/manuscript.tex").write_text(render_tex())
    build_pdf()


if __name__ == "__main__":
    main()
