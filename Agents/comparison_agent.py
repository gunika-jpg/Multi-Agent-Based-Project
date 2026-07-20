from models.product import Product
from utils.helpers import calculate_value_score


def comparison_agent(state):

    products: list[Product] = state.get("products", [])

    if not products:
        return {
            "comparison_data": {}
        }

    # Find cheapest product
    cheapest = min(products, key=lambda product: product.price)

    # Find highest rated product
    highest_rated = max(products, key=lambda product: product.rating)

    # Calculate value score
    max_price = max(product.price for product in products)

    for product in products:
        product.value_score = calculate_value_score(
            product.price,
            product.rating,
            max_price
        )

    # Find best value product
    best_value = max(products, key=lambda product: product.value_score)

    comparison_data = {
        "products": products,
        "cheapest": cheapest,
        "highest_rated": highest_rated,
        "best_value": best_value
    }

    return {
        "comparison_data": comparison_data
    }