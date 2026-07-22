import requests

from models.product import Product
from utils.config import get_settings


class AmazonService:

    def search(self, query):
        """Search Amazon products using SerpAPI."""

        # ---------------- Validate Query ----------------
        if not query or not str(query).strip():
            print("AmazonService: Empty search query received.")
            return []

        url = "https://serpapi.com/search"

        params = {
            "engine": "amazon",
            "k": query.strip(),
            "amazon_domain": "amazon.in",
            "api_key": get_settings().SERPAPI_KEY
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=15,
            )

            response.raise_for_status()

            data = response.json()

            products = []

            for item in data.get("organic_results", [])[:10]:

                price = 0.0

                if isinstance(item.get("price"), dict):
                    price = float(item["price"].get("value", 0))
                else:
                    try:
                        price = float(
                            str(item.get("price", 0))
                            .replace("₹", "")
                            .replace(",", "")
                        )
                    except (ValueError, TypeError):
                        price = 0.0

                # ---------------- Product ----------------

                product = Product(
                    name=item.get("title", "N/A"),
                    price=price,
                    rating=float(item.get("rating", 0) or 0),
                    reviews=int(item.get("reviews", 0) or 0),
                    delivery_info=", ".join(item.get("delivery", [])) if isinstance(item.get("delivery"), list) else (item.get("delivery", "") or ""),
                    seller=item.get("seller", "Amazon"),
                    image_url=item.get("thumbnail", ""),
                    url=item.get("link", ""),
                    source="Amazon",
                )

                products.append(product)

            return products

        except requests.exceptions.HTTPError as e:
            print(f"Amazon HTTP Error: {e}")
            return []

        except requests.exceptions.RequestException as e:
            print(f"Amazon Request Error: {e}")
            return []

        except Exception as e:
            print(f"Amazon Unexpected Error: {e}")
            return []