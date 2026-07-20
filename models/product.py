<<<<<<< HEAD
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: float
    rating: float
    seller: str
    source: str
    url: str
    image_url: str = ""
    
    value_score: float = 0.0
    recommendation_score: float = 0.0
=======
"""
Compatibility shim.

Services/flipkart_service.py and Services/firecrawl_service.py import
`Product` from `models.product`, but the single source of truth for the
schema actually lives in `utils/validators.py` (see that file's docstring).
This module just re-exports it so those two files import successfully
without needing to touch their code.
"""
from utils.validators import Product  # noqa: F401

>>>>>>> 87781e54869ecb82d7616c3ef400468d33171105
