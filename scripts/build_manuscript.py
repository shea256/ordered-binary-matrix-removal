#!/usr/bin/env python3
"""Build with TeX Live: latex, amsmath, amssymb, geometry, hyperref, booktabs, lm.
Optional Markdown conversion requires Pandoc 3.6.4.
"""
import argparse, hashlib, json, shutil, subprocess, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('--regenerate-tex', action='store_true')
a = p.parse_args()
if a.regenerate_tex:
    body = subprocess.run(['pandoc', '-f', 'markdown+tex_math_single_backslash-superscript-subscript', '-t', 'latex', str(ROOT / 'manuscript.md')], check=True, capture_output=True, text=True).stdout
    preamble = r'''\documentclass[11pt]{article}
\usepackage{lmodern}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,booktabs,longtable,array}
\usepackage[margin=1in]{geometry}
\usepackage[unicode,hidelinks]{hyperref}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\setlength{\emergencystretch}{3em}
\begin{document}
'''
    (ROOT / 'tex/manuscript.tex').write_text(preamble + body.replace('\\section{', '\\section*{').replace('\\subsection{', '\\subsection*{') + '\n\\end{document}\n')
with tempfile.TemporaryDirectory() as td:
    for _ in range(3):
        run = subprocess.run(['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error', '-output-directory=' + td, str(ROOT / 'tex/manuscript.tex')], cwd=ROOT, capture_output=True, text=True)
        if run.returncode:
            print(run.stdout[-6000:])
            raise SystemExit(run.returncode)
    shutil.copyfile(Path(td) / 'manuscript.pdf', ROOT / 'manuscript.pdf')
    warnings = [line for line in run.stdout.splitlines() if 'Warning' in line or 'Overfull' in line]
version = subprocess.run(['pdflatex', '--version'], check=True, capture_output=True, text=True).stdout.splitlines()[0]
receipt = {'engine': version, 'passes': 3, 'shell_escape': False, 'warnings': warnings, 'artifacts': {}}
for name in ('manuscript.md', 'tex/manuscript.tex', 'manuscript.pdf'):
    data = (ROOT / name).read_bytes()
    receipt['artifacts'][name] = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
(ROOT / 'results/paper_build.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('PDF built; receipt: results/paper_build.json')
