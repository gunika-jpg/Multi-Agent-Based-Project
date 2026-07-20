APP_NAME = "Smart Product Price Comparison Assistant"
CACHE_TTL = 900  # 15 minutes
MAX_PRODUCTS_PER_SOURCE = 10

SUPPORTED_SOURCES = [
    "Amazon",
    "Flipkart",
    "Other"
]

DEFAULT_BUDGET_MIN = 0
DEFAULT_BUDGET_MAX = 500000


DEFAULT_CURRENCY = "₹"

AGENT_NAMES = [
    'Search Agent', 
    'Comparison Agent', 
    'Recommendation Agent', 
    'Response Agent'
]