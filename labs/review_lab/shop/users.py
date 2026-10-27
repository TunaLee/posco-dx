import hashlib
import logging

from shop import db

log = logging.getLogger(__name__)


def hash_pw(password, salt):
    return hashlib.sha256((salt + password).encode()).hexdigest()


FAILS = {}
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
    return user


def is_admin(user):
    return user.get("role") == "admin"
