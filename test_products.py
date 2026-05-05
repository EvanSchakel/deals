import unittest
from products import PRODUCTS, SCAM_HIGH, SCAM_MEDIUM, SCAM_FLAGS

class TestProductsSchema(unittest.TestCase):
    def test_products_schema(self):
        """Validates that all items in PRODUCTS have the required keys and types."""
        required_keys = ['retail', 'good', 'great', 'tags', 'upgrades']
        optional_keys = {
            'ram_gate': (int, type(None)),
            'require_512': bool,
            'insane_only': bool,
            'note': str
        }

        for product_name, data in PRODUCTS.items():
            with self.subTest(product=product_name):
                # Check for required keys
                for key in required_keys:
                    self.assertIn(key, data, f"Missing required key '{key}'")

                # Check required key types
                self.assertIsInstance(data['retail'], (int, float), "retail must be a number")
                self.assertTrue(data['retail'] > 0, "retail must be positive")
                self.assertIsInstance(data['good'], (int, float), "good must be a number")
                self.assertIsInstance(data['great'], (int, float), "great must be a number")
                self.assertIsInstance(data['tags'], list, "tags must be a list")
                self.assertTrue(all(isinstance(t, str) for t in data['tags']), "all tags must be strings")
                self.assertIsInstance(data['upgrades'], list, "upgrades must be a list")
                self.assertTrue(all(isinstance(u, str) for u in data['upgrades']), "all upgrades must be strings")

                # Check optional keys
                for key, expected_type in optional_keys.items():
                    if key in data:
                        self.assertIsInstance(data[key], expected_type, f"{key} must be of type {expected_type}")

    def test_scam_lists(self):
        """Validates that scam signal lists contain only strings."""
        for name, lst in [("SCAM_HIGH", SCAM_HIGH), ("SCAM_MEDIUM", SCAM_MEDIUM), ("SCAM_FLAGS", SCAM_FLAGS)]:
            with self.subTest(list_name=name):
                self.assertIsInstance(lst, list, f"{name} must be a list")
                self.assertTrue(all(isinstance(i, str) for i in lst), f"all elements in {name} must be strings")

if __name__ == '__main__':
    unittest.main()
