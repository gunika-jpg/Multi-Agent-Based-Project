import re

def normalize_price(price):
    if price:
        price = re.sub(r"[^\d.]", "", str(price))
        return float(price)
    return 0.0


def format_currency(amount, symbol="₹"):
    """Format price with currency symbol."""
    return f"{symbol}{amount:,.2f}"

def deduplicate_products(products):
    """Remove duplicate products based on product name."""
    unique_products = []
    seen = set()

    for product in products:
        name = product["name"].strip().lower() if isinstance(product, dict) else product.name.strip().lower()
        if name not in seen:
            seen.add(name)
            unique_products.append(product)

    return unique_products
