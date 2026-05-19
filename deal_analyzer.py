"""
deal_analyzer.py
────────────────────────────────────────────────────────────────
A command-line tool for scoring used/refurbished tech listings.

Paste a listing title and price, get back a 1–10 deal score,
scam signal flags, and a plain-English verdict.

Usage:
    python deal_analyzer.py                    # interactive mode
    python deal_analyzer.py --title "..." --price 1200  # one-shot mode
    python deal_analyzer.py --list-products    # show tracked products

No external dependencies — pure Python stdlib.
────────────────────────────────────────────────────────────────
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from typing import Optional

from products import PRODUCTS, SCAM_HIGH, SCAM_MEDIUM, SCAM_FLAGS


# ── Terminal colors (works on macOS/Linux; degrades gracefully on Windows) ────

class Color:
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    GREEN  = "\033[92m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RESET  = "\033[0m"

def colorize(text: str, *codes: str) -> str:
    """Wrap text in ANSI color codes, if stdout is a real terminal."""
    if not sys.stdout.isatty():
        return text
    return "".join(codes) + text + Color.RESET

# Pattern to match most ANSI escape sequences
ANSI_ESCAPE = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')

def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from a string."""
    return ANSI_ESCAPE.sub('', text)


# ── Core data types ───────────────────────────────────────────────────────────

# Precompute translation table for sanitizing control characters and newlines
# This is faster than using multiple str.replace() and re.sub() calls.
_SANITIZE_TRANS = str.maketrans(
    {
        '\r': ' ',
        '\n': ' ',
        **{chr(i): None for i in range(0x20) if i not in (9, 10, 13)}, # tab is 9, newline is 10, carriage return is 13
        chr(0x7f): None
    }
)

def sanitize_text(text: str) -> str:
    """Remove ANSI escape sequences and control characters from untrusted input."""
    if not text:
        return text
    # Prevent DoS by capping length
    text = text[:10000]
    # Remove ANSI escape sequences
    text = ANSI_ESCAPE.sub('', text)
    # Replace newlines with spaces and remove control chars (except tab)
    return text.translate(_SANITIZE_TRANS)

@dataclass
class Listing:
    title:       str
    price:       float
    description: str = ""
    condition:   str = ""
    source:      str = ""

    def __post_init__(self):
        self.title = sanitize_text(self.title)
        self.description = sanitize_text(self.description)
        self.condition = sanitize_text(self.condition)
        self.source = sanitize_text(self.source)

@dataclass
class AnalysisResult:
    listing:        Listing
    matched_product: Optional[str]       # e.g. "MacBook Air 13\" M5 24GB"
    retail_price:   Optional[float]
    score:          int                  # 1–10
    verdict:        str                  # human-readable
    scam_level:     str                  # "none" | "low" | "medium" | "high"
    scam_signals:   list[str] = field(default_factory=list)
    warnings:       list[str] = field(default_factory=list)
    notes:          list[str] = field(default_factory=list)


# ── Price parsing ─────────────────────────────────────────────────────────────

# Strips trailing ranges like "to $1,500" or "- 1500" to only capture the first price.
_PRICE_STRIP_RE = re.compile(r"(to|[-–])\s*\$?[\d,]+")
# Matches any character that is NOT a digit or a period. Used to clean price strings.
_PRICE_DIGITS_RE = re.compile(r"[^\d.]")
# Extracts numbers followed by "gb" (ignoring whitespace) to find RAM sizes.
_RAM_RE = re.compile(r"(\d+)\s*gb")
# Matches specific storage sizes (512, 1tb, 2tb) to verify storage requirements.
_STORAGE_RE = re.compile(r"512|1\s*tb|2\s*tb")

def parse_price(raw: str) -> Optional[float]:
    """
    Extract the first plausible price from a string like '$1,299' or '1299.99'.
    Returns None if nothing looks like a price.
    """
    # Strip everything before the first dollar sign
    raw = _PRICE_STRIP_RE.sub("", str(raw or ""))
    for token in raw.split():
        digits = _PRICE_DIGITS_RE.sub("", token)
        # Prevent DoS from excessively long string to float conversions
        if len(digits) > 30:
            continue
        try:
            value = float(digits)
            if 50 < value < 30_000:
                return value
        except ValueError:
            continue
    return None


# ── Scam detection ────────────────────────────────────────────────────────────

def _check_phrases(text: str, phrases: list[str], label: str) -> list[str]:
    return [f"[{label}] {phrase}" for phrase in phrases if phrase in text]

