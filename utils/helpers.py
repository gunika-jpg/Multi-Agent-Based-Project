"""Shared helper functions. calculate_value_score is required by both the
Comparison and Recommendation agents.
"""

import statistics
import re 
def normalize_price(price) -> float:
    """Strip currency symbols/commas from a raw scraped price and return a float."""
    if price:
        cleaned = re.sub(r"[^\d.]", "", str(price))
        return float(cleaned) if cleaned else 0.0
    return 0.0


def normalize_rating(rating) -> float:
    """Parse a raw scraped rating to a clamped 0-5 float."""
    if not rating or rating == "None":
        return 0.0
    try:
        match = re.search(r"\d+(\.\d+)?", str(rating))
        if match:
            return max(0.0, min(5.0, float(match.group())))
        return 0.0
    except (ValueError, TypeError):
        return 0.0
    
def calculate_value_score(price: float, rating: float, max_price: float) -> float:
    """Score 0-100 based on price (lower is better) and rating (higher is better)."""
    if price <= 0 or rating <= 0:
        return 0.0

    rating_score = (rating / 5.0) * 50

    price_score = 0.0
    if max_price > 0:
        price_score = (1 - price / max_price) * 50

    return max(0.0, min(100.0, rating_score + price_score))


def format_currency(amount: float, symbol: str = "\u20b9") -> str:
    """Format amount with commas and 2 decimal places. Default symbol is Rupee."""
    return f"{symbol}{amount:,.2f}"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text with ellipsis if it exceeds max_length."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def brand_matches(product_brand: str, brand_filter: str) -> bool:
    """Case-insensitive substring match for brand filtering.

    Empty brand_filter always matches (no filter applied).
    Falls back to checking the product name if `brand` field is empty,
    since some scraped sources may not reliably populate `brand`.
    """
    if not brand_filter:
        return True
    return brand_filter.strip().lower() in (product_brand or "").strip().lower()


def detect_price_outliers(products: list, std_threshold: float = 2.0) -> list:
    """Return the list of product dicts whose price is more than
    `std_threshold` standard deviations from the mean price.

    Useful for flagging likely scraping errors (e.g. a $9 "iPhone 15").
    Requires at least 3 priced products to compute a meaningful std dev.
    """
    priced = [p for p in products if p.get("price", 0) > 0]
    if len(priced) < 3:
        return []

    prices = [p["price"] for p in priced]
    mean_price = statistics.mean(prices)
    try:
        std_price = statistics.stdev(prices)
    except statistics.StatisticsError:
        return []

    if std_price == 0:
        return []

    outliers = [
        p for p in priced
        if abs(p["price"] - mean_price) > std_threshold * std_price
    ]
    return outliers
