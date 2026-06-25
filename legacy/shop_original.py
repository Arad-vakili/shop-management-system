import datetime
import json
import os

users_db = {}
orders_db = {}
discount_codes = {"SAVE10": 10, "OFF5": 5, "BLACK20": 20}
ORDERS_FILE = "orders_data.txt"


def load_orders_from_file():
    global orders_db
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                orders_db = {int(k): v for k, v in data.items()}
            print(f"Loaded {len(orders_db)} orders from file.")
        except (json.JSONDecodeError, FileNotFoundError):
            print("No valid order data found. Starting with empty orders.")
            orders_db = {}
    else:
        print("No orders file found. Starting with empty orders.")
        orders_db = {}


def save_orders_to_file():
    try:
        with open(ORDERS_FILE, 'w', encoding='utf-8') as file:
            json.dump(orders_db, file, indent=2, ensure_ascii=False)
        print(f"Orders saved to {ORDERS_FILE}")
        return True
    except Exception as e:
        print(f"Error saving orders: {e}")
        return False


def save_order(username, items, discount_code, country="IR"):
    total = sum(item["price"] * item["qty"] for item in items)
    if discount_code and discount_code in discount_codes:
        total = total * (100 - discount_codes[discount_code]) / 100
    tax_rates = {"IR": 0.09, "US": 0.07, "UK": 0.20}
    tax = total * tax_rates.get(country, 0.1)
    final = total + tax
    
    if orders_db:
        order_id = max(orders_db.keys()) + 1
    else:
        order_id = 1
    
    orders_db[order_id] = {
        "user": username, "items": items, "total_before_tax": total,
        "tax": tax, "final": final, "date": str(datetime.datetime.now()),
        "discount_code": discount_code, "country": country
    }
    
    save_orders_to_file()
    print(f"Order {order_id} saved successfully!")
    return order_id


def search_orders_by_user(username):
    return [(oid, order) for oid, order in orders_db.items() if order['user'].lower() == username.lower()]


def search_orders_by_date(search_date):
    return [(oid, order) for oid, order in orders_db.items() if search_date in order['date']]


def search_orders_by_price_range(min_price, max_price):
    return [(oid, order) for oid, order in orders_db.items() if min_price <= order['final'] <= max_price]


def remove_order(order_id):
    if order_id in orders_db:
        removed = orders_db.pop(order_id)
        save_orders_to_file()
        print(f"Order {order_id} for user {removed['user']} removed successfully!")
        return True
    print(f"Order {order_id} not found!")
    return False


def remove_all_orders():
    count = len(orders_db)
    orders_db.clear()
    save_orders_to_file()
    print(f"All {count} orders removed successfully!")
    return count


def edit_order_discount(order_id, new_discount_code):
    if order_id not in orders_db:
        print(f"Order {order_id} not found!")
        return False
    
    order = orders_db[order_id]
    old_discount = order['discount_code']
    order['discount_code'] = new_discount_code
    
    subtotal = sum(item['price'] * item['qty'] for item in order['items'])
    discount_percent = discount_codes.get(new_discount_code, 0)
    if discount_percent:
        subtotal = subtotal * (100 - discount_percent) / 100
    
    tax_rates = {"IR": 0.09, "US": 0.07, "UK": 0.20}
    tax = subtotal * tax_rates.get(order['country'], 0.1)
    order['total_before_tax'] = subtotal
    order['tax'] = tax
    order['final'] = subtotal + tax
    order['date'] = str(datetime.datetime.now())
    
    save_orders_to_file()
    print(f"Order {order_id} updated: discount {old_discount} -> {new_discount_code}")
    return True


def edit_order_country(order_id, new_country):
    if order_id not in orders_db:
        print(f"Order {order_id} not found!")
        return False
    
    order = orders_db[order_id]
    old_country = order['country']
    order['country'] = new_country
    
    subtotal = sum(item['price'] * item['qty'] for item in order['items'])
    discount_percent = discount_codes.get(order['discount_code'], 0)
    if discount_percent:
        subtotal = subtotal * (100 - discount_percent) / 100
    
    tax_rates = {"IR": 0.09, "US": 0.07, "UK": 0.20}
    tax = subtotal * tax_rates.get(new_country, 0.1)
    order['total_before_tax'] = subtotal
    order['tax'] = tax
    order['final'] = subtotal + tax
    order['date'] = str(datetime.datetime.now())
    
    save_orders_to_file()
    print(f"Order {order_id} updated: country {old_country} -> {new_country}")
    return True


def add_order_interactive():
    print("\n--- Add New Order ---")
    username = input("Enter username: ")
    items = []
    
    while True:
        item_name = input("Item name (or 'done' to finish): ")
        if item_name.lower() == 'done':
            break
        try:
            price = float(input("Price: "))
            qty = int(input("Quantity: "))
            items.append({"name": item_name, "price": price, "qty": qty})
        except ValueError:
            print("Invalid input! Try again.")
    
    discount_code = input("Discount code (optional): ") or None
    country = input("Country (IR/US/UK): ") or "IR"
    
    if username not in users_db:
        users_db[username] = "guest123"
        print(f"User {username} not found! Creating as guest...")
    
    return save_order(username, items, discount_code, country)