def check_scam(text: str) -> tuple[str, list[str]]:
    """
    Scan listing text for scam / red-flag phrases.
    Returns (level, [matched_signals]).
    Level is one of: "none", "low", "medium", "high"
    """
    lower = text.lower()
    signals: list[str] = []

    signals.extend(_check_phrases(lower, SCAM_HIGH, "HIGH"))
    signals.extend(_check_phrases(lower, SCAM_MEDIUM, "MEDIUM"))
    signals.extend(_check_phrases(lower, SCAM_FLAGS, "FLAG"))

    if any("[HIGH]" in s for s in signals):
        return "high", signals
    if any("[MEDIUM]" in s for s in signals):
        return "medium", signals
    if signals:
        return "low", signals
    return "none", signals


# ── Product matching ──────────────────────────────────────────────────────────

# Precompute the flattened list of tags, sorted by length descending
# This allows match_product to be O(1) in the number of products/tags for the first match
# instead of checking all tags to find the longest one.
_ALL_TAGS = []
for _product_name, _product in PRODUCTS.items():
    for _tag in _product.get("tags", []):
        _ALL_TAGS.append((_tag, _product_name))
_ALL_TAGS.sort(key=lambda x: len(x[0]), reverse=True)

def match_product(title: str, description: str = "") -> Optional[str]:
    """
    Find the best matching product name from the PRODUCTS database.
    Checks tags against the combined title + description.
    Returns the product name with the longest matching tag, or None.
    """
    text = (title + " " + description).lower()
    # Expand common abbreviations
    text = text.replace("mbp", "macbook pro").replace("mba", "macbook air")

    # Since _ALL_TAGS is sorted by length descending, the first match is guaranteed
    # to be the longest possible matching tag.
    for tag, product_name in _ALL_TAGS:
        if tag in text:
            return product_name

    return None


# ── Scoring ───────────────────────────────────────────────────────────────────

def score_listing(listing: Listing) -> AnalysisResult:
    """
    Core scoring logic.

    Algorithm:
      1. Match the listing against the product database.
      2. Extract price and compare to retail thresholds.
      3. Apply scam modifiers.
      4. Apply condition modifiers (+/- 1).
      5. Clamp to 1–10.
    """
    full_text = f"{listing.title} {listing.description}"
    scam_level, scam_signals = check_scam(full_text)
    product_name = match_product(listing.title, listing.description)
    warnings: list[str] = []
    notes: list[str] = []

    # ── No product match ───────────────────────────────────────────────────────
    if not product_name:
        base_score = 3 if scam_level == "none" else 1
        verdict = (
            "No matching product found in the database. "
            "Add it to products.py to get a proper score."
        )
        return AnalysisResult(
            listing=listing,
            matched_product=None,
            retail_price=None,
            score=base_score,
            verdict=verdict,
            scam_level=scam_level,
            scam_signals=scam_signals,
            warnings=["Product not in database — score is rough estimate only."],
            notes=notes,
        )

    product = PRODUCTS[product_name]
    retail   = product["retail"]
    ratio    = listing.price / retail

    # ── Base price score ───────────────────────────────────────────────────────
    if ratio <= product.get("great", 0.78):
        base_score = 9
        verdict    = "Great deal — well below market."
    elif product.get("insane_only") and ratio <= 1.01:
        base_score = 3
        verdict    = "Near retail — not much savings."
    elif ratio <= product.get("good", 0.84):
        base_score = 7
        verdict    = "Good deal — meaningfully below retail."
    elif ratio <= 0.94:
        base_score = 5
        verdict    = "Decent — moderate discount."
    elif ratio <= 1.01:
        base_score = 3
        verdict    = "Near retail — not much savings."
    else:
        base_score = 1
        verdict    = "Above retail — don't buy."

    notes.append(
        f"Matched: {product_name}  |  "
        f"${listing.price:.0f} vs ${retail} retail  |  "
        f"{(1 - ratio) * 100:.1f}% off"
    )

    # ── RAM gate ───────────────────────────────────────────────────────────────
    ram_gate = product.get("ram_gate")
    if ram_gate:
        # Limit RAM string length to prevent integer conversion DoS
        rams = [int(r) for r in _RAM_RE.findall(full_text.lower())
                if len(r) <= 10 and int(r) >= ram_gate]
        if not rams:
            warnings.append(
                f"RAM not confirmed in listing — this product requires {ram_gate}GB+. "
                "Verify before buying."
            )
            base_score = max(1, base_score - 1)

    # ── Storage gate ───────────────────────────────────────────────────────────
    if product.get("require_512") and not _STORAGE_RE.search(full_text.lower()):
        warnings.append(
            "This product filter requires 512GB+ storage. "
            "Listing does not confirm it — may be the base 256GB config."
        )
        base_score = max(1, base_score - 2)

    # ── Condition modifiers ────────────────────────────────────────────────────
    cond = listing.condition.lower()
    if any(c in cond for c in ["new", "sealed", "open box", "open-box"]):
        base_score = min(10, base_score + 1)
        notes.append("Condition bonus: new/open-box (+1)")
    elif any(c in cond for c in ["fair", "acceptable", "poor"]):
        base_score = max(1, base_score - 2)
        notes.append("Condition penalty: fair/acceptable (-2)")

    # ── Scam modifiers ─────────────────────────────────────────────────────────
    if scam_level == "high":
        base_score = min(base_score, 2)
        verdict    = "⚠️  SCAM WARNING — do not proceed."
        warnings.append("HIGH scam risk detected. Do not pay outside a buyer-protected platform.")
    elif scam_level == "medium":
        base_score = max(1, base_score - 2)
        warnings.append("Moderate scam signals — verify seller carefully.")
    elif scam_level == "low":
        base_score = max(1, base_score - 1)
        warnings.append("Minor flags present — proceed with caution.")

    # ── Clamp ──────────────────────────────────────────────────────────────────
    final_score = max(1, min(10, base_score))

    return AnalysisResult(
        listing=listing,
        matched_product=product_name,
        retail_price=retail,
        score=final_score,
        verdict=verdict,
        scam_level=scam_level,
        scam_signals=scam_signals,
        warnings=warnings,
        notes=notes,
    )


