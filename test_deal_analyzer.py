import unittest
from deal_analyzer import check_scam
from products import SCAM_HIGH, SCAM_MEDIUM, SCAM_FLAGS

class TestCheckScam(unittest.TestCase):

    def test_check_scam_none(self):
        # Safe text should return "none" and an empty list of signals
        text = "This is a completely normal listing. Works perfectly."
        level, signals = check_scam(text)
        self.assertEqual(level, "none")
        self.assertEqual(signals, [])

    def test_check_scam_low(self):
        # Text with a phrase from SCAM_FLAGS should return "low" and the signal
        flag_phrase = SCAM_FLAGS[0]
        text = f"The condition is okay, but {flag_phrase}."
        level, signals = check_scam(text)
        self.assertEqual(level, "low")
        self.assertIn(f"[FLAG] {flag_phrase}", signals)

    def test_check_scam_medium(self):
        # Text with a phrase from SCAM_MEDIUM should return "medium"
        medium_phrase = SCAM_MEDIUM[0]
        text = f"I am {medium_phrase}."
        level, signals = check_scam(text)
        self.assertEqual(level, "medium")
        self.assertIn(f"[MEDIUM] {medium_phrase}", signals)

    def test_check_scam_high(self):
        # Text with a phrase from SCAM_HIGH should return "high"
        high_phrase = SCAM_HIGH[0]
        text = f"The phone is {high_phrase}."
        level, signals = check_scam(text)
        self.assertEqual(level, "high")
        self.assertIn(f"[HIGH] {high_phrase}", signals)

    def test_check_scam_case_insensitive(self):
        # Text should match regardless of case
        high_phrase = SCAM_HIGH[0]
        # Uppercase the phrase in text
        text = f"The phone is {high_phrase.upper()}."
        level, signals = check_scam(text)
        self.assertEqual(level, "high")
        self.assertIn(f"[HIGH] {high_phrase}", signals)

    def test_check_scam_multiple(self):
        # Multiple signals, should return the highest level ("high")
        high_phrase = SCAM_HIGH[0]
        medium_phrase = SCAM_MEDIUM[0]
        flag_phrase = SCAM_FLAGS[0]

        text = f"It is {high_phrase}, {medium_phrase}, and {flag_phrase}."
        level, signals = check_scam(text)

        self.assertEqual(level, "high")
        self.assertIn(f"[HIGH] {high_phrase}", signals)
        self.assertIn(f"[MEDIUM] {medium_phrase}", signals)
        self.assertIn(f"[FLAG] {flag_phrase}", signals)
        # icloud locked also matches icloud lock so it might be >3 depending on lists, we just need to ensure the highest 3 are present.
        # So we assert True for those items being in signals, not necessarily length

if __name__ == "__main__":
    unittest.main()
