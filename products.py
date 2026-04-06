"""
products.py
────────────────────────────────────────────────────────────────
Product database for the deal analyzer.

Each entry defines:
  - retail:       MSRP in USD
  - good:         ratio threshold for a "good" deal  (e.g. 0.84 = 16% off)
  - great:        ratio threshold for a "great" deal (e.g. 0.78 = 22% off)
  - tags:         lowercase keywords to match against a listing title
  - ram_gate:     minimum RAM (GB) to consider the listing valid (optional)
  - require_512:  if True, listing must mention 512GB+ storage (optional)
  - insane_only:  if True, only alert at the "great" threshold (optional)
  - upgrades:     category tag for grouping ["macbook", "desktop", "watch"]
  - note:         human-readable note shown in --list-products output

To add a product, copy any entry below and edit the values.
────────────────────────────────────────────────────────────────
"""

# ── MacBooks ──────────────────────────────────────────────────────────────────

PRODUCTS: dict[str, dict] = {

    # ─ MacBook Air M5 ─────────────────────────────────────────────────────────
    "MacBook Air 13\" M5 24GB": {
        "retail": 1299,
        "good":   0.90,
        "great":  0.86,
        "ram_gate": 24,
        "tags": [
            "macbook air 13 m5", "mba 13 m5", "air 13 m5",
            "macbook air m5 13", "macbook air m5",
        ],
        "upgrades": ["macbook"],
        "note": "PRIMARY TARGET — launched March 2026, open-box only for now",
    },
    "MacBook Air 15\" M5": {
        "retail": 1499,
        "good":   0.90,
        "great":  0.86,
        "ram_gate": 24,
        "tags": ["macbook air 15 m5", "mba 15 m5", "air 15 m5"],
        "upgrades": ["macbook"],
    },

    # ─ MacBook Air M4 ─────────────────────────────────────────────────────────
    "MacBook Air 13\" M4 512GB+": {
        "retail":       1299,
        "good":         0.84,
        "great":        0.78,
        "ram_gate":     24,
        "require_512":  True,
        "tags": [
            "macbook air 13 m4", "mba 13 m4", "air 13 m4",
            "macbook air m4 13",
        ],
        "upgrades": ["macbook"],
        "note": "Storage upgrade only — 512GB+ required to match filter",
    },
    "MacBook Air 15\" M4": {
        "retail":   1299,
        "good":     0.84,
        "great":    0.76,
        "ram_gate": 24,
        "tags": ["macbook air 15 m4", "mba 15 m4", "air 15 m4"],
        "upgrades": ["macbook"],
    },

    # ─ MacBook Pro M5 ─────────────────────────────────────────────────────────
    "MacBook Pro 14\" M5 Pro": {
        "retail":   2199,
        "good":     0.83,
        "great":    0.73,
        "ram_gate": 24,
        "tags": [
            "macbook pro 14 m5 pro", "mbp 14 m5 pro", "pro 14 m5 pro",
        ],
        "upgrades": ["macbook"],
        "note": "Very new (March 2026) — great deals will be rare",
    },
    "MacBook Pro 14\" M5": {
        "retail":   1599,
        "good":     0.86,
        "great":    0.80,
        "ram_gate": 24,
        "tags": ["macbook pro 14 m5", "mbp 14 m5", "pro 14 m5"],
        "upgrades": ["macbook"],
        "note": "Same chip as M5 Air — only worth buying at a steep discount",
    },
    "MacBook Pro 16\" M5 Pro": {
        "retail":   2499,
        "good":     0.84,
        "great":    0.78,
        "ram_gate": 24,
        "tags": ["macbook pro 16 m5 pro", "mbp 16 m5 pro", "pro 16 m5"],
        "upgrades": ["macbook"],
    },
    "MacBook Pro 14\" M5 Max": {
        "retail":   3499,
        "good":     0.84,
        "great":    0.78,
        "ram_gate": 24,
        "tags": ["macbook pro 14 m5 max", "mbp 14 m5 max", "pro 14 m5 max"],
        "upgrades": ["macbook"],
    },

    # ─ MacBook Pro M4 ─────────────────────────────────────────────────────────
    "MacBook Pro 14\" M4 Pro": {
        "retail":   1999,
        "good":     0.82,
        "great":    0.75,
        "ram_gate": 24,
        "tags": [
            "macbook pro 14 m4 pro", "mbp 14 m4 pro", "pro 14 m4 pro",
        ],
        "upgrades": ["macbook"],
        "note": "Target ~$1,400–$1,500 used",
    },
    "MacBook Pro 14\" M4 Max": {
        "retail":   2499,
        "good":     0.84,
        "great":    0.78,
        "ram_gate": 24,
        "tags": ["macbook pro 14 m4 max", "mbp 14 m4 max", "pro 14 m4 max"],
        "upgrades": ["macbook"],
    },
    "MacBook Pro 16\" M4 Pro": {
        "retail":   2499,
        "good":     0.84,
        "great":    0.78,
        "ram_gate": 24,
        "tags": ["macbook pro 16 m4 pro", "mbp 16 m4 pro", "pro 16 m4"],
        "upgrades": ["macbook"],
    },
    "MacBook Pro 16\" M4 Max": {
        "retail":   3499,
        "good":     0.84,
        "great":    0.78,
        "ram_gate": 24,
        "tags": ["macbook pro 16 m4 max", "mbp 16 m4 max", "pro 16 m4 max"],
        "upgrades": ["macbook"],
    },

    # ── Desktops ──────────────────────────────────────────────────────────────

    "Mac Mini M4 Pro": {
        "retail":   1399,
        "good":     0.84,
        "great":    0.78,
        "tags":     ["mac mini m4 pro", "mini m4 pro"],
        "upgrades": ["desktop"],
    },
    "Mac Studio M4 Max": {
        "retail":   1999,
        "good":     0.84,
        "great":    0.78,
        "tags":     ["mac studio m4 max", "studio m4 max"],
        "upgrades": ["desktop"],
    },
    "Mac Studio M3 Ultra": {
        "retail":   3999,
        "good":     0.84,
        "great":    0.78,
        "tags": [
            "mac studio m3 ultra", "studio m3 ultra",
            "mac studio ultra 2025",
        ],
        "upgrades": ["desktop"],
        "note": "Current flagship — M4 Ultra does not exist",
    },
    "Mac Studio M2 Ultra 64GB": {
        "retail":   2800,
        "good":     0.76,
        "great":    0.67,
        "tags":     ["mac studio m2 ultra", "studio m2 ultra"],
        "upgrades": ["desktop"],
        "note":     "800 GB/s bandwidth — excellent for local AI workloads",
    },
    "Mac Studio M1 Ultra 64GB": {
        "retail":   2200,
        "good":     0.76,
        "great":    0.67,
        "tags": [
            "mac studio m1 ultra", "studio m1 ultra",
            "mac studio ultra 2022",
        ],
        "upgrades": ["desktop"],
    },

    # ── Apple Watch ───────────────────────────────────────────────────────────

    "Apple Watch Ultra 3": {
        "retail":   799,
        "good":     0.82,
        "great":    0.73,
        "tags":     ["apple watch ultra 3", "watch ultra 3", "ultra 3 49mm"],
        "upgrades": ["watch"],
        "note":     "PRIMARY WATCH TARGET",
    },
    "Apple Watch Ultra 2": {
        "retail":   799,
        "good":     0.82,
        "great":    0.73,
        "tags":     ["apple watch ultra 2", "watch ultra 2", "ultra 2 49mm"],
        "upgrades": ["watch"],
    },
    "Apple Watch Ultra 1 (49mm)": {
        "retail":      599,
        "good":        0.70,
        "great":       0.58,
        "insane_only": True,
        "tags": [
            "apple watch ultra 49mm", "watch ultra 49mm",
            "apple watch ultra titanium", "apple watch ultra 1st gen",
            "apple watch ultra first gen",
        ],
        "upgrades": ["watch"],
        "note":     "1st gen Ultra — insane deal only (discontinued)",
    },
    "Apple Watch Series 11 45mm": {
        "retail":      429,
        "good":        0.74,
        "great":       0.62,
        "insane_only": True,
        "tags":        ["apple watch series 11 45", "watch 11 45", "series 11 45mm"],
        "upgrades":    ["watch"],
    },
    "Apple Watch Series 11 41mm": {
        "retail":      399,
        "good":        0.74,
        "great":       0.62,
        "insane_only": True,
        "tags":        ["apple watch series 11 41", "watch 11 41", "series 11 41mm"],
        "upgrades":    ["watch"],
    },
    "Apple Watch Series 10 46mm": {
        "retail":      429,
        "good":        0.74,
        "great":       0.62,
        "insane_only": True,
        "tags":        ["apple watch series 10 46", "watch 10 46", "series 10 46mm"],
        "upgrades":    ["watch"],
    },
    "Apple Watch Series 10 42mm": {
        "retail":      399,
        "good":        0.74,
        "great":       0.62,
        "insane_only": True,
        "tags":        ["apple watch series 10 42", "watch 10 42", "series 10 42mm"],
        "upgrades":    ["watch"],
    },
    "Apple Watch SE 3 44mm": {
        "retail":      279,
        "good":        0.70,
        "great":       0.56,
        "insane_only": True,
        "tags":        ["apple watch se 3", "watch se 3 44", "se3 44mm", "apple watch se3"],
        "upgrades":    ["watch"],
    },
}


