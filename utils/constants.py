"""Shared constants used across agents."""

# Default weighting for the Recommendation Agent's scoring formula.
# Values must sum to 100. UI (Streamlit sliders) can override these via
# state['weights'] — see utils.validators.validate_weights for safe handling.
DEFAULT_WEIGHTS = {
    "budget_fit": 30,   # reward staying within the user's budget
    "price": 25,        # reward lower absolute price
    "rating": 20,       # reward higher rating
    "reviews": 10,      # reward more reviews (social proof, log-scaled)
    "value": 15,         # reward high rating-per-rupee (from Comparison Agent)
}

RANK_LABELS = [
    "\U0001F947 Best Pick",   # 🥇
    "\U0001F948 Runner Up",   # 🥈
    "\U0001F949 Third Choice",  # 🥉
    "4th Choice",
    "5th Choice",
]

# How many top products to keep per source when diversifying recommendations,
# so the top-5 isn't dominated by five near-identical Amazon listings.
MAX_PER_SOURCE_IN_TOP5 = 3

# A price more than this many standard deviations from the mean is flagged
# as a potential outlier (scraping error, wrong product match, etc.)
OUTLIER_STD_THRESHOLD = 2.0
AMAZON_DOMAIN = "amazon.in"
MAX_PRODUCTS_PER_SOURCE = 10