import unittest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import validate_price, validate_quantity, validate_country, format_currency, get_valid_input


class TestUtils(unittest.TestCase):
    def test_validate_price_valid(self):
        self.assertEqual(validate_price("10.50"), 10.50)
        self.assertEqual(validate_price("0"), 0.0)
        self.assertEqual(validate_price("99.99"), 99.99)
    
    def test_validate_price_invalid(self):
        with self.assertRaises(ValueError):
            validate_price("abc")
        with self.assertRaises(ValueError):
            validate_price("-5")
    
    def test_validate_quantity_valid(self):
        self.assertEqual(validate_quantity("5"), 5)
        self.assertEqual(validate_quantity("0"), 0)
        self.assertEqual(validate_quantity("100"), 100)
    
    def test_validate_quantity_invalid(self):
        with self.assertRaises(ValueError):
            validate_quantity("abc")
        with self.assertRaises(ValueError):
            validate_quantity("-3")
        with self.assertRaises(ValueError):
            validate_quantity("2.5")
    
    def test_validate_country(self):
        self.assertTrue(validate_country("IR"))
        self.assertTrue(validate_country("US"))
        self.assertTrue(validate_country("UK"))
        self.assertFalse(validate_country("DE"))
        self.assertFalse(validate_country("FR"))
    
    def test_format_currency(self):
        self.assertEqual(format_currency(10.5), "$10.50")
        self.assertEqual(format_currency(1000.00), "$1000.00")
        self.assertEqual(format_currency(0.99), "$0.99")
    
    @patch('builtins.input', return_value="10.50")
    def test_get_valid_input(self, mock_input):
        result = get_valid_input("Enter price: ", validate_price)
        self.assertEqual(result, 10.50)
    
    @patch('builtins.input', side_effect=["abc", "10.50"])
    def test_get_valid_input_retry(self, mock_input):
        result = get_valid_input("Enter price: ", validate_price)
        self.assertEqual(result, 10.50)


if __name__ == "__main__":
    unittest.main()