# ── Scam signal libraries ─────────────────────────────────────────────────────
# These lists are intentionally public — no personal info, pure pattern matching.

SCAM_HIGH: list[str] = [
    # iCloud / activation lock
    "icloud locked", "activation lock", "unknown passcode", "icloud lock",
    "locked to icloud", "find my enabled", "find my is on",
    "linked to previous owner", "cannot turn off find my",
    # Sketchy payment methods
    "zelle", "venmo", "cash app", "cashapp", "western union",
    "wire transfer", "gift card", "google play card",
    "bank transfer", "bank wire", "revolut",
    "paypal friends and family", "paypal f&f",
    "crypto", "bitcoin", "ethereum",
    # Off-platform contact
    "text me at", "email me outside", "contact me at",
    "i'm deployed", "military deployment", "i am overseas",
    "shipping agent", "escrow service",
    # Non-functional
    "for parts only", "parts not working", "does not power on",
]

SCAM_MEDIUM: list[str] = [
    "selling for a friend", "not mine to test fully",
    "must sell today", "leaving the country",
    "international shipping only", "cannot meet in person",
    "stock photos", "representative image",
    "no returns accepted", "as-is no returns",
]

SCAM_FLAGS: list[str] = [
    # These are condition disclosures — they lower the score but don't kill it
    "box only", "no charger", "screen has lines", "cracked", "dent",
    "cosmetic damage", "keyboard issue", "battery swollen", "battery health",
    "touch id not working", "face id not working", "one speaker",
    "powers on but", "works but",
]
