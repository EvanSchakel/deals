import unittest
from deal_analyzer import Listing, strip_ansi

class TestSecurity(unittest.TestCase):
    def test_strip_ansi(self):
        malicious = "Normal \033[31mRed\033[0m Text"
        self.assertEqual(strip_ansi(malicious), "Normal Red Text")

    def test_listing_sanitization(self):
        listing = Listing(
            title="\033[31mHacked Title\033[0m",
            price=100.0,
            condition="Good\033[32m",
            description="Buy \x1B[1mNow",
            source="\033[0meBay"
        )
        self.assertEqual(listing.title, "Hacked Title")
        self.assertEqual(listing.condition, "Good")
        self.assertEqual(listing.description, "Buy Now")
        self.assertEqual(listing.source, "eBay")

if __name__ == '__main__':
    unittest.main()
