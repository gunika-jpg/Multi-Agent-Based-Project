import asyncio
from playwright.async_api import async_playwright

from models.product import Product
from utils.constants import MAX_PRODUCTS_PER_SOURCE
from utils.helpers import normalize_price


class FlipkartService:

    async def _scrape_products(self, query):

        products = []

        async with async_playwright() as p:

            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            url = f"https://www.flipkart.com/search?q={query}"

            await page.goto(url)

            # Close login popup (if it appears)
            try:
                await page.click("button._2KpZ6l._2doB4z", timeout=3000)
            except:
                pass

            await page.wait_for_timeout(3000)

            items = await page.query_selector_all("div[data-id]")

            for item in items[:MAX_PRODUCTS_PER_SOURCE]:

                try:
                    name = await item.query_selector("div.KzDlHZ")
                    price = await item.query_selector("div.Nx9bqj")
                    rating = await item.query_selector("div.XQDdHH")
                    link = await item.query_selector("a.CGtC98")
                    image = await item.query_selector("img")

                    product = Product(
                        name=await name.inner_text() if name else "Unknown Product",
                        price=normalize_price(await price.inner_text()) if price else 0.0,
                        rating=float(await rating.inner_text()) if rating else 0.0,
                        seller="Flipkart",
                        source="Flipkart",
                        url="https://www.flipkart.com" + await link.get_attribute("href") if link else "",
                        image_url=await image.get_attribute("src") if image else ""
                    )

                    products.append(product)

                except:
                    continue

            await browser.close()

        return products

    def search(self, query):
        return asyncio.run(self._scrape_products(query))