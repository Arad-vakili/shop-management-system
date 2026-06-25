import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services import OrderService
from src.models import Item


class TestOrderService(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_orders.txt"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.service = OrderService(self.test_file)
        self.items = [Item("Book", 50, 2), Item("Pen", 2, 5)]
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists("data") and not os.listdir("data"):
            os.rmdir("data")
    
    def test_create_order(self):
        order_id = self.service.create_order("alice", self.items, "SAVE10", "US")
        self.assertEqual(order_id, 1)
        self.assertEqual(len(self.service.orders), 1)
    
    def test_get_order(self):
        order_id = self.service.create_order("bob", self.items)
        order = self.service.get_order(order_id)
        self.assertIsNotNone(order)
        self.assertEqual(order.user, "bob")
        self.assertEqual(len(order.items), 2)
    
    def test_search_by_user(self):
        self.service.create_order("alice", [Item("Book", 10, 1)])
        self.service.create_order("bob", [Item("Pen", 5, 2)])
        self.service.create_order("alice", [Item("Paper", 3, 10)])
        
        results = self.service.search_by_user("alice")
        self.assertEqual(len(results), 2)
        self.assertTrue(all(order.user == "alice" for _, order in results))
    
    def test_search_by_date(self):
        order_id = self.service.create_order("test", [Item("Book", 10, 1)])
        order = self.service.get_order(order_id)
        date_str = order.date[:10]
        
        results = self.service.search_by_date(date_str)
        self.assertEqual(len(results), 1)
    
    def test_search_by_price_range(self):
        self.service.create_order("user1", [Item("Cheap", 10, 1)])
        self.service.create_order("user2", [Item("Medium", 50, 2)])
        self.service.create_order("user3", [Item("Expensive", 100, 3)])
        
        results = self.service.search_by_price_range(90, 150)
        self.assertEqual(len(results), 1)
    
    def test_delete_order(self):
        order_id = self.service.create_order("test", self.items)
        self.assertEqual(len(self.service.orders), 1)
        
        result = self.service.delete_order(order_id)
        self.assertTrue(result)
        self.assertEqual(len(self.service.orders), 0)
    
    def test_delete_nonexistent_order(self):
        result = self.service.delete_order(999)
        self.assertFalse(result)
    
    def test_delete_all_orders(self):
        self.service.create_order("user1", self.items)
        self.service.create_order("user2", self.items)
        
        count = self.service.delete_all_orders()
        self.assertEqual(count, 2)
        self.assertEqual(len(self.service.orders), 0)
    
    def test_update_discount(self):
        order_id = self.service.create_order("test", self.items, "SAVE10", "US")
        
        result = self.service.update_discount(order_id, "OFF5")
        self.assertTrue(result)
        
        updated = self.service.get_order(order_id)
        self.assertEqual(updated.discount_code, "OFF5")
    
    def test_update_country(self):
        order_id = self.service.create_order("test", self.items, "SAVE10", "US")
        
        result = self.service.update_country(order_id, "UK")
        self.assertTrue(result)
        
        updated = self.service.get_order(order_id)
        self.assertEqual(updated.country, "UK")
    
    def test_get_statistics(self):
        self.service.create_order("alice", [Item("Book", 10, 2)], "SAVE10", "US")
        self.service.create_order("bob", [Item("Pen", 5, 3)], "OFF5", "IR")
        self.service.create_order("alice", [Item("Paper", 2, 10)], None, "UK")
        
        stats = self.service.get_statistics()
        self.assertEqual(stats["total_orders"], 3)
        self.assertGreater(stats["total_sales"], 0)
        self.assertEqual(stats["top_customer"], "alice")
    
    def test_list_all_orders(self):
        self.service.create_order("alice", self.items)
        self.service.create_order("bob", self.items)
        
        orders = self.service.list_all_orders()
        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0].user, "alice")
        self.assertEqual(orders[1].user, "bob")
    
    def test_persistence(self):
        order_id = self.service.create_order("persist_test", self.items, "SAVE10", "US")
        self.service.save_orders()
        
        new_service = OrderService(self.test_file)
        self.assertEqual(len(new_service.orders), 1)
        
        loaded_order = new_service.get_order(order_id)
        self.assertIsNotNone(loaded_order)
        self.assertEqual(loaded_order.user, "persist_test")
        self.assertEqual(loaded_order.discount_code, "SAVE10")


if __name__ == "__main__":
    unittest.main()