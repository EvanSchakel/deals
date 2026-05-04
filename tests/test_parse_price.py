import unittest
from deal_analyzer import parse_price

class TestParsePrice(unittest.TestCase):
    def test_valid_strings(self):
        """Test valid strings with typical formats."""
        self.assertEqual(parse_price("$1,299"), 1299.0)
        self.assertEqual(parse_price("1299.99"), 1299.99)
        self.assertEqual(parse_price("$1200"), 1200.0)
        self.assertEqual(parse_price("1000"), 1000.0)

    def test_out_of_bounds(self):
        """Test values outside the 50 < value < 30_000 range."""
        # Lower bound
        self.assertIsNone(parse_price("$50"), "Values <= 50 should return None")
        self.assertIsNone(parse_price("$49.99"), "Values <= 50 should return None")
        self.assertEqual(parse_price("$50.01"), 50.01)

        # Upper bound
        self.assertIsNone(parse_price("$30,000"), "Values >= 30,000 should return None")
        self.assertIsNone(parse_price("$30,001"), "Values >= 30,000 should return None")
        self.assertEqual(parse_price("$29,999.99"), 29999.99)

    def test_price_ranges(self):
        """Test price ranges where second value is stripped out."""
        self.assertEqual(parse_price("$1000 - $1200"), 1000.0)
        self.assertEqual(parse_price("1000 to 1200"), 1000.0)
        self.assertEqual(parse_price("$1000-$1200"), 1000.0)
        self.assertEqual(parse_price("1000–1200"), 1000.0)
        self.assertEqual(parse_price("1000 - 1200"), 1000.0)

    def test_text_containing_prices(self):
        """Test standard descriptive strings with prices."""
        self.assertEqual(parse_price("Selling for $1200 OBO"), 1200.0)
        self.assertEqual(parse_price("MacBook Pro for 1299.99 brand new"), 1299.99)
        self.assertEqual(parse_price("asking 1000 shipped"), 1000.0)

    def test_invalid_formats_and_edge_cases(self):
        """Test invalid strings and edge cases."""
        self.assertIsNone(parse_price("abc"))
        self.assertIsNone(parse_price(""))
        self.assertIsNone(parse_price(None))
        self.assertIsNone(parse_price("Free"))
        self.assertIsNone(parse_price("Selling my MacBook for a good price"))

if __name__ == "__main__":
    unittest.main()
