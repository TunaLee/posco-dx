#!/usr/bin/env python3
"""장면 미리보기. 사용: python3 src/preview.py <모듈> <함수> [<함수> ...] --out <폴더>

장면마다 1280x720 PNG 를 <폴더>/<함수>.png 로 찍는다. 비워 둘 구역은 옅은 빗금으로 겹쳐 보여 준다
(--zone left40 | top20 | top25 를 함수 이름 뒤에 :로 붙인다. 예: s9:left40).
"""
import importlib
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import art  # noqa: E402

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ZONES = {"left40": (0, 0, 512, 720), "top20": (0, 0, 1280, 144), "top25": (0, 0, 1280, 180)}


def main():
    args = sys.argv[1:]
    out = Path(args[args.index("--out") + 1])
    args = args[: args.index("--out")]
    out.mkdir(parents=True, exist_ok=True)
    mod = importlib.import_module(args[0])
    for spec in args[1:]:
        name, _, zone = spec.partition(":")
        svg = getattr(mod, name)()
        z = ""
        if zone:
            x, y, w, h = ZONES[zone]
            z = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#F28C28" fill-opacity=".08" stroke="#F28C28" stroke-dasharray="6 6"/>'
        html = (f'<!doctype html><html><body style="margin:0;background:#fff">{art.DEFS}'
                f'<svg viewBox="0 0 1280 720" width="1280" height="720">{svg}{z}</svg></body></html>')
        page = out / f"{name}.html"
        page.write_text(html)
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--window-size=1280,720",
                        f"--screenshot={out / (name + '.png')}", f"file://{page}"],
                       stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=False)
        print(out / f"{name}.png")


if __name__ == "__main__":
    main()
