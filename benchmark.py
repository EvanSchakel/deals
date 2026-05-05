import timeit

setup = r"""
import re

def parse_price(raw: str):
    raw = re.sub(r"(to|[-–])\s*\$?[\d,]+", "", str(raw or ""))
    for token in raw.split():
        digits = re.sub(r"[^\d.]", "", token)
        try:
            value = float(digits)
            if 50 < value < 30_000:
                return value
        except ValueError:
            continue
    return None

data = [
    "$1,299.99",
    "Price is $500",
    "Asking 1500 OBO",
    "New Macbook 2500 - $3000",
    "Not a price, just text " * 10
] * 100
"""

stmt = r"""
for text in data:
    parse_price(text)
"""

print("Baseline:", timeit.timeit(stmt, setup, number=100))

setup_optimized = r"""
import re

_STRIP_RE = re.compile(r"(to|[-–])\s*\$?[\d,]+")
_DIGITS_RE = re.compile(r"[^\d.]")

def parse_price_opt(raw: str):
    raw = _STRIP_RE.sub("", str(raw or ""))
    for token in raw.split():
        digits = _DIGITS_RE.sub("", token)
        try:
            value = float(digits)
            if 50 < value < 30_000:
                return value
        except ValueError:
            continue
    return None

data = [
    "$1,299.99",
    "Price is $500",
    "Asking 1500 OBO",
    "New Macbook 2500 - $3000",
    "Not a price, just text " * 10
] * 100
"""

stmt_optimized = r"""
for text in data:
    parse_price_opt(text)
"""

print("Optimized:", timeit.timeit(stmt_optimized, setup_optimized, number=100))
