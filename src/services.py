import json
import os
from datetime import datetime
from .models import Order, Item, User


class OrderService:
    
    def __init__(self, data_file="data/orders_data.txt"):
        self.data_file = data_file
        self.orders = {}
        self.users = {}
        data_dir = os.path.dirname(self.data_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
        self.load_orders()
    
    def load_orders(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for order_id, order_data in data.items():
                        self.orders[int(order_id)] = Order.from_dict(order_data)
                print(f"Loaded {len(self.orders)} orders from file.")
            except (json.JSONDecodeError, FileNotFoundError):
                print("No valid order data found. Starting with empty orders.")
                self.orders = {}
        else:
            print("No orders file found. Starting with empty orders.")
            self.orders = {}
    
    def save_orders(self):
        try:
            data_dir = os.path.dirname(self.data_file)
            if data_dir and not os.path.exists(data_dir):
                os.makedirs(data_dir, exist_ok=True)
            data = {str(oid): order.to_dict() for oid, order in self.orders.items()}
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            print(f"Orders saved to {self.data_file}")
            return True
        except Exception as e:
            print(f"Error saving orders: {e}")
            return False
    
    def create_order(self, user, items, discount_code=None, country="IR"):
        order_id = max(self.orders.keys()) + 1 if self.orders else 1
        
        order = Order(
            order_id=order_id,
            user=user,
            items=items,
            country=country,
            discount_code=discount_code
        )
        
        self.orders[order_id] = order
        
        if user not in self.users:
            self.users[user] = User(username=user)
        self.users[user].add_order(order_id)
        
        self.save_orders()
        print(f"Order {order_id} created successfully!")
        return order_id
    
    def get_order(self, order_id):
        return self.orders.get(order_id)
    
    def search_by_user(self, username):
        return [(oid, order) for oid, order in self.orders.items() 
                if order.user.lower() == username.lower()]
    
    def search_by_date(self, date_str):
        return [(oid, order) for oid, order in self.orders.items() 
                if date_str in order.date]
    
    def search_by_price_range(self, min_price, max_price):
        return [(oid, order) for oid, order in self.orders.items() 
                if min_price <= order.calculate_total() <= max_price]
    
    def delete_order(self, order_id):
        if order_id in self.orders:
            removed = self.orders.pop(order_id)
            self.save_orders()
            print(f"Order {order_id} for user {removed.user} removed successfully!")
            return True
        print(f"Order {order_id} not found!")
        return False
    
    def delete_all_orders(self):
        count = len(self.orders)
        self.orders.clear()
        self.save_orders()
        print(f"All {count} orders removed successfully!")
        return count
    
    def update_discount(self, order_id, new_discount):
        order = self.get_order(order_id)
        if not order:
            print(f"Order {order_id} not found!")
            return False
        
        old_discount = order.discount_code
        order.discount_code = new_discount
        order.date = str(datetime.now())
        self.save_orders()
        print(f"Order {order_id} updated: discount {old_discount} -> {new_discount}")
        return True
    
    def update_country(self, order_id, new_country):
        order = self.get_order(order_id)
        if not order:
            print(f"Order {order_id} not found!")
            return False
        
        old_country = order.country
        order.country = new_country
        order.date = str(datetime.now())
        self.save_orders()
        print(f"Order {order_id} updated: country {old_country} -> {new_country}")
        return True
    
    def get_statistics(self):
        if not self.orders:
            return {"total_orders": 0, "total_sales": 0, "avg_order": 0, 
                    "total_items": 0, "top_customer": None}
        
        total_orders = len(self.orders)
        totals = [order.calculate_total() for order in self.orders.values()]
        total_sales = sum(totals)
        avg_order = total_sales / total_orders
        
        customer_sales = {}
        for order in self.orders.values():
            customer_sales[order.user] = customer_sales.get(order.user, 0) + order.calculate_total()
        top_customer = max(customer_sales, key=customer_sales.get) if customer_sales else None
        
        total_items = sum(sum(item.qty for item in order.items) for order in self.orders.values())
        
        return {
            "total_orders": total_orders,
            "total_sales": total_sales,
            "avg_order": avg_order,
            "total_items": total_items,
            "top_customer": top_customer,
            "top_customer_sales": customer_sales.get(top_customer, 0) if top_customer else 0
        }
    
    def list_all_orders(self):
        return [self.orders[oid] for oid in sorted(self.orders.keys())]