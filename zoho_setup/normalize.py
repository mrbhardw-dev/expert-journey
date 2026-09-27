"""Cleaning rules shared by validation and import. Mirrors deluge/normalize_registration.dg."""
import re
from datetime import datetime
from zoneinfo import ZoneInfo

REG_PATTERN = re.compile(r"^([0-9]{2,3})([A-Z]{1,2})([0-9]{1,6})$")
DUBLIN = ZoneInfo("Europe/Dublin")
EXAMPLE_MARKER = "Example row - delete before import"


def registration(value):
    """'191d12345' / '191 D 12345' -> '191-D-12345'. None if not a modern Irish plate."""
    raw = re.sub(r"[^A-Z0-9]", "", (value or "").upper())
    m = REG_PATTERN.match(raw)
    return "-".join(m.groups()) if m else None


def mobile(value):
    """Irish numbers to +353 format. '087 123 4567' -> '+353871234567'. None if invalid."""
    digits = re.sub(r"[^0-9+]", "", value or "")
    if digits.startswith("00"):
        digits = "+" + digits[2:]
    elif digits.startswith("0"):
        digits = "+353" + digits[1:]
    elif digits.startswith("353"):
        digits = "+" + digits
    return digits if re.fullmatch(r"\+[0-9]{9,15}", digits) else None


def boolean(value):
    return (value or "").strip().lower() in ("true", "yes", "y", "1", "x")


def date(value):
    """'2026-03-14' or '14/03/2026' -> '2026-03-14'. None if blank; ValueError if unreadable."""
    value = (value or "").strip()
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    raise ValueError(f"unreadable date {value!r} (use YYYY-MM-DD)")


def local_datetime(value):
    """'2026-03-14 09:00' (Irish local time) -> ISO 8601 with offset, as CRM expects."""
    value = (value or "").strip()
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(value, fmt).replace(tzinfo=DUBLIN)
            return dt.isoformat(timespec="seconds")
        except ValueError:
            pass
    raise ValueError(f"unreadable date/time {value!r} (use YYYY-MM-DD HH:MM)")


def is_example(row):
    return any(EXAMPLE_MARKER in (v or "") for v in row.values())


def api_name_from_label(label):
    """How Zoho CRM derives a custom field's API name from its label."""
    cleaned = re.sub(r"[^A-Za-z0-9 _]", "", label).strip()
    return re.sub(r"\s+", "_", cleaned)
