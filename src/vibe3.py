"""바이브코딩 온라인 강의 3장 — 하네스 엔지니어링 & 내 업무 에이전트 (180분).

차시마다 모듈 하나(v3_c1 … v3_c8)가 slides() 를 돌려준다. 공통 도구는 v3kit.
공통 업무: 회의록 → 할 일 정리 → 공유 초안 (labs/meeting_agent)
"""
import importlib
import os

import v3kit
from v3kit import agenda, cover

CHAPTERS = [f"v3_c{i}" for i in range(1, 9)]
# V3_ONLY=v3_c1,v3_c2 → 그 차시만 (병렬 작업 확인용) · build.py 는 V3_OUT 으로 출력 경로를 바꾼다
ONLY = [x for x in os.environ.get("V3_ONLY", "").split(",") if x]


def _mods():
    for m in (ONLY or CHAPTERS):
        try:
            yield importlib.import_module(m)
        except ModuleNotFoundError as e:
            if e.name != m:
                raise


CSS = v3kit.CSS + "".join(getattr(m, "CSS", "") for m in _mods())


def slides():
    out = [cover(), agenda()]
    for mod in _mods():
        out += mod.slides()
    return out
