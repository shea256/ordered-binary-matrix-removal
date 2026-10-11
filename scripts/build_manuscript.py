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
\usepackage{amsmath,amssymb,booktabs,longtable,array,calc}
\usepackage[margin=1in]{geometry}
\usepackage[unicode,hidelinks]{hyperref}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\setlength{\emergencystretch}{3em}
\DeclareUnicodeCharacter{2212}{\ensuremath{-}}
\DeclareUnicodeCharacter{00D7}{\ensuremath{\times}}
\DeclareUnicodeCharacter{2265}{\ensuremath{\ge}}
\DeclareUnicodeCharacter{2264}{\ensuremath{\le}}
\DeclareUnicodeCharacter{2260}{\ensuremath{\ne}}
\DeclareUnicodeCharacter{2208}{\ensuremath{\in}}
\DeclareUnicodeCharacter{2209}{\ensuremath{\notin}}
\DeclareUnicodeCharacter{2227}{\ensuremath{\land}}
\DeclareUnicodeCharacter{2228}{\ensuremath{\lor}}
\DeclareUnicodeCharacter{222A}{\ensuremath{\cup}}
\DeclareUnicodeCharacter{2216}{\ensuremath{\setminus}}
\DeclareUnicodeCharacter{03C3}{\ensuremath{\sigma}}
\DeclareUnicodeCharacter{03C0}{\ensuremath{\pi}}
\DeclareUnicodeCharacter{03B5}{\ensuremath{\epsilon}}
\DeclareUnicodeCharacter{03B2}{\ensuremath{\beta}}
\DeclareUnicodeCharacter{2115}{\ensuremath{\mathbb{N}}}
\DeclareUnicodeCharacter{211D}{\ensuremath{\mathbb{R}}}
\DeclareUnicodeCharacter{2080}{\ensuremath{_0}}
\DeclareUnicodeCharacter{2081}{\ensuremath{_1}}
\DeclareUnicodeCharacter{2082}{\ensuremath{_2}}
\DeclareUnicodeCharacter{2083}{\ensuremath{_3}}
\DeclareUnicodeCharacter{2084}{\ensuremath{_4}}
\DeclareUnicodeCharacter{2085}{\ensuremath{_5}}
\DeclareUnicodeCharacter{2086}{\ensuremath{_6}}
\DeclareUnicodeCharacter{2087}{\ensuremath{_7}}
\DeclareUnicodeCharacter{2088}{\ensuremath{_8}}
\DeclareUnicodeCharacter{2089}{\ensuremath{_9}}
\DeclareUnicodeCharacter{2070}{\ensuremath{^0}}
\DeclareUnicodeCharacter{00B9}{\ensuremath{^1}}
\DeclareUnicodeCharacter{00B2}{\ensuremath{^2}}
\DeclareUnicodeCharacter{00B3}{\ensuremath{^3}}
\DeclareUnicodeCharacter{2074}{\ensuremath{^4}}
\DeclareUnicodeCharacter{2075}{\ensuremath{^5}}
\DeclareUnicodeCharacter{2076}{\ensuremath{^6}}
\DeclareUnicodeCharacter{2077}{\ensuremath{^7}}
\DeclareUnicodeCharacter{2078}{\ensuremath{^8}}
\DeclareUnicodeCharacter{2079}{\ensuremath{^9}}
\DeclareUnicodeCharacter{207A}{\ensuremath{^+}}
\DeclareUnicodeCharacter{207B}{\ensuremath{^-}}
\DeclareUnicodeCharacter{02B0}{\ensuremath{^h}}
\DeclareUnicodeCharacter{230A}{\ensuremath{\lfloor}}
\DeclareUnicodeCharacter{230B}{\ensuremath{\rfloor}}
\DeclareUnicodeCharacter{2192}{\ensuremath{\to}}
\DeclareUnicodeCharacter{2205}{\ensuremath{\emptyset}}
\begin{document}
'''
    (ROOT / 'tex/manuscript.tex').write_text(preamble + body.replace('\\section{', '\\section*{').replace('\\subsection{', '\\subsection*{') + '\n\\end{document}\n')
with tempfile.TemporaryDirectory() as td:
    for _ in range(3):
        run = subprocess.run(['pdflatex', '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error', '-output-directory=' + td, str(ROOT / 'tex/manuscript.tex')], cwd=ROOT, capture_output=True, text=True, errors='replace')
        if run.returncode:
            print(run.stdout[-6000:])
            raise SystemExit(run.returncode)
    shutil.copyfile(Path(td) / 'manuscript.pdf', ROOT / 'manuscript.pdf')
    warnings = [line for line in run.stdout.splitlines() if 'Warning' in line or 'Overfull' in line]
version = subprocess.run(['pdflatex', '--version'], check=True, capture_output=True, text=True).stdout.splitlines()[0]
receipt = {'engine': version, 'passes': 3, 'shell_escape': False, 'warnings': warnings, 'artifacts': {}}
for name in ('manuscript.md', 'tex/manuscript.tex', 'manuscript.pdf', 'proofs/four-by-four.md', 'proofs/optimized-order.md', 'proofs/three-by-four.md'):
    data = (ROOT / name).read_bytes()
    receipt['artifacts'][name] = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
(ROOT / 'results/paper_build.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('PDF built; receipt: results/paper_build.json')
