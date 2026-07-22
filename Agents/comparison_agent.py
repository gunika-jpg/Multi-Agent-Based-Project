from models.product import Product


def calculate_value_score(price, rating, max_price):
    if max_price == 0:
        return 0.0
    return round((1 - (price / max_price)) * 50 + (rating / 5) * 50, 2)


def comparison_agent(state):
    products = state.get("products", [])
    if not products:
        return {"comparison_data": {}}

    cheapest = min(products, key=lambda p: p.price)
    highest_rated = max(products, key=lambda p: p.rating)
    max_price = max(p.price for p in products)

    # Add value_score to each Product object
    for p in products:
        p.value_score = calculate_value_score(
            p.price,
            p.rating,
            max_price
        )

    best_value = max(products, key=lambda p: p.value_score)

    by_source = {}
    for p in products:
        by_source.setdefault(p.source, []).append(p)

    return {
        "comparison_data": {
            "products": products,
            "cheapest": cheapest,
            "highest_rated": highest_rated,
            "best_value": best_value,
            "by_source": by_source,
        }
    }