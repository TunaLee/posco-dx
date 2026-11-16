#!/usr/bin/env python3
"""하네스 강의를 template.html 에 붙여 docs/index.html 을 만든다.

사용: python3 src/build.py
"""
import os
import sys
from pathlib import Path

import art
import deck
import deck_gas
import explain
import hx
import intro
import stats_hx

ROOT = Path(__file__).resolve().parent.parent


SKIP = {"runs", "logs", "__pycache__", ".venv", "out", ".DS_Store", "old"}


def make_downloads():
    """실습 장표에서 가리킨 자료를 docs/dl/ 에 zip · 파일로 (GitHub 없이 덱 폴더만으로)."""
    import shutil
    import unicodedata
    import zipfile
    import subprocess
    labs, dl = ROOT / "labs", ROOT / "docs" / "dl"
    tracked = set(subprocess.run(["git", "ls-files", "-z", "labs"], cwd=ROOT, capture_output=True, text=True).stdout.split("\0"))
    tracked = {unicodedata.normalize("NFC", x) for x in tracked}
    if dl.exists():
        shutil.rmtree(dl)
    dl.mkdir(parents=True)

    def add(z, folder):
        for f in sorted(folder.rglob("*")):
            rel = f.relative_to(labs)
            if f.is_file() and not (set(rel.parts) & SKIP) and f.suffix not in (".db", ".pyc") and unicodedata.normalize("NFC", f"labs/{rel}") in tracked:
                z.write(f, Path("labs") / rel)
    for name in sorted(hx.LAB_FILES):
        if name == "labs":
            with zipfile.ZipFile(dl / "labs.zip", "w", zipfile.ZIP_DEFLATED) as z:
                for top in sorted(labs.iterdir()):
                    if top.is_dir():
                        add(z, top)
                    elif top.is_file() and f"labs/{top.name}" in tracked:
                        z.write(top, Path("labs") / top.name)
        elif "." in name:
            shutil.copy(labs / name, dl / name)
        else:
            with zipfile.ZipFile(dl / f"{name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
                for extra in ("common", "data", name):      # 공통 모듈 · 데이터 함께
                    if (labs / extra).is_dir():
                        add(z, labs / extra)
                for top in ("README.md", "requirements.txt"):
                    if (labs / top).exists():
                        z.write(labs / top, Path("labs") / top)
    total = sum(f.stat().st_size for f in dl.iterdir())
    print("dl/", len(list(dl.iterdir())), "개", f"{total / 1e6:.1f}MB")


def build():
    parts = [art.DEFS] + hx.slides()
    tpl = (ROOT / "src" / "template.html").read_text()
    css = intro.CSS + explain.CSS + deck.CSS + deck_gas.CSS + hx.CSS + stats_hx.CSS + hx.mcp_fig.CSS + hx.viz2.CSS
    tpl = tpl.replace("</style>", css + "</style>", 1)
    html = tpl.replace("{{DECK_TITLE}}", "하네스 엔지니어링 · 평가와 검증").replace("{{SLIDES}}", "\n\n".join(parts))
    out = ROOT / "docs" / "index.html"
    out.write_text(html)
    print(out, len(parts) - 1, "장")
    make_downloads()


def build_vibe3():
    """바이브코딩 온라인 강의 3장 덱 → docs/vibe3.html"""
    import vibe3
    parts = [art.DEFS] + vibe3.slides()
    tpl = (ROOT / "src" / "template.html").read_text()
    css = intro.CSS + explain.CSS + deck.CSS + deck_gas.CSS + hx.CSS + stats_hx.CSS + hx.mcp_fig.CSS + hx.viz2.CSS + vibe3.CSS
    tpl = tpl.replace("</style>", css + "</style>", 1)
    html = tpl.replace("{{DECK_TITLE}}", "하네스 엔지니어링 · 내 업무 에이전트").replace("{{SLIDES}}", "\n\n".join(parts))
    out = Path(os.environ["V3_OUT"]) if os.environ.get("V3_OUT") else ROOT / "docs" / "vibe3.html"
    out.write_text(html)
    print(out, len(parts) - 1, "장")
    if os.environ.get("V3_OUT") or os.environ.get("V3_ONLY"):
        return
    # 단원별 파일 — docs/vibe3-N.html (표지 + 그 차시 장)
    import importlib
    import v3kit
    for i, (c, t, _) in enumerate(v3kit.AGENDA, 1):
        mod = importlib.import_module(f"v3_c{i}")
        cov = v3kit.cover().replace("바이브코딩 · 3", f"바이브코딩 · {c}").replace("하네스 엔지니어링<br/>· 내 업무 에이전트", t)
        p = [art.DEFS, cov] + mod.slides()
        o = ROOT / "docs" / f"vibe3-{i}.html"
        o.write_text(tpl.replace("{{DECK_TITLE}}", f"{c} {t}").replace("{{SLIDES}}", "\n\n".join(p)))
        print(o.name, len(p) - 1, "장")


def build_vibe1():
    """바이브코딩 온라인 강의 1부 — 단원마다 한 파일 → docs/vibe1-N.html (V1_ONLY=3,6 으로 일부만)."""
    import importlib
    import v1kit
    import v3kit
    only = [x for x in os.environ.get("V1_ONLY", "").split(",") if x]
    base = (ROOT / "src" / "template.html").read_text()
    css0 = intro.CSS + explain.CSS + deck.CSS + deck_gas.CSS + hx.CSS + stats_hx.CSS + hx.mcp_fig.CSS + hx.viz2.CSS + v3kit.CSS + v1kit.CSS
    for i, (u, title, _, _) in enumerate(v1kit.UNITS, 1):
        if only and str(i) not in only:
            continue
        try:
            mod = importlib.import_module(f"v1_u{i}")
        except ModuleNotFoundError as e:
            if e.name != f"v1_u{i}":
                raise
            continue
        parts = [art.DEFS, v1kit.cover(u), v1kit.roadmap(u)] + mod.slides() + [v1kit.nextup(u)]
        tpl = base.replace("</style>", css0 + getattr(mod, "CSS", "") + "</style>", 1)
        out = ROOT / "docs" / v1kit.file_of(u)
        out.write_text(tpl.replace("{{DECK_TITLE}}", f"{u} {title}").replace("{{SLIDES}}", "\n\n".join(parts)))
        print(out.name, len(parts) - 1, "장")


if __name__ == "__main__":
    if sys.argv[1:] == ["vibe3"]:
        build_vibe3()
    elif sys.argv[1:] == ["vibe1"]:
        build_vibe1()
    else:
        build()
        build_vibe3()
        build_vibe1()
