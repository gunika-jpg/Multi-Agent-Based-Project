from firecrawl import FirecrawlApp

from models.product import Product
from utils.config import settings
from utils.constants import MAX_PRODUCTS_PER_SOURCE
from utils.helpers import normalize_price


class FirecrawlService:

    STORES = {
        "Croma": "https://www.croma.com/searchB?q={query}",
        "Reliance Digital": "https://www.reliancedigital.in/search?q={query}"
    }

    def __init__(self):
        self.app = FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY)

    def search(self, query):

        products = []
        query = query.replace(" ", "%20")

        for store, url_template in self.STORES.items():

            url = url_template.format(query=query)

            try:
                result = self.app.scrape_url(
                    url,
                    {
                        "extractorOptions": {
                            "mode": "llm-extraction",
                            "extractionSchema": {
                                "type": "object",
                                "properties": {
                                    "products": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "name": {
                                                    "type": "string"
                                                },
                                                "price": {
                                                    "type": "string"
                                                },
                                                "rating": {
                                                    "type": "number"
                                                },
                                                "image_url": {
                                                    "type": "string"
                                                },
                                                "url": {
                                                    "type": "string"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                )

                if not result:
                    continue

                extracted = result.get("llm_extraction", {})
                product_list = extracted.get("products", [])

                for item in product_list[:MAX_PRODUCTS_PER_SOURCE]:

                    product = Product(
                        name=item.get("name", "Unknown Product"),
                        price=normalize_price(item.get("price", "")),
                        rating=float(item.get("rating", 0)),
                        seller=store,
                        source=store,
                        url=item.get("url", ""),
                        image_url=item.get("image_url", "")
                    )

                    products.append(product)

            except Exception:
                continue

        return products