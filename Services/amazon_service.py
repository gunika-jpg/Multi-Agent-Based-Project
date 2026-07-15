import requests
import time
from typing import List
from utils.config import get_settings
from utils.logger import setup_logger
from utils.validators import Product
from utils.helpers import normalize_price, normalize_rating
from utils.constants import MAX_PRODUCTS_PER_SOURCE, AMAZON_DOMAIN

class AmazonService:
    def __init__(self):
        self.settings = get_settings()
        self.logger = setup_logger('AmazonService')
        self.api_key = self.settings.SERPAPI_KEY

    def search(self, query: str) -> List[Product]:
        """Search Amazon using SerpAPI."""
        if not self.api_key:
            self.logger.warning("SERPAPI_KEY not found. Skipping Amazon search.")
            return []

        self.logger.info(f"Searching Amazon for: {query}")
        start_time = time.time()

        try:
            params = {
                "engine": "amazon",
                "api_key": self.api_key,
                "k": query,
                "amazon_domain": AMAZON_DOMAIN
            }

            response = requests.get('https://serpapi.com/search', params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            organic_results = data.get('organic_results', [])
            products = []

            for item in organic_results[:MAX_PRODUCTS_PER_SOURCE]:
                title = item.get('title', 'Unknown Product')

                price_val = 0.0
                price_data = item.get('price')
                if isinstance(price_data, dict):
                    price_val = price_data.get('value', 0.0)
                    if not price_val and 'raw' in price_data:
                        price_val = normalize_price(price_data['raw'])
                elif isinstance(price_data, (str, int, float)):
                    price_val = normalize_price(str(price_data))

                rating = normalize_rating(str(item.get('rating', 0)))

                reviews = item.get('reviews', 0)
                if isinstance(reviews, str):
                    try:
                        reviews = int(reviews.replace(',', ''))
                    except ValueError:
                        reviews = 0

                product = Product(
                    name=title,
                    price=price_val,
                    rating=rating,
                    reviews=reviews,
                    url=item.get('link', ''),
                    image_url=item.get('thumbnail', ''),
                    source='Amazon'
                )
                products.append(product)

            elapsed = time.time() - start_time
            self.logger.info(f"Found {len(products)} products on Amazon in {elapsed:.2f}s")
            return products

        except requests.RequestException as e:
            self.logger.error(f"Amazon API request failed: {e}")
        except Exception as e:
            self.logger.error(f"Error processing Amazon results: {e}", exc_info=True)

        return []