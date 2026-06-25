import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Item, Order, User


class TestItem(unittest.TestCase):
    def test_item_creation(self):
        item = Item("Laptop", 999.99, 2)
        self.assertEqual(item.name, "Laptop")
        self.assertEqual(item.price, 999.99)
        self.assertEqual(item.qty, 2)

    def test_item_subtotal(self):
        item = Item("Phone", 500, 3)
        self.assertEqual(item.subtotal(), 1500)


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.items = [Item("Laptop", 1000, 1), Item("Mouse", 20, 2)]
        self.order = Order(
            order_id=1,
            user="testuser",
            items=self.items,
            country="US",
            discount_code="SAVE10"
        )

    def test_order_calculation_no_discount(self):
        order = Order(1, "test", [Item("Book", 50, 2)], "IR")
        self.assertEqual(order.calculate_subtotal(), 100)
        self.assertAlmostEqual(order.calculate_tax(), 9, places=2)
        self.assertAlmostEqual(order.calculate_total(), 109, places=2)

    def test_order_calculation_with_discount(self):
        order = Order(2, "test", [Item("Book", 50, 2)], "IR", "SAVE10")
        self.assertEqual(order.calculate_subtotal(), 90)
        self.assertAlmostEqual(order.calculate_tax(), 8.1, places=2)
        self.assertAlmostEqual(order.calculate_total(), 98.1, places=2)

    def test_order_to_dict(self):
        order_dict = self.order.to_dict()
        self.assertEqual(order_dict["order_id"], 1)
        self.assertEqual(order_dict["user"], "testuser")
        self.assertEqual(len(order_dict["items"]), 2)
        self.assertEqual(order_dict["discount_code"], "SAVE10")

    def test_order_from_dict(self):
        data = {
            "order_id": 3,
            "user": "john",
            "items": [{"name": "Pen", "price": 1.5, "qty": 4}],
            "country": "UK",
            "discount_code": "OFF5",
            "date": "2024-01-01 12:00:00"
        }
        order = Order.from_dict(data)
        self.assertEqual(order.order_id, 3)
        self.assertEqual(order.user, "john")
        self.assertEqual(len(order.items), 1)
        self.assertEqual(order.country, "UK")

    def test_different_country_tax(self):
        order_us = Order(1, "test", [Item("Book", 100, 1)], "US")
        self.assertAlmostEqual(order_us.calculate_tax(), 7, places=2)
        
        order_uk = Order(2, "test", [Item("Book", 100, 1)], "UK")
        self.assertAlmostEqual(order_uk.calculate_tax(), 20, places=2)
        
        order_unknown = Order(3, "test", [Item("Book", 100, 1)], "DE")
        self.assertAlmostEqual(order_unknown.calculate_tax(), 10, places=2)

    def tearDown(self):
        pass


class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User("alice")
        self.assertEqual(user.username, "alice")
        self.assertEqual(user.password, "guest123")
        self.assertEqual(user.orders, [])

    def test_user_add_order(self):
        user = User("bob")
        user.add_order(1)
        user.add_order(2)
        self.assertEqual(len(user.orders), 2)
        self.assertIn(1, user.orders)
        self.assertIn(2, user.orders)

    def test_user_prevent_duplicate_orders(self):
        user = User("charlie")
        user.add_order(1)
        user.add_order(1)
        self.assertEqual(len(user.orders), 1)


if __name__ == "__main__":
    unittest.main()