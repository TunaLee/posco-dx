"""팀 코드 저장소 데이터 — 작은 주문 · 정산 서비스(shop/)와 팀원 4명의 PR 12개.

모든 사람 · 코드 · PR 은 실습용 가상 자료다.
ISSUES 는 PR 에 일부러 심어 둔 문제 목록(채점용 정답)이다. 리뷰할 때는 보지 않는다.
"""

BASE = {
"shop/db.py": '''import sqlite3

DB_PATH = "shop.db"


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def query(sql, params=()):
    with connect() as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]


def execute(sql, params=()):
    with connect() as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid
''',
"shop/orders.py": '''from shop import db
from shop.pricing import calc_total


def create_order(user_id, items, coupon=None):
    total = calc_total(items, coupon)
    order_id = db.execute(
        "INSERT INTO orders (user_id, total, status) VALUES (?, ?, 'paid')",
        (user_id, total),
    )
    for it in items:
        db.execute(
            "INSERT INTO order_items (order_id, sku, qty, price) VALUES (?, ?, ?, ?)",
            (order_id, it["sku"], it["qty"], it["price"]),
        )
    return order_id


def get_order(order_id):
    rows = db.query("SELECT * FROM orders WHERE id = ?", (order_id,))
    return rows[0] if rows else None
''',
"shop/pricing.py": '''from decimal import Decimal, ROUND_DOWN

TAX_RATE = Decimal("0.1")


def subtotal(items):
    return sum(Decimal(str(it["price"])) * it["qty"] for it in items)


def calc_total(items, coupon=None):
    amount = subtotal(items)
    if coupon:
        amount -= Decimal(str(coupon.get("amount", 0)))
    amount = max(amount, Decimal("0"))
    total = amount * (1 + TAX_RATE)
    return int(total.quantize(Decimal("1"), rounding=ROUND_DOWN))
''',
"shop/users.py": '''import hashlib
import logging

from shop import db

log = logging.getLogger(__name__)


def hash_pw(password, salt):
    return hashlib.sha256((salt + password).encode()).hexdigest()


def login(email, password):
    rows = db.query("SELECT * FROM users WHERE email = ?", (email,))
    if not rows:
        return None
    user = rows[0]
    if hash_pw(password, user["salt"]) != user["pw_hash"]:
        log.info("login failed: %s", email)
        return None
    return user


def is_admin(user):
    return user.get("role") == "admin"
''',
"tests/test_pricing.py": '''from shop.pricing import calc_total


def test_total_with_tax():
    assert calc_total([{"price": 10000, "qty": 2}]) == 22000


def test_coupon_amount():
    assert calc_total([{"price": 10000, "qty": 1}], {"amount": 3000}) == 7700
''',
"README.md": '''# shop — 주문 · 정산 서비스

- 주문 생성 · 조회 · 가격 계산 · 로그인
- `pytest` 로 테스트
''',
}

