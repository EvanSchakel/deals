<div align="center">
  <h1>🍎 Deal Analyzer</h1>
  <p><i>A blazing fast, zero-dependency CLI tool for scoring used and refurbished Apple tech listings.</i></p>

  [![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/ci.yml)
  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
</div>

---

## 🎯 The Problem
Finding a genuinely good deal on used Apple hardware is tough. Prices fluctuate, scammers use the same tricks over and over, and knowing exactly what "15% off retail" looks like requires doing math in your head.

## 💡 The Solution
**Deal Analyzer** instantly scores listings from 1 to 10. Just paste a title and a price.
It matches the product, compares the price to hardcoded "good" and "great" thresholds, and checks the text against 40+ known scam and flag signals.

It runs locally, requires no subscriptions, uses no API keys, and has zero external dependencies.

---

## ✨ Features

- **📊 Deal Scoring** — Automatically compares price to retail thresholds (good / great) for 25+ Apple products.
- **🏷️ Product Matching** — Intelligently identifies the exact product model from messy listing text using tag-based matching.
- **🛡️ RAM & Storage Gates** — Flags suspicious listings that try to hide missing base specs.
- **🚨 Scam Detection** — Checks for 40+ high, medium, and flag-level signals (e.g., iCloud lock variants, sketchy payment methods, off-platform contact).
- **🕹️ Interactive Mode** — Step-by-step terminal prompts for scoring listings manually.
- **⚡ One-Shot CLI Mode** — Pipe in arguments directly for ultra-fast scripting or batch processing.
- **📖 Product Browser** — `--list-products` displays the entire database of tracked products, retail prices, and deal thresholds.

---

## 🚀 Installation

You can install Deal Analyzer directly via `pip` or use it from the source.

### Option 1: Install via pip (Recommended)
This method installs the `deal-analyzer` command globally on your system.

```bash
git clone https://github.com/OWNER/REPO.git
cd deal-analyzer
pip install .
```

### Option 2: Run from Source
```bash
git clone https://github.com/OWNER/REPO.git
cd deal-analyzer
python deal_analyzer.py
```

*Requires Python 3.10 or higher.*

---

## 🛠️ Usage

### Interactive Mode
Run the tool without arguments to enter the step-by-step interactive prompt:
```bash
deal-analyzer
```

### One-Shot CLI Mode (Great for scripts)
Provide the details directly via flags to get an instant score:
```bash
deal-analyzer --title "MacBook Air M3 24GB 512GB" --price 1050
deal-analyzer --title "MacBook Pro 14 M4 Pro 24GB Like New" --price 1420 --condition "Like New"
deal-analyzer --title "Apple Watch Ultra 2 49mm" --price 580 --source "eBay"
```

### List Tracked Products
View the database of tracked products, their retail prices, and scoring thresholds:
```bash
deal-analyzer --list-products
```

---

## 📈 Example Output

```text
────────────────────────────────────────────────────────────
  MacBook Pro 14 M4 Pro 24GB
  Listed: $1,420.00  (retail: $1,999)
  Matched: MacBook Pro 14" M4 Pro

  ★★★★★★★★☆☆  8/10
  Good deal — meaningfully below retail.
  Scam risk: NONE

  Notes:
    → Matched: MacBook Pro 14" M4 Pro  |  $1,420 vs $1,999 retail  |  29.0% off
    → Condition bonus: like new (+1)
────────────────────────────────────────────────────────────
```

---

## 📏 Scoring Scale

| Score | Meaning |
|-------|---------|
| **9–10** | Great deal — well below market value |
| **7–8**  | Good deal — meaningful discount |
| **5–6**  | Decent — moderate savings |
| **3–4**  | Near retail — not worth it used |
| **1–2**  | Above retail or major scam risk detected |

*Note: Scores are capped at **2** for HIGH scam risk signals and reduced by **2** for MEDIUM signals.*

---

## 🤝 Contributing

We welcome contributions! Deal Analyzer is designed to be easily extensible.

- **Adding a Product**: Open `products.py` and add a new entry to the `PRODUCTS` dictionary.
- **Adding Scam Signals**: Open `products.py` and add phrases to `SCAM_HIGH`, `SCAM_MEDIUM`, or `SCAM_FLAGS`.

Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — use it, fork it, extend it however you like.
