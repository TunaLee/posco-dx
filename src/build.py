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


if __name__ == "__main__":
    build()