# ── Output formatting ─────────────────────────────────────────────────────────

def stars(n: int, total: int = 10) -> str:
    n = max(0, min(total, n))
    return "★" * n + "☆" * (total - n)

SCORE_COLORS = {
    range(9, 11): Color.GREEN,
    range(7,  9): Color.GREEN,
    range(5,  7): Color.YELLOW,
    range(3,  5): Color.YELLOW,
    range(1,  3): Color.RED,
}

def score_color(n: int) -> str:
    for r, color in SCORE_COLORS.items():
        if n in r:
            return color
    return Color.RESET

SCAM_COLORS = {
    "none":   Color.GREEN,
    "low":    Color.YELLOW,
    "medium": Color.YELLOW,
    "high":   Color.RED,
}

def print_result(result: AnalysisResult) -> None:
    divider = "─" * 60
    print(f"\n{colorize(divider, Color.DIM)}")

    # Header
    title_display = result.listing.title[:58]
    print(f"  {colorize(title_display, Color.BOLD)}")

    price_str = f"${result.listing.price:,.2f}"
    if result.retail_price:
        retail_str = f"  (retail: ${result.retail_price:,.0f})"
    else:
        retail_str = ""
    print(f"  Listed: {colorize(price_str, Color.CYAN)}{retail_str}")

    if result.matched_product:
        print(f"  Matched: {result.matched_product}")
    else:
        print(f"  {colorize('No product match', Color.DIM)}")

    # Score bar
    color = score_color(result.score)
    score_display = f"{stars(result.score)}  {result.score}/10"
    print(f"\n  {colorize(score_display, color, Color.BOLD)}")
    print(f"  {colorize(result.verdict, color)}")

    # Scam
    scam_color = SCAM_COLORS.get(result.scam_level, Color.RESET)
    print(f"  Scam risk: {colorize(result.scam_level.upper(), scam_color)}")

    # Scam signals
    if result.scam_signals:
        print(f"\n  {colorize('⚠️  Signals detected:', Color.YELLOW)}")
        for sig in result.scam_signals:
            print(f"    • {sig}")

    # Warnings
    if result.warnings:
        print(f"\n  {colorize('Warnings:', Color.YELLOW)}")
        for w in result.warnings:
            print(f"    ⚡ {w}")

    # Notes
    if result.notes:
        print(f"\n  {colorize('Notes:', Color.DIM)}")
        for note in result.notes:
            print(f"    {colorize('→ ' + note, Color.DIM)}")

    print(f"{colorize(divider, Color.DIM)}\n")


def print_product_list() -> None:
    """Print all products in the database with their thresholds."""
    print(f"\n{colorize('═' * 65, Color.BOLD)}")
    print(f"  {colorize('Tracked Products', Color.BOLD)}")
    print(colorize('═' * 65, Color.BOLD))

    categories: dict[str, list] = {}
    for name, p in PRODUCTS.items():
        upgrades = p.get("upgrades", ["other"])
        cat = upgrades[0] if upgrades else "other"
        categories.setdefault(cat, []).append((name, p))

    cat_labels = {
        "macbook": "💻  MacBooks",
        "desktop": "🖥️   Desktops",
        "watch":   "⌚  Apple Watch",
        "other":   "📦  Other",
    }

    for cat, items in categories.items():
        print(f"\n  {colorize(cat_labels.get(cat, cat.title()), Color.CYAN)}")
        print(f"  {'Product':<40} {'Retail':>8}  {'Good <':>8}  {'Great <':>8}")
        print(f"  {'-'*38}  {'-'*8}  {'-'*8}  {'-'*8}")
        for name, p in sorted(items, key=lambda x: x[1]["retail"]):
            retail = p["retail"]
            good   = int(retail * p.get("good",  0.84))
            good_str = f"{'-':>8}" if p.get("insane_only") else f"${good:>7,}"
            great  = int(retail * p.get("great", 0.78))
            flags  = " ★" if name == p.get("note", "")[:10] else ""
            print(f"  {name[:40]:<40} ${retail:>7,}  {good_str}  ${great:>7,}{flags}")

    print(f"\n{colorize('═' * 65, Color.BOLD)}\n")


