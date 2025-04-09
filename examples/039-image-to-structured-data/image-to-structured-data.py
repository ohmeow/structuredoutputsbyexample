# Image Extraction

# - Integration with downstream processing pipelines

# Instructor excels at transforming images into structured data, combining vision capabilities with Pydantic models for reliable extraction.
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a structured data model for product information
class Product(BaseModel):
    name: str = Field(description="Product name")
    price: float = Field(description="Product price in USD")
    description: str = Field(description="Brief product description")
    features: List[str] = Field(description="Key product features")
    brand: Optional[str] = Field(None, description="Brand name if visible")

# Extract product information from an image
def extract_product_info(image_path_or_url: str) -> Product:
    return client.chat.completions.create(
        model="gpt-4-vision-preview",
        response_model=Product,
        messages=[
            {
                "role": "user",
                "content": [
                    "Extract detailed product information from this image:",
                    image_path_or_url
                ]
            }
        ],
        autodetect_images=True  # Automatically handle the image
    )

# Example usage
product = extract_product_info("path/to/product_image.jpg")
print(f"Product: {product.name} (${product.price:.2f})")
print(f"Description: {product.description}")
print(f"Features: {', '.join(product.features)}")
if product.brand:
    print(f"Brand: {product.brand}")

# You can extract more complex data structures from images:
from typing import List, Optional
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a recipe structure
class Ingredient(BaseModel):
    name: str = Field(description="Ingredient name")
    quantity: str = Field(description="Amount needed, including units")
    optional: bool = Field(description="Whether this ingredient is optional")

class Step(BaseModel):
    instruction: str = Field(description="Cooking instruction")
    time_minutes: Optional[int] = Field(None, description="Time required for this step in minutes")

class Recipe(BaseModel):
    title: str = Field(description="Recipe title")
    servings: int = Field(description="Number of servings")
    prep_time_minutes: int = Field(description="Preparation time in minutes")
    cook_time_minutes: int = Field(description="Cooking time in minutes")
    ingredients: List[Ingredient] = Field(description="List of ingredients")
    steps: List[Step] = Field(description="Cooking steps in order")
    difficulty: str = Field(description="Recipe difficulty (easy, medium, hard)")

# Extract recipe from an image
def extract_recipe(image_path: str) -> Recipe:
    # Create an Image object
    image = instructor.Image.from_path(image_path)

    return client.chat.completions.create(
        model="gpt-4-vision-preview",
        response_model=Recipe,
        messages=[
            {
                "role": "system",
                "content": "Extract complete recipe information from the provided image."
            },
            {
                "role": "user",
                "content": [
                    "Please extract the detailed recipe information from this image:",
                    image
                ]
            }
        ]
    )

# The function would be used like this:
# recipe = extract_recipe("path/to/recipe_card.jpg")

