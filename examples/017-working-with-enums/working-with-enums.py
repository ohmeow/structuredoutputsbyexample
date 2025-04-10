# Working with Enums
# Use enumerated types with Instructor for consistent, validated extractions. Enums help enforce a fixed set of allowed values.

# Import the necessary libraries
from enum import Enum
from pydantic import BaseModel
import instructor
from openai import OpenAI

# Define an enum for product categories
class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    HOME = "home"
    BOOKS = "books"
    TOYS = "toys"

# Define a Product model with Pydantic and enum validation
class Product(BaseModel):
    name: str
    price: float
    category: ProductCategory

# Patch the client
client = instructor.from_openai(OpenAI())

# Extract with enum validation
product = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=Product,
    messages=[
        {"role": "user", "content": "Our new wireless headphones cost $79.99 and belong in our electronics department."}
    ]
)

# Output:
# Product: Our new wireless headphones
# Price: $79.99
# Category: ProductCategory.ELECTRONICS
print(f"Product: {product.name}")
print(f"Price: ${product.price}")
print(f"Category: {product.category}")