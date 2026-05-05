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

if __name__ == "__main__":
    unittest.main()
