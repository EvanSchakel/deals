import unittest
from deal_analyzer import evaluate_price, apply_condition_modifiers, apply_scam_modifiers

class TestDealAnalyzerRefactoring(unittest.TestCase):
    def test_evaluate_price(self):
        product = {"great": 0.78, "good": 0.84}
        score, verdict = evaluate_price(0.75, product)
        self.assertEqual(score, 9)

        score, verdict = evaluate_price(0.80, product)
        self.assertEqual(score, 7)

        score, verdict = evaluate_price(0.90, product)
        self.assertEqual(score, 5)

        score, verdict = evaluate_price(1.0, product)
        self.assertEqual(score, 3)

        score, verdict = evaluate_price(1.1, product)
        self.assertEqual(score, 1)

    def test_apply_condition_modifiers(self):
        notes = []
        score = apply_condition_modifiers("New", 5, notes)
        self.assertEqual(score, 6)
        self.assertIn("Condition bonus: new/open-box (+1)", notes)

        notes = []
        score = apply_condition_modifiers("Fair", 5, notes)
        self.assertEqual(score, 3)
        self.assertIn("Condition penalty: fair/acceptable (-2)", notes)

        notes = []
        score = apply_condition_modifiers("Good", 5, notes)
        self.assertEqual(score, 5)
        self.assertEqual(len(notes), 0)

    def test_apply_scam_modifiers(self):
        warnings = []
        score, verdict = apply_scam_modifiers("high", 8, "Original verdict", warnings)
        self.assertEqual(score, 2)
        self.assertEqual(verdict, "⚠️  SCAM WARNING — do not proceed.")
        self.assertEqual(len(warnings), 1)

        warnings = []
        score, verdict = apply_scam_modifiers("medium", 8, "Original verdict", warnings)
        self.assertEqual(score, 6)
        self.assertEqual(verdict, "Original verdict")
        self.assertEqual(len(warnings), 1)

        warnings = []
        score, verdict = apply_scam_modifiers("low", 8, "Original verdict", warnings)
        self.assertEqual(score, 7)
        self.assertEqual(verdict, "Original verdict")
        self.assertEqual(len(warnings), 1)

if __name__ == '__main__':
    unittest.main()
