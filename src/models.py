import datetime
from dataclasses import dataclass, field


@dataclass
class Item:
    name: str
    price: float
    qty: int
    
    def subtotal(self):
        return self.price * self.qty


@dataclass
class Order:
    order_id: int
    user: str
    items: list
    country: str = "IR"
    discount_code: str = None
    date: str = field(default_factory=lambda: str(datetime.datetime.now()))
    
    TAX_RATES = {"IR": 0.09, "US": 0.07, "UK": 0.20}
    DISCOUNT_CODES = {"SAVE10": 10, "OFF5": 5, "BLACK20": 20}
    
    def calculate_total(self):
        subtotal = sum(item.subtotal() for item in self.items)
        
        if self.discount_code and self.discount_code in self.DISCOUNT_CODES:
            discount = self.DISCOUNT_CODES[self.discount_code]
            subtotal = subtotal * (100 - discount) / 100
        
        tax_rate = self.TAX_RATES.get(self.country, 0.1)
        tax = subtotal * tax_rate
        
        return subtotal + tax
    
    def calculate_tax(self):
        subtotal = sum(item.subtotal() for item in self.items)
        if self.discount_code and self.discount_code in self.DISCOUNT_CODES:
            discount = self.DISCOUNT_CODES[self.discount_code]
            subtotal = subtotal * (100 - discount) / 100
        tax_rate = self.TAX_RATES.get(self.country, 0.1)
        return subtotal * tax_rate
    
    def calculate_subtotal(self):
        subtotal = sum(item.subtotal() for item in self.items)
        if self.discount_code and self.discount_code in self.DISCOUNT_CODES:
            discount = self.DISCOUNT_CODES[self.discount_code]
            subtotal = subtotal * (100 - discount) / 100
        return subtotal
    
    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user": self.user,
            "items": [{"name": i.name, "price": i.price, "qty": i.qty} for i in self.items],
            "country": self.country,
            "discount_code": self.discount_code,
            "date": self.date,
            "total": self.calculate_total(),
            "subtotal": self.calculate_subtotal(),
            "tax": self.calculate_tax()
        }
    
    @classmethod
    def from_dict(cls, data):
        items = [Item(**item) for item in data.get("items", [])]
        return cls(
            order_id=data["order_id"],
            user=data["user"],
            items=items,
            country=data.get("country", "IR"),
            discount_code=data.get("discount_code"),
            date=data.get("date", str(datetime.datetime.now()))
        )


@dataclass
class User:
    username: str
    password: str = "guest123"
    orders: list = field(default_factory=list)
    
    def add_order(self, order_id):
        if order_id not in self.orders:
            self.orders.append(order_id)