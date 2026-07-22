from Services.amazon_service import AmazonService
from Services.flipkart_service import FlipkartService
from Services.firecrawl_service import FirecrawlService


def deduplicate_products(products):
    """Remove duplicate products based on product name."""
    unique_products = []
    seen = set()

    for product in products:
        name = str(product.get("name", "")).strip().lower()

        if name and name not in seen:
            seen.add(name)
            unique_products.append(product)

    return unique_products


def search_agent_node(state):

    query = state.get("query", "")
    errors = state.get("errors", []).copy()

    amazon = AmazonService()
    flipkart = FlipkartService()
    firecrawl = FirecrawlService()

    products = []

    # Amazon Search
    try:
        products.extend(amazon.search(query))
    except Exception as e:
        errors.append(f"Amazon search failed: {e}")

    # Flipkart Search
    try:
        print("Calling Flipkart...")
        products.extend(flipkart.search(query))
    except Exception as e:
        print("Flipkart Error:", e)
        errors.append(f"Flipkart search failed: {e}")

    # Other Stores Search
    try:
        products.extend(firecrawl.search(query))
    except Exception as e:
        errors.append(f"Other store search failed: {e}")

    # Remove duplicate products
    products = deduplicate_products(products)

    return {
        "products": products,
        "errors": errors,
    }