# PR: 바뀐 파일은 변경 후 전체 내용 · 새 파일도 같은 방식
PRS = [
{"id": 101, "author": "김하늘", "title": "주문 검색 API 추가", "created_at": "2026-10-27 09:12",
 "description": "주문 상태 · 사용자 이름으로 주문을 검색하는 함수 추가",
 "files": {"shop/orders.py": BASE["shop/orders.py"] + '''

def search_orders(status, name):
    sql = f"SELECT o.* FROM orders o JOIN users u ON u.id = o.user_id WHERE o.status = '{status}' AND u.name LIKE '%{name}%'"
    return db.query(sql)
'''}},
{"id": 102, "author": "이준호", "title": "쿠폰 정률 할인 지원", "created_at": "2026-10-27 10:40",
 "description": "금액 쿠폰에 더해 % 할인 쿠폰(rate) 지원",
 "files": {"shop/pricing.py": BASE["shop/pricing.py"].replace('''    if coupon:
        amount -= Decimal(str(coupon.get("amount", 0)))''', '''    if coupon:
        amount -= Decimal(str(coupon.get("amount", 0)))
        if "rate" in coupon:
            amount = amount * (1 - Decimal(str(coupon["rate"])) / 100)'''),
   "tests/test_pricing.py": BASE["tests/test_pricing.py"] + '''

def test_coupon_rate():
    assert calc_total([{"price": 10000, "qty": 1}], {"rate": 10}) == 9900
'''}},
{"id": 103, "author": "박서연", "title": "로그인 실패 횟수 제한", "created_at": "2026-10-27 13:05",
 "description": "5회 연속 실패하면 10분 잠금",
 "files": {"shop/users.py": BASE["shop/users.py"].replace('''def login(email, password):
    rows = db.query("SELECT * FROM users WHERE email = ?", (email,))
    if not rows:
        return None
    user = rows[0]
    if hash_pw(password, user["salt"]) != user["pw_hash"]:
        log.info("login failed: %s", email)
        return None
    return user''', '''FAILS = {}
MAX_FAILS = 5


def login(email, password):
    if FAILS.get(email, 0) >= MAX_FAILS:
        log.warning("locked: %s", email)
        return None
    rows = db.query("SELECT * FROM users WHERE email = ?", (email,))
    if not rows:
        return None
    user = rows[0]
    if hash_pw(password, user["salt"]) != user["pw_hash"]:
        FAILS[email] = FAILS.get(email, 0) + 1
        log.info("login failed: %s / %s", email, password)
        return None
    FAILS.pop(email, None)
    return user''')}},
{"id": 104, "author": "최민재", "title": "주문 목록 페이지네이션", "created_at": "2026-10-27 15:30",
 "description": "page · size 로 주문 목록 나눠 보기 (page 는 1부터)",
 "files": {"shop/orders.py": BASE["shop/orders.py"] + '''

def list_orders(user_id, page=1, size=20):
    offset = page * size
    return db.query(
        "SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC LIMIT ? OFFSET ?",
        (user_id, size, offset),
    )
'''}},
{"id": 105, "author": "김하늘", "title": "외부 결제 API 연동", "created_at": "2026-10-28 09:20",
 "description": "결제 대행사 API 로 승인 요청",
 "files": {"shop/payment.py": '''import json
import urllib.request

PG_URL = "https://pg.example.com/v1/approve"
PG_API_KEY = "sk_live_9f8a7c6b5d4e3f2a1b0c"


def approve(order_id, amount):
    body = json.dumps({"order_id": order_id, "amount": amount}).encode()
    req = urllib.request.Request(PG_URL, data=body, headers={"Authorization": f"Bearer {PG_API_KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read())
    except Exception:
        pass
'''}},
{"id": 106, "author": "이준호", "title": "사용자별 주문 통계", "created_at": "2026-10-28 11:10",
 "description": "관리자 화면용 · 사용자마다 주문 수와 합계",
 "files": {"shop/stats.py": '''from shop import db


def order_stats():
    users = db.query("SELECT id, name FROM users")
    out = []
    for u in users:
        rows = db.query("SELECT total FROM orders WHERE user_id = ?", (u["id"],))
        out.append({"user": u["name"], "count": len(rows), "sum": sum(r["total"] for r in rows)})
    return out
'''}},
{"id": 107, "author": "박서연", "title": "README 설치 방법 추가", "created_at": "2026-10-28 14:00",
 "description": "개발 환경 설치 순서 정리",
 "files": {"README.md": BASE["README.md"] + '''
## 설치

```
python -m venv .venv
pip install -r requirements.txt
pytest
```
'''}},
{"id": 108, "author": "최민재", "title": "배송비 계산", "created_at": "2026-10-28 16:45",
 "description": "주문 금액 50,000원 이상이면 배송비 무료 · 아니면 3,000원",
 "files": {"shop/shipping.py": '''FREE_OVER = 50000
FEE = 3000


def shipping_fee(amount):
    if amount > FREE_OVER:
        return 0
    return FEE
'''}},
{"id": 109, "author": "김하늘", "title": "관리자 주문 삭제", "created_at": "2026-10-29 10:05",
 "description": "잘못 들어간 주문을 관리자가 지울 수 있게",
 "files": {"shop/orders.py": BASE["shop/orders.py"] + '''

def delete_order(user, order_id):
    db.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
    db.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    return True
'''}},
{"id": 110, "author": "이준호", "title": "환불 처리", "created_at": "2026-10-29 13:30",
 "description": "주문 일부 · 전체 환불",
 "files": {"shop/refund.py": '''from shop import db


def refund(order_id, amount):
    order = db.query("SELECT * FROM orders WHERE id = ?", (order_id,))[0]
    db.execute("UPDATE orders SET total = total - ?, status = 'refunded' WHERE id = ?", (amount, order_id))
    return {"order_id": order_id, "refunded": amount, "remain": order["total"] - amount}
'''}},
{"id": 111, "author": "박서연", "title": "가격 조회 캐시", "created_at": "2026-10-30 09:40",
 "description": "같은 상품 가격을 반복 조회하지 않도록 캐시",
 "files": {"shop/catalog.py": '''from shop import db


def get_price(sku, cache={}):
    if sku not in cache:
        rows = db.query("SELECT price FROM products WHERE sku = ?", (sku,))
        cache[sku] = rows[0]["price"]
    return cache[sku]
'''}},
{"id": 112, "author": "최민재", "title": "로그 메시지 정리", "created_at": "2026-10-30 11:15",
 "description": "로그인 실패 로그를 경고 수준으로",
 "files": {"shop/users.py": BASE["shop/users.py"].replace('log.info("login failed: %s", email)', 'log.warning("login failed: %s", email)')}},
]

