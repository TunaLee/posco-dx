# 실습 전체 설정 — 모델 이름과 트랙은 여기서만 바꾼다.
# ※ 모든 회사·인물·데이터는 실습용 가상 자료입니다.

# 메인 Agent 모델 (답변 작성, Supervisor)
MODEL = "claude-sonnet-5-5"

# 채점(judge)·분류처럼 싼 작업에 쓰는 모델
JUDGE_MODEL = "claude-haiku-5-5"

# 기본 트랙: "pangyo" (문의 대응 라우팅) | "pohang" (사양서 추출·견적)
# 실행할 때 --track 으로 덮어쓸 수 있다.
TRACK = "pangyo"

# 한 번 실행에 쓸 수 있는 최대 비용(USD). 넘으면 SDK 가 멈춘다.
MAX_BUDGET_USD = 0.50

# 반복 실행 기본 횟수 (lab1, lab5)
DEFAULT_N = 5
