# 🍎 Deal Analyzer

A command-line tool for scoring used and refurbished Apple tech listings — no subscriptions, no API keys, no external dependencies.

Paste a listing title and price, get back a **1–10 deal score**, scam signal detection, and a plain-English verdict in under a second.

---

## Features

- **Deal scoring** — compares price to retail thresholds (good / great) for 25+ Apple products
- **Product matching** — automatically identifies the product from listing text using tag-based matching
- **RAM & storage gates** — flags listings that don't confirm required specs
- **Scam detection** — checks for 40+ high, medium, and flag-level signals (iCloud lock variants, sketchy payment methods, off-platform contact, condition disclosures)
- **Interactive mode** — step-by-step prompts for scoring one listing at a time
- **One-shot CLI mode** — pipe in arguments directly for scripting or batch use
- **Product browser** — `--list-products` shows every tracked product with retail price and deal thresholds

---

## Requirements

- Python 3.10+
- No third-party packages — pure stdlib

---

## Usage

**Interactive mode** (prompts you through each field):
```bash
python deal_analyzer.py
```

**One-shot mode** (great for scripts):
```bash
python deal_analyzer.py --title "MacBook Air M5 24GB 512GB" --price 1050
python deal_analyzer.py --title "MacBook Pro 14 M4 Pro 24GB Like New" --price 1420 --condition "Like New"
python deal_analyzer.py --title "Apple Watch Ultra 2 49mm" --price 580 --source "eBay"
```

**List all tracked products and thresholds:**
```bash
python deal_analyzer.py --list-products
```

---

## Example Output

```
────────────────────────────────────────────────────────────
  MacBook Pro 14 M4 Pro 24GB
  Listed: $1,420.00  (retail: $1,999)
  Matched: MacBook Pro 14" M4 Pro

  ★★★★★★★★☆☆  8/10
  Good deal — meaningfully below retail.
  Scam risk: NONE

  Score Breakdown:
    → Matched: MacBook Pro 14" M4 Pro  |  $1,420 vs $1,999 retail  |  29.0% off
    → Base score: 7/10
    → Condition bonus: new/open-box (+1)
────────────────────────────────────────────────────────────
```

---

## Scoring Scale

| Score | Meaning |
|-------|---------|
| 9–10  | Great deal — well below market |
| 7–8   | Good deal — meaningful discount |
| 5–6   | Decent — moderate savings |
| 3–4   | Near retail — not worth it used |
| 1–2   | Above retail or scam risk |

Scores are capped at **2** for HIGH scam risk signals and reduced by 2 for MEDIUM signals.

---

## Extending the Product Database

Open `products.py` and add an entry to the `PRODUCTS` dict:

```python
"iPhone 16 Pro 256GB": {
    "retail": 1099,
    "good":   0.84,   # flag as "good" at 16% off → $923
    "great":  0.76,   # flag as "great" at 24% off → $835
    "ram_gate": None,
    "tags": ["iphone 16 pro", "ip16 pro", "iphone 16pro"],
    "upgrades": ["phone"],
},
```

No code changes needed anywhere else — the analyzer picks it up automatically.

---

## Adding Scam Signals

Open `products.py` and add phrases to any of the three lists:

```python
SCAM_HIGH   # → score capped at 2
SCAM_MEDIUM # → score -2
SCAM_FLAGS  # → score -1 (condition disclosures)
```

---

## Project Structure

```
deal-analyzer/
├── deal_analyzer.py   # main program — scoring, CLI, output formatting
├── products.py        # product database and scam signal lists
└── README.md
```

---

## License

MIT — use it, fork it, extend it however you like.
