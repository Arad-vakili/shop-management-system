from .services import OrderService
from .models import Item
from .utils import validate_price, validate_quantity, get_valid_input, format_currency


class ShopManagementSystem:
    
    def __init__(self):
        self.order_service = OrderService()
    
    def run(self):
        while True:
            self.show_menu()
            choice = input("\nEnter your choice (1-7): ")
            
            if choice == '1':
                self.add_order()
            elif choice == '2':
                self.search_menu()
            elif choice == '3':
                self.edit_menu()
            elif choice == '4':
                self.remove_menu()
            elif choice == '5':
                self.list_all_orders()
            elif choice == '6':
                self.show_statistics()
            elif choice == '7':
                self.exit_system()
                break
            else:
                print("Invalid choice! Try again.")
    
    def show_menu(self):
        print("\n" + "="*50)
        print("ONLINE SHOP MANAGEMENT SYSTEM".center(50))
        print("="*50)
        print("1. Add New Order")
        print("2. Search Orders")
        print("3. Edit Order")
        print("4. Remove Order")
        print("5. List All Orders")
        print("6. Show Statistics")
        print("7. Exit")
        print("="*50)
    
    def add_order(self):
        print("\n--- Add New Order ---")
        username = input("Enter username: ")
        items = []
        
        while True:
            item_name = input("Item name (or 'done' to finish): ")
            if item_name.lower() == 'done':
                break
            
            try:
                price = get_valid_input("Price: ", validate_price)
                qty = get_valid_input("Quantity: ", validate_quantity)
                items.append(Item(name=item_name, price=price, qty=qty))
            except ValueError as e:
                print(f"Error: {e}")
                continue
        
        discount_code = input("Discount code (optional): ") or None
        country = input("Country (IR/US/UK): ") or "IR"
        
        order_id = self.order_service.create_order(username, items, discount_code, country)
        print(f"Order #{order_id} created successfully!")
        return order_id
    
    def search_menu(self):
        print("\n--- Search Menu ---")
        print("1. Search by Username")
        print("2. Search by Date")
        print("3. Search by Price Range")
        choice = input("Choose: ")
        
        results = []
        if choice == '1':
            username = input("Enter username: ")
            results = self.order_service.search_by_user(username)
        elif choice == '2':
            date = input("Enter date (YYYY-MM-DD): ")
            results = self.order_service.search_by_date(date)
        elif choice == '3':
            try:
                min_price = float(input("Min price: "))
                max_price = float(input("Max price: "))
                results = self.order_service.search_by_price_range(min_price, max_price)
            except ValueError:
                print("Invalid price!")
                return
        else:
            return
        
        self.display_search_results(results)
    
    def display_search_results(self, results):
        if not results:
            print("No orders found!")
            return
        
        print(f"\nFound {len(results)} order(s):")
        for oid, order in results:
            total = order.calculate_total()
            print(f"  Order #{oid}: {order.user} - {format_currency(total)} - {order.date[:19]}")
    
    def edit_menu(self):
        try:
            order_id = int(input("Enter order ID to edit: "))
            print("1. Edit Discount Code")
            print("2. Edit Country")
            choice = input("Choose: ")
            
            if choice == '1':
                new_discount = input("New discount code: ")
                self.order_service.update_discount(order_id, new_discount)
            elif choice == '2':
                new_country = input("New country (IR/US/UK): ")
                self.order_service.update_country(order_id, new_country)
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid order ID!")
    
    def remove_menu(self):
        print("1. Remove Single Order")
        print("2. Remove All Orders")
        choice = input("Choose: ")
        
        if choice == '1':
            try:
                order_id = int(input("Enter order ID: "))
                self.order_service.delete_order(order_id)
            except ValueError:
                print("Invalid ID!")
        elif choice == '2':
            confirm = input("Delete ALL orders? (yes/no): ")
            if confirm.lower() == 'yes':
                confirm_again = input("Are you absolutely sure? (yes/no): ")
                if confirm_again.lower() == 'yes':
                    self.order_service.delete_all_orders()
                else:
                    print("Cancelled!")
            else:
                print("Cancelled!")
    
    def list_all_orders(self):
        orders = self.order_service.list_all_orders()
        if not orders:
            print("No orders found!")
            return
        
        print("\n" + "="*80)
        print("ALL ORDERS LIST".center(80))
        print("="*80)
        print(f"{'ID':<5} {'User':<15} {'Final Price':<15} {'Date':<20} {'Country':<5} {'Items':<15}")
        print("-"*80)
        
        for order in orders:
            items_summary = ", ".join([f"{item.name}({item.qty})" for item in order.items[:2]])
            if len(order.items) > 2:
                items_summary += "..."
            
            print(
                f"{order.order_id:<5} {order.user:<15} "
                f"{format_currency(order.calculate_total()):<15} "
                f"{order.date[:19]:<20} "
                f"{order.country:<5} {items_summary:<15}"
            )
        print("="*80)
    
    def show_statistics(self):
        stats = self.order_service.get_statistics()
        
        if stats["total_orders"] == 0:
            print("No data available!")
            return
        
        print("\n" + "="*50)
        print("SYSTEM STATISTICS".center(50))
        print("="*50)
        print(f"Total Orders: {stats['total_orders']}")
        print(f"Total Sales: {format_currency(stats['total_sales'])}")
        print(f"Average Order Value: {format_currency(stats['avg_order'])}")
        print(f"Total Items Sold: {stats['total_items']}")
        if stats['top_customer']:
            print(f"Top Customer: {stats['top_customer']} ({format_currency(stats['top_customer_sales'])})")
        print("="*50)
    
    def exit_system(self):
        self.order_service.save_orders()
        print("Goodbye!")


def main():
    app = ShopManagementSystem()
    app.run()


if __name__ == "__main__":
    main()