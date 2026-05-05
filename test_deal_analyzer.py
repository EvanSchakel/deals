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

    def test_parse_price_formats(self):
        from deal_analyzer import parse_price
        self.assertEqual(parse_price("$1,299.99"), 1299.99)
        self.assertEqual(parse_price("Asking 1500"), 1500.0)
        self.assertEqual(parse_price("1,500 to 2,000"), 1500.0)
        self.assertEqual(parse_price("Price: $500 - $600"), 500.0)
        self.assertIsNone(parse_price("Invalid text"))
        self.assertIsNone(parse_price("10")) # Below $50 threshold
        self.assertIsNone(parse_price("50000")) # Above $30,000 threshold

    def test_score_listing_gates(self):
        from deal_analyzer import Listing, score_listing
        # Test RAM gate (MacBook Air 13" M5 requires 24GB)
        listing_no_ram = Listing(title="MacBook Air 13 M5", price=1000)
        res_no_ram = score_listing(listing_no_ram)
        self.assertTrue(any("RAM not confirmed" in w for w in res_no_ram.warnings))

        listing_with_ram = Listing(title="MacBook Air 13 M5 24GB", price=1000)
        res_with_ram = score_listing(listing_with_ram)
        self.assertFalse(any("RAM not confirmed" in w for w in res_with_ram.warnings))

        # Test Storage gate (MacBook Air 13" M4 512GB+ requires 512GB+)
        listing_no_storage = Listing(title="MacBook Air 13 M4", price=1000)
        res_no_storage = score_listing(listing_no_storage)
        self.assertTrue(any("requires 512GB+ storage" in w for w in res_no_storage.warnings))

        listing_with_storage = Listing(title="MacBook Air 13 M4 512GB", price=1000)
        res_with_storage = score_listing(listing_with_storage)
        self.assertFalse(any("requires 512GB+ storage" in w for w in res_with_storage.warnings))

    def test_score_listing_scam_high(self):
        from deal_analyzer import Listing, score_listing
        listing = Listing(title="MacBook Pro 14 M4 Pro", description="zelle only", price=1000)
        res = score_listing(listing)
        self.assertEqual(res.scam_level, "high")
        self.assertLessEqual(res.score, 2)
        self.assertIn("⚠️  SCAM WARNING — do not proceed.", res.verdict)

if __name__ == "__main__":
    unittest.main()
