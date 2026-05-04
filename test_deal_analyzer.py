import unittest
from deal_analyzer import parse_price

class TestParsePrice(unittest.TestCase):
    def test_valid_prices(self):
        self.assertEqual(parse_price("$1,299"), 1299.0)
        self.assertEqual(parse_price("1299.99"), 1299.99)
        self.assertEqual(parse_price("Price: $500"), 500.0)

    def test_out_of_bounds_prices(self):
        # Value too low
        self.assertIsNone(parse_price("$50"))
        self.assertIsNone(parse_price("49.99"))

        # Value too high
        self.assertIsNone(parse_price("$30,000"))
        self.assertIsNone(parse_price("50000.00"))

    def test_value_error_cases(self):
        # Token has no digits after stripping
        self.assertIsNone(parse_price("free"))
        self.assertIsNone(parse_price("N/A"))
        self.assertIsNone(parse_price("---"))

        # Token evaluates to empty string after stripping
        self.assertIsNone(parse_price("abc"))

        # Only periods (results in float('.') which raises ValueError)
        self.assertIsNone(parse_price("..."))

        # Mixed tokens where the first one fails but the second succeeds
        self.assertEqual(parse_price("free 1000"), 1000.0)
        self.assertEqual(parse_price("... $1,299"), 1299.0)
        self.assertEqual(parse_price("N/A 1500.00"), 1500.0)

        # Tokens where the first is out of bounds, but the next is valid
        self.assertEqual(parse_price("$10 1000"), 1000.0)

if __name__ == "__main__":
    unittest.main()
