import unittest
from deal_analyzer import Listing, AnalysisResult, score_listing
from products import PRODUCTS

class TestDealAnalyzer(unittest.TestCase):

    def test_no_product_match(self):
        # Base score 3 if scam_level == "none"
        listing_no_scam = Listing(title="Unknown Product", price=100)
        result1 = score_listing(listing_no_scam)
        self.assertEqual(result1.score, 3)

        # Base score 1 otherwise
        # using a high scam word "icloud locked"
        listing_high_scam = Listing(title="Unknown Product icloud locked", price=100)
        result2 = score_listing(listing_high_scam)
        self.assertEqual(result2.score, 1)

    def test_price_thresholds_great(self):
        # MacBook Air 15" M5 tags: ["macbook air 15 m5", "mba 15 m5", "air 15 m5"]
        # Retail 1499, great <= 0.86
        # Include "24gb" to bypass RAM gate
        price_great = 1499 * 0.86
        listing = Listing(title="macbook air 15 m5 24gb", price=price_great)
        result = score_listing(listing)
        self.assertEqual(result.score, 9)

    def test_price_thresholds_good(self):
        # MacBook Air 15" M5 tags: ["macbook air 15 m5", "mba 15 m5", "air 15 m5"]
        # Retail 1499, good <= 0.90
        # price > great to hit good threshold
        price_good = 1499 * 0.88
        listing = Listing(title="macbook air 15 m5 24gb", price=price_good)
        result = score_listing(listing)
        self.assertEqual(result.score, 7)

    def test_price_thresholds_decent(self):
        # MacBook Air 15" M5 tags: ["macbook air 15 m5", "mba 15 m5", "air 15 m5"]
        # Retail 1499, decent <= 0.94
        price_decent = 1499 * 0.92
        listing = Listing(title="macbook air 15 m5 24gb", price=price_decent)
        result = score_listing(listing)
        self.assertEqual(result.score, 5)

    def test_price_thresholds_near_retail(self):
        # MacBook Air 15" M5 tags: ["macbook air 15 m5", "mba 15 m5", "air 15 m5"]
        # Retail 1499, near retail <= 1.01
        price_near_retail = 1499 * 0.98
        listing = Listing(title="macbook air 15 m5 24gb", price=price_near_retail)
        result = score_listing(listing)
        self.assertEqual(result.score, 3)

    def test_price_thresholds_above_retail(self):
        # MacBook Air 15" M5 tags: ["macbook air 15 m5", "mba 15 m5", "air 15 m5"]
        # Retail 1499, above retail > 1.01
        price_above_retail = 1499 * 1.05
        listing = Listing(title="macbook air 15 m5 24gb", price=price_above_retail)
        result = score_listing(listing)
        self.assertEqual(result.score, 1)

    def test_ram_gate_missing(self):
        # MacBook Air 13" M5 24GB requires 24GB RAM
        # if missing, reduces base_score by 1
        # Great deal base score is 9, should become 8
        price_great = 1299 * 0.86
        listing = Listing(title="macbook air 13 m5", price=price_great)
        result = score_listing(listing)
        self.assertEqual(result.score, 8)

    def test_ram_gate_present(self):
        # MacBook Air 13" M5 24GB requires 24GB RAM
        price_great = 1299 * 0.86
        listing = Listing(title="macbook air 13 m5 24gb", price=price_great)
        result = score_listing(listing)
        self.assertEqual(result.score, 9)

    def test_storage_gate_missing(self):
        # MacBook Air 13" M4 512GB+ requires 512GB+ storage and 24GB+ RAM
        # if storage missing, reduces base score by 2
        # Great deal base score is 9, should become 7
        price_great = 1299 * 0.78
        listing = Listing(title="macbook air 13 m4 24gb", price=price_great)
        result = score_listing(listing)
        self.assertEqual(result.score, 7)

    def test_storage_gate_present(self):
        # MacBook Air 13" M4 512GB+ requires 512GB+ storage and 24GB+ RAM
        price_great = 1299 * 0.78
        listing = Listing(title="macbook air 13 m4 24gb 512gb", price=price_great)
        result = score_listing(listing)
        self.assertEqual(result.score, 9)

    def test_condition_modifier_bonus(self):
        # "new" condition gives +1 bonus
        price_good = 1499 * 0.88 # base score 7
        listing = Listing(title="macbook air 15 m5 24gb", price=price_good, condition="New")
        result = score_listing(listing)
        self.assertEqual(result.score, 8)

    def test_condition_modifier_penalty(self):
        # "fair" condition gives -2 penalty
        price_good = 1499 * 0.88 # base score 7
        listing = Listing(title="macbook air 15 m5 24gb", price=price_good, condition="Fair")
        result = score_listing(listing)
        self.assertEqual(result.score, 5)

    def test_scam_modifier_high(self):
        # high scam: max score is 2. Base score for great deal is 9 -> caps at 2.
        # keyword: "icloud locked"
        price_great = 1499 * 0.86
        listing = Listing(title="macbook air 15 m5 24gb icloud locked", price=price_great)
        result = score_listing(listing)
        self.assertEqual(result.score, 2)

    def test_scam_modifier_medium(self):
        # medium scam: reduces score by 2
        # keyword: "selling for a friend"
        price_great = 1499 * 0.86 # base score 9
        listing = Listing(title="macbook air 15 m5 24gb", description="selling for a friend", price=price_great)
        result = score_listing(listing)
        self.assertEqual(result.score, 7)

    def test_scam_modifier_low(self):
        # low scam: reduces score by 1
        # keyword (flags): "box only"
        price_great = 1499 * 0.86 # base score 9
        listing = Listing(title="macbook air 15 m5 24gb", description="box only", price=price_great)
        result = score_listing(listing)
        self.assertEqual(result.score, 8)

    def test_score_clamping_max(self):
        # Score clamping max 10
        # great deal (9) + condition bonus (1) + another great deal indicator = 10, won't exceed 10.
        # Even with extremely low price, it stays 10
        price_insane = 1499 * 0.10
        listing = Listing(title="macbook air 15 m5 24gb", price=price_insane, condition="new")
        result = score_listing(listing)
        self.assertEqual(result.score, 10)

    def test_score_clamping_min(self):
        # Score clamping min 1
        # bad deal (1) + condition penalty (-2)
        price_above_retail = 1499 * 1.5
        listing = Listing(title="macbook air 15 m5 24gb", price=price_above_retail, condition="fair")
        result = score_listing(listing)
        self.assertEqual(result.score, 1)

if __name__ == '__main__':
    unittest.main()
