def validate_price(price):
    try:
        value = float(price)
        if value < 0:
            raise ValueError("Price cannot be negative")
        return value
    except ValueError:
        raise ValueError("Invalid price format")
    
def validate_quantity(qty):
    try:
        value = int(qty)
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        return value
    except ValueError:
        raise ValueError("Invalid quantity format")

def validate_country(country):
    valid_countries = ["IR", "US", "UK"]
    return country.upper() in valid_countries

def format_currency(amount):
    return f"${amount:.2f}"

def get_valid_input(prompt, validator, error_msg="Invalid input!"):
    while True:
        try:
            value = input(prompt)
            return validator(value)
        except ValueError as e:
            print(f"{error_msg} {e}")