# 심어 둔 문제 (채점용 정답) · kind: 보안 · 버그 · 성능 · 테스트
ISSUES = [
    {"pr": 101, "id": "101-a", "kind": "보안", "file": "shop/orders.py", "key": "SQL 인젝션", "desc": "f-string 으로 status · name 을 SQL 에 바로 넣음 · 파라미터 바인딩 필요"},
    {"pr": 102, "id": "102-a", "kind": "버그", "file": "shop/pricing.py", "key": "할인율 범위 검증 없음", "desc": "rate 가 100 초과 · 음수여도 그대로 계산"},
    {"pr": 103, "id": "103-a", "kind": "보안", "file": "shop/users.py", "key": "비밀번호 로그 기록", "desc": "실패 로그에 password 를 그대로 남김"},
    {"pr": 103, "id": "103-b", "kind": "버그", "file": "shop/users.py", "key": "잠금 해제 시간 없음", "desc": "설명은 10분 잠금인데 시간 기록 · 해제가 없어 영구 잠금 · 프로세스 메모리라 서버 재시작 시 초기화"},
    {"pr": 104, "id": "104-a", "kind": "버그", "file": "shop/orders.py", "key": "오프셋 계산 오류", "desc": "page 가 1부터인데 offset = page * size → 첫 페이지를 건너뜀 · (page - 1) * size"},
    {"pr": 105, "id": "105-a", "kind": "보안", "file": "shop/payment.py", "key": "API 키 하드코딩", "desc": "운영 키(sk_live_…)가 코드에 그대로 · 환경 변수 · 비밀 저장소로"},
    {"pr": 105, "id": "105-b", "kind": "버그", "file": "shop/payment.py", "key": "예외 무시", "desc": "except Exception: pass · 결제 실패가 None 으로 조용히 넘어감"},
    {"pr": 106, "id": "106-a", "kind": "성능", "file": "shop/stats.py", "key": "N+1 쿼리", "desc": "사용자마다 쿼리 한 번 · GROUP BY 한 번으로"},
    {"pr": 108, "id": "108-a", "kind": "버그", "file": "shop/shipping.py", "key": "경계값 오류", "desc": "50,000원 이상 무료인데 > 비교 · 정확히 50,000원이면 배송비가 붙음"},
    {"pr": 108, "id": "108-b", "kind": "테스트", "file": "shop/shipping.py", "key": "테스트 없음", "desc": "경계값(49,999 · 50,000) 테스트가 없음"},
    {"pr": 109, "id": "109-a", "kind": "보안", "file": "shop/orders.py", "key": "권한 검사 없음", "desc": "user 를 받지만 is_admin 확인 없이 삭제"},
    {"pr": 110, "id": "110-a", "kind": "버그", "file": "shop/refund.py", "key": "초과 환불", "desc": "환불액이 결제액보다 커도 그대로 · 음수 total 가능 · 이미 환불된 주문도 다시 환불"},
    {"pr": 110, "id": "110-b", "kind": "테스트", "file": "shop/refund.py", "key": "테스트 없음", "desc": "부분 · 전체 · 초과 환불 테스트 없음"},
    {"pr": 111, "id": "111-a", "kind": "버그", "file": "shop/catalog.py", "key": "가변 기본 인자 캐시", "desc": "cache={} 기본 인자 · 가격이 바뀌어도 갱신 안 됨 · 무효화 수단 없음"},
]
CLEAN = [107, 112]   # 문제 없는 PR · 지어낸 지적이 나오면 오탐
