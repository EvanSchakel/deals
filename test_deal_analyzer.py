import unittest
from deal_analyzer import match_product

class TestDealAnalyzer(unittest.TestCase):
    def test_match_product_mbp_abbreviation(self):
        # "mbp" should be expanded to "macbook pro"
        # "MacBook Pro 14\" M5" has tag "macbook pro 14 m5"
        # If we input "mbp 14 m5", it should match.
        title = "mbp 14 m5"
        matched = match_product(title)
        self.assertEqual(matched, "MacBook Pro 14\" M5")

    def test_match_product_mba_abbreviation(self):
        # "mba" should be expanded to "macbook air"
        # "MacBook Air 13\" M5 24GB" has tag "macbook air m5"
        title = "mba m5"
        matched = match_product(title)
        self.assertEqual(matched, "MacBook Air 13\" M5 24GB")

    def test_match_product_abbreviation_in_description(self):
        title = "Apple Laptop"
        description = "This is a great mbp 16 m5 pro for sale"
        matched = match_product(title, description)
        self.assertEqual(matched, "MacBook Pro 16\" M5 Pro")

    def test_match_product_mixed_case_abbreviation(self):
        title = "MBP 14 M4 PRO"
        matched = match_product(title)
        self.assertEqual(matched, "MacBook Pro 14\" M4 Pro")

    def test_match_product_no_match_abbreviation(self):
        title = "mbp non-existent-model"
        matched = match_product(title)
        self.assertIsNone(matched)

    def test_realistic_price_parsing(self):
        from deal_analyzer import parse_price
        self.assertEqual(parse_price("512GB for $1200"), 1200.0)
        self.assertEqual(parse_price("1299"), 1299.0)
        self.assertEqual(parse_price("Price: 1299.99"), 1299.99)
        self.assertEqual(parse_price("$1,299 obo"), 1299.0)
        self.assertEqual(parse_price("512GB 1200"), 1200.0)
        self.assertIsNone(parse_price("No price here just 512GB and 120Hz"))

    def test_realistic_scam_detection(self):
        from deal_analyzer import check_scam
        # 'gazelle' shouldn't trigger 'zelle'
        scam_level, signals = check_scam("Selling my old gazelle")
        self.assertEqual(scam_level, "none")
        self.assertFalse(any("zelle" in s for s in signals))

        # Exact 'zelle' should trigger
        scam_level, signals = check_scam("Pay me with Zelle only")
        self.assertEqual(scam_level, "high")
        self.assertTrue(any("zelle" in s for s in signals))

    def test_realistic_product_matching(self):
        from deal_analyzer import match_product
        # Missing size spec (14/16 inch) should match shortest matching tag
        matched = match_product("MacBook Pro M4 Pro")
        self.assertEqual(matched, "MacBook Pro 14\" M4 Pro")

        # Test noisy titles
        matched = match_product("MacBook Pro 14-inch M4 Pro!!")
        self.assertEqual(matched, "MacBook Pro 14\" M4 Pro")

if __name__ == "__main__":
    unittest.main()