# ── Interactive mode ──────────────────────────────────────────────────────────

def interactive_mode() -> None:
    print(f"\n{colorize('═' * 60, Color.BOLD)}")
    print(f"  {colorize('🍎  Tech Deal Analyzer', Color.BOLD)}")
    print(f"  {colorize('Paste a listing, get a deal score.', Color.DIM)}")
    print(colorize('═' * 60, Color.BOLD))
    print("  Commands: score | products | quit\n")

    while True:
        try:
            cmd = input(f"  {colorize('>', Color.CYAN)} ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n  Bye!")
            break

        if cmd in ("q", "quit", "exit"):
            print("  Bye!")
            break

        elif cmd in ("products", "list", "p"):
            print_product_list()

        elif cmd in ("score", "s", ""):
            # Gather listing details
            try:
                print()
                req = colorize("*", Color.RED)
                opt = colorize("(opt)", Color.DIM)

                title = strip_ansi(input(f"  Title {req}           : ").strip())
                if not title:
                    print(f"\n  {colorize('Title is required.', Color.RED)}\n")
                    continue

                price_input = strip_ansi(input(f"  Price ($) {req}       : ").strip())
                price = parse_price(price_input)
                if price is None:
                    print(f"\n  {colorize('Could not parse a valid price from that input.', Color.RED)}\n")
                    continue

                condition   = strip_ansi(input(f"  Condition {opt}   : ").strip())
                description = strip_ansi(input(f"  Description {opt} : ").strip())
                source      = strip_ansi(input(f"  Source {opt}      : ").strip())

                listing = Listing(
                    title=title,
                    price=price,
                    condition=condition,
                    description=description,
                    source=source,
                )
                result = score_listing(listing)
                print_result(result)

            except (KeyboardInterrupt, EOFError):
                print("\n  Cancelled.\n")

        elif cmd == "help":
            print("  score      — analyze a listing")
            print("  products   — list all tracked products and thresholds")
            print("  quit       — exit\n")

        else:
            print(f"  {colorize('Unknown command. Try: score, products, quit', Color.DIM)}\n")


# ── One-shot CLI mode ─────────────────────────────────────────────────────────

def _safe_float(value: str) -> float:
    """Safely convert string to float, preventing DoS from excessively long inputs."""
    if len(value) > 30:
        raise argparse.ArgumentTypeError("Input string too long for float conversion.")
    try:
        return float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid float value: '{value}'")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="deal_analyzer",
        description="Score a used/refurbished tech listing from the command line.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python deal_analyzer.py --list-products
  python deal_analyzer.py --title "MacBook Air M5 24GB 512GB" --price 1050
  python deal_analyzer.py --title "MacBook Pro M4 Pro" --price 1400 --condition "Like New"
        """,
    )
    parser.add_argument("--title",         type=str,   help="Listing title")
    parser.add_argument("--price",         type=_safe_float, help="Listed price in USD")
    parser.add_argument("--condition",     type=str,   default="", help="Condition (e.g. Like New, Good)")
    parser.add_argument("--description",   type=str,   default="", help="Listing description text")
    parser.add_argument("--source",        type=str,   default="", help="Source (e.g. eBay, Swappa)")
    parser.add_argument("--list-products", action="store_true",   help="Show all tracked products")
    return parser.parse_args()


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()

    if args.list_products:
        print_product_list()
        return

    if args.title is not None or args.price is not None:
        if not args.title or args.price is None:
            print(colorize("Error: Both --title and --price must be provided for one-shot mode.", Color.RED), file=sys.stderr)
            sys.exit(1)

        if args.price <= 0:
            print(colorize("Error: --price must be a positive number.", Color.RED), file=sys.stderr)
            sys.exit(1)

        listing = Listing(
            title=strip_ansi(args.title),
            price=args.price,
            condition=strip_ansi(args.condition or ""),
            description=strip_ansi(args.description or ""),
            source=strip_ansi(args.source or ""),
        )
        result = score_listing(listing)
        print_result(result)
        return

    # No args — drop into interactive mode
    interactive_mode()


if __name__ == "__main__":
    main()
