import unittest
from deal_analyzer import Listing, score_listing

class TestDealAnalyzer(unittest.TestCase):
    def test_score_listing_no_product_match(self):
        """Test fallback branch when a listing does not match any product."""
        # Non-scammy listing with an unrecognized product
        listing = Listing(
            title="A completely unknown gadget",
            price=100.0,
            description="It works.",
            condition="Used",
            source="Craigslist"
        )
        result = score_listing(listing)
        self.assertEqual(result.score, 3)
        self.assertIn("No matching product found in the database", result.verdict)
        self.assertIsNone(result.matched_product)
        self.assertIsNone(result.retail_price)

    def test_score_listing_no_product_match_scammy(self):
        """Test fallback branch when an unrecognized product is marked as a scam."""
        # Scammy listing with an unrecognized product
        listing = Listing(
            title="A completely unknown gadget",
            price=100.0,
            description="iCloud locked, cannot test.",
            condition="Parts only",
            source="Craigslist"
        )
        result = score_listing(listing)
        self.assertEqual(result.score, 1)
        self.assertIn("No matching product found in the database", result.verdict)
        self.assertIsNone(result.matched_product)
        self.assertIsNone(result.retail_price)

if __name__ == '__main__':
    unittest.main()
