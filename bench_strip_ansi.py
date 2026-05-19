import re
import timeit
import deal_analyzer

ANSI_ESCAPE = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')

def strip_ansi_orig(text: str) -> str:
    return ANSI_ESCAPE.sub('', text)

def strip_ansi_fast(text: str) -> str:
    if '\x1b' in text or not text.isascii():
        return ANSI_ESCAPE.sub('', text)
    return text

data = [
    "Hello world!",
    "This is a normal string",
    "String with some numbers 12345",
    "\033[91mThis is red\033[0m",
    "Another \x1b[1mstring\x1b[0m with \x90 ANSI"
] * 100

print("Baseline:", timeit.timeit("for d in data: strip_ansi_orig(d)", globals=globals(), number=1000))
print("Fast:", timeit.timeit("for d in data: strip_ansi_fast(d)", globals=globals(), number=1000))
