#!/usr/bin/env python3
"""하네스 강의를 template.html 에 붙여 docs/<판본>/index.html 을 만든다.

사용: python3 src/build.py           → 판교 · 포항 둘 다
      python3 src/build.py pangyo    → docs/pangyo/index.html
"""
import sys
from pathlib import Path

import art
import deck
import deck_gas
import explain
import harness
import intro

ROOT = Path(__file__).resolve().parent.parent
TITLE = {"pangyo": "하네스 엔지니어링 · 판교", "pohang": "하네스 엔지니어링 · 포항"}


def build(variant):
    parts = [art.DEFS] + harness.slides(variant)
    tpl = (ROOT / "src" / "template.html").read_text()
    css = intro.CSS + explain.CSS + deck.CSS + deck_gas.CSS + harness.CSS
    tpl = tpl.replace("</style>", css + "</style>", 1)
    html = tpl.replace("{{DECK_TITLE}}", TITLE[variant]).replace("{{SLIDES}}", "\n\n".join(parts))
    html = html.replace('src="assets/', 'src="../assets/')
    out = ROOT / "docs" / variant / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print(out, len(parts) - 1, "장")


if __name__ == "__main__":
    for v in (sys.argv[1:] or ["pangyo", "pohang"]):
        build(v)