def list_all_orders():
    if not orders_db:
        print("No orders found!")
        return
    
    print("\n" + "="*80)
    print("ALL ORDERS LIST".center(80))
    print("="*80)
    print(f"{'ID':<5} {'User':<15} {'Final Price':<15} {'Date':<20} {'Country':<5} {'Items':<15}")
    print("-"*80)
    for oid, order in orders_db.items():
        items_summary = ", ".join([f"{item['name']}({item['qty']})" for item in order['items'][:2]])
        if len(order['items']) > 2:
            items_summary += "..."
        print(
            f"{oid:<5} {order['user']:<15} ${order['final']:<14.2f} {order['date'][:19]:<20} {order['country']:<5} {items_summary:<15}")
    print("="*80)
    
    if os.path.exists(ORDERS_FILE):
        file_size = os.path.getsize(ORDERS_FILE)
        print(f"Data stored in: {ORDERS_FILE} ({file_size} bytes)")


def get_statistics():
    if not orders_db:
        print("No data available!")
        return
    
    total_orders = len(orders_db)
    total_sales = sum(order['final'] for order in orders_db.values())
    avg_order_value = total_sales / total_orders
    
    user_sales = {}
    for order in orders_db.values():
        user_sales[order['user']] = user_sales.get(order['user'], 0) + order['final']
    top_user = max(user_sales, key=user_sales.get) if user_sales else None
    
    total_items = 0
    for order in orders_db.values():
        total_items += sum(item['qty'] for item in order['items'])
    
    print("\n" + "="*50)
    print("SYSTEM STATISTICS".center(50))
    print("="*50)
    print(f"Total Orders: {total_orders}")
    print(f"Total Sales: ${total_sales:.2f}")
    print(f"Average Order Value: ${avg_order_value:.2f}")
    print(f"Total Items Sold: {total_items}")
    print(f"Top Customer: {top_user} (${user_sales.get(top_user, 0):.2f})")
    print("="*50)


def show_menu():
    print("\n" + "="*50)
    print("ONLINE SHOP MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add New Order")
    print("2. Search Orders")
    print("3. Edit Order")
    print("4. Remove Order")
    print("5. List All Orders")
    print("6. Show Statistics")
    print("7. Exit")
    print("="*50)


def search_menu():
    print("\n--- Search Menu ---")
    print("1. Search by Username")
    print("2. Search by Date")
    print("3. Search by Price Range")
    choice = input("Choose: ")
    
    if choice == '1':
        username = input("Enter username: ")
        results = search_orders_by_user(username)
    elif choice == '2':
        date = input("Enter date (YYYY-MM-DD): ")
        results = search_orders_by_date(date)
    elif choice == '3':
        try:
            min_price = float(input("Min price: "))
            max_price = float(input("Max price: "))
            results = search_orders_by_price_range(min_price, max_price)
        except ValueError:
            print("Invalid price!")
            return
    else:
        return
    
    if results:
        print(f"\nFound {len(results)} order(s):")
        for oid, order in results:
            print(f"  Order #{oid}: {order['user']} - ${order['final']:.2f} - {order['date'][:19]}")
    else:
        print("No orders found!")


def edit_menu():
    try:
        order_id = int(input("Enter order ID to edit: "))
        print("1. Edit Discount Code")
        print("2. Edit Country")
        choice = input("Choose: ")
        
        if choice == '1':
            new_discount = input("New discount code: ")
            edit_order_discount(order_id, new_discount)
        elif choice == '2':
            new_country = input("New country (IR/US/UK): ")
            edit_order_country(order_id, new_country)
        else:
            print("Invalid choice!")
    except ValueError:
        print("Invalid order ID!")


def remove_menu():
    print("1. Remove Single Order")
    print("2. Remove All Orders")
    choice = input("Choose: ")
    
    if choice == '1':
        try:
            order_id = int(input("Enter order ID: "))
            remove_order(order_id)
        except ValueError:
            print("Invalid ID!")
    elif choice == '2':
        confirm = input("Delete ALL orders? (yes/no): ")
        if confirm.lower() == 'yes':
            confirm_again = input("Are you absolutely sure? (yes/no): ")
            if confirm_again.lower() == 'yes':
                remove_all_orders()
            else:
                print("Cancelled!")
        else:
            print("Cancelled!")


def main():
    load_orders_from_file()
    
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            add_order_interactive()
        elif choice == '2':
            search_menu()
        elif choice == '3':
            edit_menu()
        elif choice == '4':
            remove_menu()
        elif choice == '5':
            list_all_orders()
        elif choice == '6':
            get_statistics()
        elif choice == '7':
            save_orders_to_file()
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()