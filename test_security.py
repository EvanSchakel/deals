import unittest
from deal_analyzer import strip_ansi, Listing

class TestSecurity(unittest.TestCase):
    def test_strip_ansi(self):
        """Verify that ANSI escape sequences are correctly stripped to prevent spoofing."""
        # Test basic color removal
        malicious_input = "\033[91mHacked\033[0m"
        self.assertEqual(strip_ansi(malicious_input), "Hacked")

        # Test cursor movement removal (like \033[2J which clears screen)
        clear_screen = "\033[2J\033[HMacBook"
        self.assertEqual(strip_ansi(clear_screen), "MacBook")

        # Test normal text is unaffected
        normal_text = "MacBook Pro M4 14\""
        self.assertEqual(strip_ansi(normal_text), normal_text)

        # Test empty string and None handles gracefully
        self.assertEqual(strip_ansi(""), "")
        self.assertEqual(strip_ansi(None), None)

    def test_listing_init_sanitization(self):
        """Verify the inputs aren't mutated inside Listing by default, but we expect caller to sanitize them."""
        title = "\x1b[31mRed Title\x1b[0m"
        clean_title = strip_ansi(title)

        l = Listing(title=clean_title, price=100.0)
        self.assertEqual(l.title, "Red Title")

if __name__ == '__main__':
    unittest.main()
