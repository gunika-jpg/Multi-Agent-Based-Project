from groq import Groq
from utils.config import settings


class GroqService:

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)

    def generate_comparison_summary(self, products, budget):

        if not products:
            return "No products found."

        product_details = ""

        for product in products:
            product_details += (
                f"Name: {product.name}\n"
                f"Price: ₹{product.price}\n"
                f"Rating: {product.rating}\n"
                f"Source: {product.source}\n\n"
            )

        prompt = f"""
You are an AI Product Comparison Assistant.

Compare the following products based on:
- Price
- Rating
- Best value for money

User Budget: ₹{budget}

Products:

{product_details}

Give a short comparison and recommend the best product.
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    def generate_recommendation(self, recommended, alternatives):

        prompt = f"""
You are an AI Shopping Assistant.

Recommended Product:
Name: {recommended.name}
Price: ₹{recommended.price}
Rating: {recommended.rating}
Source: {recommended.source}

Alternative Products:
"""

        for product in alternatives:
            prompt += (
                f"- {product.name} | ₹{product.price} | "
                f"{product.rating}⭐ | {product.source}\n"
            )

        prompt += """

Explain:
1. Why this product is recommended.
2. Why it is better than the alternatives.
3. Whether it offers good value for money.

Keep the answer under 200 words.
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content