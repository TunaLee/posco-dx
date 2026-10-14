#!/usr/bin/env python3
"""하네스 강의를 template.html 에 붙여 docs/index.html 을 만든다.

사용: python3 src/build.py
"""
from pathlib import Path

import art
import deck
import deck_gas
import explain
import hx
import intro
import stats_hx

ROOT = Path(__file__).resolve().parent.parent


def build():
    parts = [art.DEFS] + hx.slides()
    tpl = (ROOT / "src" / "template.html").read_text()
    css = intro.CSS + explain.CSS + deck.CSS + deck_gas.CSS + hx.CSS + stats_hx.CSS
    tpl = tpl.replace("</style>", css + "</style>", 1)
    html = tpl.replace("{{DECK_TITLE}}", "하네스 엔지니어링 · 평가와 검증").replace("{{SLIDES}}", "\n\n".join(parts))
    out = ROOT / "docs" / "index.html"
    out.write_text(html)
    print(out, len(parts) - 1, "장")


if __name__ == "__main__":
    build()
