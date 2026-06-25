# 🛒 Shop Management System

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-100%25-brightgreen.svg)](tests/)
[![Code Quality](https://img.shields.io/badge/code%20quality-A+-brightgreen.svg)](src/)

> A Python shop management system demonstrating the power of refactoring - from monolithic spaghetti code to clean, object-oriented design with 100% test coverage.

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [📂 Project Structure](#-project-structure)
- [🚀 Installation](#-installation)
- [💻 Usage](#-usage)
- [🧪 Testing](#-testing)
- [📊 Before vs After Refactoring](#-before-vs-after-refactoring)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📝 **Order Management** | Create, read, update, and delete orders |
| 🏷️ **Discount System** | Apply discount codes (SAVE10, OFF5, BLACK20) |
| 💰 **Tax Calculation** | Country-specific tax rates (IR: 9%, US: 7%, UK: 20%) |
| 🔍 **Search Capabilities** | Search by username, date, or price range |
| 📊 **Statistics** | View total sales, average order value, top customers |
| 💾 **Data Persistence** | JSON file storage for orders |
| 🧪 **100% Test Coverage** | Comprehensive unit tests for all components |

---

## 📂 Project Structure

```
shop-management-system/
│
├── 📁 src/                          # ✅ REFACTORED: Clean OOP code
│   ├── 📄 __init__.py              # Package initialization
│   ├── 📄 models.py                # Data models (Item, Order, User)
│   ├── 📄 services.py              # Business logic (OrderService)
│   ├── 📄 utils.py                 # Helper functions (validation)
│   └── 📄 main.py                  # Application UI
│
├── 📁 legacy/                       # ❌ ORIGINAL: Monolithic code
│   └── 📄 shop_original.py         # Original spaghetti code
│
├── 📁 tests/                        # ✅ Unit tests (35+ tests)
│   ├── 📄 __init__.py
│   ├── 📄 test_models.py           # Test data models
│   ├── 📄 test_services.py         # Test business logic
│   └── 📄 test_utils.py            # Test utilities
│
├── 📁 data/                         # Data storage
│   └── 📄 orders_data.txt          # JSON data
│
├── 📄 README.md                     # This file
├── 📄 LICENSE                       # MIT License
├── 📄 .gitignore                    # Git ignore rules
├── 📄 requirements.txt              # Dependencies
└── 📄 setup.py                      # Package setup
```

---

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- Git (optional)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/Arad-vakili/shop-management-system.git
cd shop-management-system

# No external dependencies needed - uses Python standard library only
```

---

## 💻 Usage

### Run the Refactored Version (Recommended)
```bash
python -m src.main
```

### Run the Original Version (For Comparison)
```bash
python legacy/shop_original.py
```

### Interactive Session Example
```
==================================================
        ONLINE SHOP MANAGEMENT SYSTEM
==================================================
1. Add New Order
2. Search Orders
3. Edit Order
4. Remove Order
5. List All Orders
6. Show Statistics
7. Exit
==================================================

Enter your choice (1-7): 1

--- Add New Order ---
Enter username: john_doe
Item name (or 'done' to finish): Laptop
Price: 999.99
Quantity: 1
Item name (or 'done' to finish): Mouse
Price: 29.99
Quantity: 2
Item name (or 'done' to finish): done
Discount code (optional): SAVE10
Country (IR/US/UK): US
Order 1 created successfully!
```

### Programmatic Usage
```python
from src.services import OrderService
from src.models import Item

# Initialize service
service = OrderService()

# Create order
items = [Item("Laptop", 999.99, 1)]
order_id = service.create_order("john_doe", items, "SAVE10", "US")

# Search orders
results = service.search_by_user("john_doe")

# Get statistics
stats = service.get_statistics()
print(f"Total Sales: ${stats['total_sales']:.2f}")
```

---

## 🧪 Testing

### Run All Tests
```bash
python -m unittest discover tests -v
```

### Run Specific Test Files
```bash
python -m tests.test_models
python -m tests.test_services
python -m tests.test_utils
```

### Test Results
```
✅ test_models.py - 12 tests passing
✅ test_services.py - 14 tests passing  
✅ test_utils.py - 9 tests passing
✅ TOTAL: 35 tests, 100% coverage
```

---

## 📊 Before vs After Refactoring

### Code Quality Metrics

| Metric | Original (legacy/) | Refactored (src/) | Improvement |
|--------|-------------------|-------------------|-------------|
| **Lines of Code** | ~400 | ~350 | -12% |
| **Functions/Methods** | 12 functions | 20+ methods | +66% |
| **Global Variables** | 5 | 0 | -100% |
| **Classes** | 0 | 4 | +100% |
| **Test Coverage** | 0% | 100% | +100% |

### What Was Improved

**❌ Before (Monolithic):**
- Global variables everywhere
- One function does everything (calculation, saving, UI)
- No test coverage
- Hard to maintain
- Poor error handling

**✅ After (Refactored):**
- Clean OOP design
- Separation of concerns (models, services, utils)
- 100% test coverage
- Easy to maintain and extend
- Robust error handling

### Code Example Comparison

**❌ BEFORE (Original):**
```python
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
    return order_id
```

**✅ AFTER (Refactored):**
```python
@dataclass
class Order:
    order_id: int
    user: str
    items: List[Item]
    country: str = "IR"
    discount_code: Optional[str] = None
    
    TAX_RATES = {"IR": 0.09, "US": 0.07, "UK": 0.20}
    DISCOUNT_CODES = {"SAVE10": 10, "OFF5": 5, "BLACK20": 20}
    
    def calculate_total(self):
        return self.calculate_subtotal() + self.calculate_tax()
    
    def calculate_subtotal(self):
        subtotal = sum(item.subtotal() for item in self.items)
        if self.discount_code and self.discount_code in self.DISCOUNT_CODES:
            discount = self.DISCOUNT_CODES[self.discount_code]
            subtotal = subtotal * (100 - discount) / 100
        return subtotal
    
    def calculate_tax(self):
        tax_rate = self.TAX_RATES.get(self.country, 0.1)
        return self.calculate_subtotal() * tax_rate
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute

- 🐛 **Report bugs** - Open an issue describing the problem
- 💡 **Suggest features** - Open an issue with your idea
- 📝 **Improve documentation** - Fix typos or add examples
- 🔧 **Submit code changes** - Fix bugs or add features

### Development Setup

```bash
# Fork the repository
# Clone your fork
git clone https://github.com/yourusername/shop-management-system.git
cd shop-management-system

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run tests to ensure everything works
python -m unittest discover tests -v
```

### How to Submit Changes

1. **Fork** the repository
2. **Create a branch** for your feature
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
   - Follow PEP 8 style guide
   - Write tests for new features
   - Update documentation
4. **Run tests** to make sure everything passes
   ```bash
   python -m unittest discover tests -v
   ```
5. **Commit** with a clear message
   ```bash
   git commit -m "Add: Amazing new feature"
   ```
6. **Push** to your fork
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request** on GitHub

### Guidelines

| Type | Guidelines |
|------|-----------|
| **Code** | PEP 8 compliant, well-documented, tested |
| **Tests** | Cover all new functionality |
| **Docs** | Update README if needed |
| **Commits** | Clear, descriptive messages |
| **PRs** | Explain what and why |

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

This project demonstrates the **power of refactoring** and serves as a learning resource for:
- Clean Code principles
- Object-Oriented Programming
- Test-Driven Development
- Software Design Patterns

---

**⭐ Star this repository if you find the before/after comparison useful!**

---

*Built with ❤️ to help developers learn the art of refactoring*

**Remember:** The best code is code that's easy to read, easy to test, and easy to change. This project shows you exactly how to get there! 🚀
