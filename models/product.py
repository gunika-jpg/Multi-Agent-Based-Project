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