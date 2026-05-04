import timeit

setup = """
import re
raw = '1000 - $1,299'
RE_PRICE_RANGE = re.compile(r"(to|[-–])\s*\$?[\d,]+")
RE_DIGITS = re.compile(r"[^\d.]")
"""

test_no_compile = """
r1 = re.sub(r"(to|[-–])\s*\$?[\d,]+", "", str(raw or ""))
r2 = re.sub(r"[^\d.]", "", "1299.99")
"""

test_compile = """
r1 = RE_PRICE_RANGE.sub("", str(raw or ""))
r2 = RE_DIGITS.sub("", "1299.99")
"""

no_compile_time = timeit.timeit(test_no_compile, setup=setup, number=100000)
compile_time = timeit.timeit(test_compile, setup=setup, number=100000)

print(f"No compile: {no_compile_time:.4f}s")
print(f"Pre-compile: {compile_time:.4f}s")
print(f"Speedup: {no_compile_time / compile_time:.2f}x")
