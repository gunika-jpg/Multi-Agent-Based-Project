<<<<<<< HEAD
from Services.amazon_service import AmazonService
from Services.flipkart_service import FlipkartService
from Services.firecrawl_service import FirecrawlService
from utils.helpers import deduplicate_products


def search_agent(state):

    query = state["query"]

    amazon = AmazonService()
    flipkart = FlipkartService()
    firecrawl = FirecrawlService()

    products = []

    # Search Amazon
    try:
        products.extend(amazon.search(query))
    except:
        print("Amazon search failed")

    # Search Flipkart
    try:
        products.extend(flipkart.search(query))
    except:
        print("Flipkart search failed")

    # Search Other Stores
    try:
        products.extend(firecrawl.search(query))
    except:
        print("Other store search failed")

    # Remove duplicate products
    products = deduplicate_products(products)

    return {
        "products": products
    }
=======
"""
Search Agent — Member 1

Responsibility: query Amazon (SerpAPI), Flipkart (Playwright), and Firecrawl
(Croma / Reliance Digital) for the user's query, normalize every result to a
plain dict matching the Product schema in utils/validators.py, merge them
all into one list, and write it to state["products"] for the Comparison
Agent to consume.

Input state keys read:
    query : str

Output state keys written:
    products     : List[Dict]
    agent_status : Dict
    errors       : List[str]

If every live source fails or returns nothing (e.g. no API keys configured
yet), falls back to frontend.helpers.generate_mock_products so the rest of
the pipeline (Comparison -> Recommendation -> Response) can still be
demoed/tested end to end.
"""
from typing import Any, Dict, List

from utils.logger import setup_logger
from Services.amazon_service import AmazonService
from Services.flipkart_service import FlipkartService
from Services.firecrawl_service import FirecrawlService

logger = setup_logger("SearchAgent")


def _to_dicts(products: List[Any]) -> List[Dict]:
    """Normalize a list of Product (pydantic) objects OR plain dicts into dicts."""
    out = []
    for p in products:
        if hasattr(p, "model_dump"):
            out.append(p.model_dump())
        elif isinstance(p, dict):
            out.append(p)
    return out


def search_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    query = state.get("query", "")
    agent_status = state.get("agent_status", {}).copy()
    agent_status["search"] = "running"
    errors = state.get("errors", []).copy()

    logger.info(f"Search Agent started for query: '{query}'")

    all_products: List[Dict] = []

    # --- Amazon (SerpAPI) ---
    try:
        amazon_products = AmazonService().search(query)
        all_products.extend(_to_dicts(amazon_products))
        logger.info(f"Amazon returned {len(amazon_products)} products")
    except Exception as e:
        logger.error(f"Amazon search failed: {e}")
        errors.append(f"Amazon search failed: {e}")

    # --- Flipkart (Playwright scrape) ---
    try:
        flipkart_products = FlipkartService().search(query)
        all_products.extend(_to_dicts(flipkart_products))
        logger.info(f"Flipkart returned {len(flipkart_products)} products")
    except Exception as e:
        logger.error(f"Flipkart search failed: {e}")
        errors.append(f"Flipkart search failed: {e}")

    # --- Firecrawl (Croma / Reliance Digital) ---
    try:
        firecrawl_products = FirecrawlService().search(query)
        all_products.extend(_to_dicts(firecrawl_products))
        logger.info(f"Firecrawl returned {len(firecrawl_products)} products")
    except Exception as e:
        logger.error(f"Firecrawl search failed: {e}")
        errors.append(f"Firecrawl search failed: {e}")

    # --- Fallback so the pipeline is always demoable ---
    if not all_products:
        logger.warning("No live results from any source — falling back to mock data")
        from frontend.helpers import generate_mock_products
        all_products = generate_mock_products(query)
        errors.append("Live sources returned nothing (check API keys) — showing sample data.")

    agent_status["search"] = "completed"

    return {
        "products": all_products,
        "agent_status": agent_status,
        "errors": errors,
    }
>>>>>>> 87781e54869ecb82d7616c3ef400468d33171105
