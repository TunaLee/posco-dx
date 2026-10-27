"""리뷰용 저장소 shop.git 만들기 — main + 팀원 PR 브랜치 12개 (실제 커밋 · 작성자 · 시각).

server.py 가 처음 켤 때 한 번 부른다. 다시 만들려면 repos/shop.git 을 지우고 서버를 켠다.
"""
import json
import os
import subprocess
import tempfile
from pathlib import Path

from shop_data import BASE, PRS

EMAIL = {"김하늘": "haneul", "이준호": "junho", "박서연": "seoyeon", "최민재": "minjae", "팀장": "lead"}


def git(cwd, *args, who="팀장", when="2026-10-26 18:00"):
    env = {**os.environ, "GIT_AUTHOR_NAME": who, "GIT_COMMITTER_NAME": who,
           "GIT_AUTHOR_EMAIL": f"{EMAIL.get(who, 'dev')}@team.example", "GIT_COMMITTER_EMAIL": f"{EMAIL.get(who, 'dev')}@team.example",
           "GIT_AUTHOR_DATE": when + " +0900", "GIT_COMMITTER_DATE": when + " +0900"}
    subprocess.run(["git", *args], cwd=cwd, env=env, check=True, capture_output=True)


def write(root, files):
    for path, text in files.items():
        f = Path(root) / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")


def make(repos):
    bare = Path(repos) / "shop.git"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(bare)], check=True, capture_output=True)
    meta = {"prs": {}, "comments": {}, "approvals": {}, "merged": {}}
    with tempfile.TemporaryDirectory() as w:
        git(w, "init", "-b", "main")
        write(w, BASE)
        git(w, "add", "-A")
        git(w, "commit", "-m", "shop 첫 커밋 · 주문 · 가격 · 로그인")
        git(w, "remote", "add", "origin", str(bare))
        git(w, "push", "origin", "main")
        for p in PRS:
            br = f"pr-{p['id']}"
            git(w, "checkout", "-q", "-b", br, "main")
            write(w, p["files"])
            git(w, "add", "-A")
            git(w, "commit", "-m", f"{p['title']}\n\n{p['description']}", who=p["author"], when=p["created_at"])
            git(w, "push", "origin", br)
            git(w, "checkout", "-q", "main")
            meta["prs"][br] = {"id": p["id"], "title": p["title"], "author": p["author"],
                               "created_at": p["created_at"], "description": p["description"]}
    (Path(repos) / "shop.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
