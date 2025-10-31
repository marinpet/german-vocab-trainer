from __future__ import annotations
from datetime import datetime, date, timezone

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

def date_today() -> date:
    return utcnow().date()