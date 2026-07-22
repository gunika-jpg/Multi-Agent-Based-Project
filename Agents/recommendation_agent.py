from models.product import Product


def recommendation_agent(state):
    products = state.get("products", [])
    budget = state.get("budget", 0)

    if not products:
        return {"recommendations": []}

    max_price = max(p.price for p in products)

    for p in products:
        score = 0

        if budget > 0 and p.price <= budget:
            score += 30

        if max_price > 0:
            score += (1 - (p.price / max_price)) * 30

        score += (p.rating / 5) * 40

        p.recommendation_score = round(score, 2)

    products.sort(key=lambda p: p.recommendation_score, reverse=True)

    return {"recommendations": products[:5]}