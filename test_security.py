import unittest
from deal_analyzer import strip_ansi, Listing, main
import argparse
from unittest.mock import patch, MagicMock
import io

class TestSecurity(unittest.TestCase):
    def test_strip_ansi_basic(self):
        self.assertEqual(strip_ansi("\033[91mRed\033[0m"), "Red")
        self.assertEqual(strip_ansi("Normal Text"), "Normal Text")
        self.assertEqual(strip_ansi("Mixed \033[1mBold\033[0m and \033[2mDim\033[0m"), "Mixed Bold and Dim")

    def test_strip_ansi_complex(self):
        # More complex sequences
        self.assertEqual(strip_ansi("\x1b[38;5;208mOrange\x1b[0m"), "Orange")
        self.assertEqual(strip_ansi("\x1b[2J\x1b[HClear Screen"), "Clear Screen")

    def test_listing_sanitization_in_main(self):
        # Mocking parse_args to return malicious inputs
        mock_args = argparse.Namespace(
            title="\033[91mMalicious\033[0m Title",
            price=100.0,
            condition="\033[92mGood\033[0m",
            description="\033[93mDescription\033[0m",
            source="\033[94meBay\033[0m",
            list_products=False
        )

        with patch('deal_analyzer.parse_args', return_value=mock_args):
            with patch('deal_analyzer.score_listing') as mock_score:
                with patch('deal_analyzer.print_result'):
                    main()
                    # Capture the Listing object passed to score_listing
                    args, kwargs = mock_score.call_args
                    listing = args[0]
                    self.assertEqual(listing.title, "Malicious Title")
                    self.assertEqual(listing.condition, "Good")
                    self.assertEqual(listing.description, "Description")
                    self.assertEqual(listing.source, "eBay")

    @patch('builtins.input')
    def test_listing_sanitization_in_interactive(self, mock_input):
        # Sequence of inputs for interactive mode:
        # 1. 'score' command
        # 2. title
        # 3. price
        # 4. condition
        # 5. description
        # 6. source
        # 7. 'quit' command
        mock_input.side_effect = [
            'score',
            '\033[91mMalicious\033[0m Title',
            '100',
            '\033[92mGood\033[0m',
            '\033[93mDescription\033[0m',
            '\033[94meBay\033[0m',
            'quit'
        ]

        with patch('deal_analyzer.score_listing') as mock_score:
            with patch('deal_analyzer.print_result'):
                # Suppress stdout
                with patch('sys.stdout', new=io.StringIO()):
                    from deal_analyzer import interactive_mode
                    interactive_mode()

                    # Check if score_listing was called with sanitized Listing
                    # It should be the first call to score_listing
                    args, kwargs = mock_score.call_args
                    listing = args[0]
                    self.assertEqual(listing.title, "Malicious Title")
                    self.assertEqual(listing.condition, "Good")
                    self.assertEqual(listing.description, "Description")
                    self.assertEqual(listing.source, "eBay")

    def test_terminal_output_spoofing_sanitization(self):
        from deal_analyzer import sanitize_text
        malicious_input = "MacBook Air 13\" M5 24GB\r  Listed: $100.00\n  Matched: MacBook Air 13\" M5 24GB\n"
        sanitized = sanitize_text(malicious_input)
        self.assertNotIn("\r", sanitized)
        self.assertNotIn("\n", sanitized)
        self.assertEqual(sanitized, "MacBook Air 13\" M5 24GB   Listed: $100.00   Matched: MacBook Air 13\" M5 24GB ")

    def test_safe_float_dos(self):
        from deal_analyzer import _safe_float
        import argparse
        # Test with a normal string
        self.assertEqual(_safe_float("1200.5"), 1200.5)
        # Test with a very long string that would otherwise cause DoS
        long_string = "1" * 1000000
        with self.assertRaises(argparse.ArgumentTypeError):
            _safe_float(long_string)

    def test_parse_price_dos(self):
        from deal_analyzer import parse_price
        # Test with a normal string
        self.assertEqual(parse_price("$1,200.50"), 1200.5)
        # Test with a very long string
        long_string = "1" * 1000000
        # It should return None because it exceeds the length limit
        self.assertIsNone(parse_price(long_string))
        # Test mixed normal and long
        self.assertEqual(parse_price(f"some text {long_string} then $1,200.50"), 1200.5)

if __name__ == '__main__':
    unittest.main()
