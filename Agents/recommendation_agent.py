from models.product import Product


def recommendation_agent(state):

    products: list[Product] = state.get("products", [])
    budget = state.get("budget", 0)

    if not products:
        return {
            "recommendations": []
        }

    max_price = max(product.price for product in products)

    recommendations = []

    for product in products:

        score = 0

        # Budget Score
        if budget > 0:
            if product.price <= budget:
                score += 30

        # Price Score
        if max_price > 0:
            score += (1 - (product.price / max_price)) * 30

        # Rating Score
        score += (product.rating / 5) * 40

        product.recommendation_score = round(score, 2)

        recommendations.append(product)

    recommendations.sort(
        key=lambda product: product.recommendation_score,
        reverse=True
    )

    return {
        "recommendations": recommendations[:5]
    }