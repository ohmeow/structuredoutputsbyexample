# Vision Inputs
# Learn how to process and extract structured data from images with Instructor. This guide demonstrates unified handling of vision inputs across different providers.
# Multimodal models enable extraction of structured data from images, but handling image inputs can be complex with different requirements across providers.
# Instructor simplifies vision inputs with a unified Image class that automatically manages format details for each provider.

# Import necessary libraries
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a model for image analysis
class ImageContent(BaseModel):
    description: str = Field(description="A detailed description of the image")
    objects: List[str] = Field(description="List of main objects in the image")
    colors: List[str] = Field(description="Dominant colors in the image")

# Method 1: Creating an Image object from a file path
def analyze_image_from_file(file_path: str) -> ImageContent:
    """Load and analyze an image from a local file path."""
    image = instructor.Image.from_path(file_path)

    return client.chat.completions.create(
        model="gpt-4-vision-preview",
        response_model=ImageContent,
        messages=[
            {
                "role": "user",
                "content": [
                    "Describe this image in detail:",
                    image  # The Image object is handled automatically
                ]
            }
        ]
    )

# Method 2: Creating an Image object from a URL
def analyze_image_from_url(image_url: str) -> ImageContent:
    """Load and analyze an image from a URL."""
    image = instructor.Image.from_url(image_url)

    return client.chat.completions.create(
        model="gpt-4-vision-preview",
        response_model=ImageContent,
        messages=[
            {
                "role": "user",
                "content": [
                    "Describe this image in detail:",
                    image
                ]
            }
        ]
    )

# Method 3: Using autodetect_images for convenience
def analyze_with_autodetect(image_path_or_url: str) -> ImageContent:
    """Automatically detect and analyze an image from a path or URL."""
    return client.chat.completions.create(
        model="gpt-4-vision-preview",
        response_model=ImageContent,
        messages=[
            {
                "role": "user",
                "content": [
                    "Describe this image in detail:",
                    image_path_or_url  # Will be automatically detected as an image
                ]
            }
        ],
        autodetect_images=True  # Automatically converts paths/URLs to Image objects
    )

# Example usage with more structured outputs
class ProductDetails(BaseModel):
    """Model for extracting specific product details from product images."""
    product_name: str = Field(description="The name or title of the product")
    brand: str = Field(description="The brand of the product")
    category: str = Field(description="Product category (e.g., electronics, clothing)")
    key_features: List[str] = Field(description="Main features or selling points")
    target_audience: str = Field(description="Who this product is primarily designed for")

def extract_product_info(image_path_or_url: str) -> ProductDetails:
    """Extract structured product information from a product image."""
    return client.chat.completions.create(
        model="gpt-4-vision-preview",
        response_model=ProductDetails,
        messages=[
            {
                "role": "system",
                "content": "Extract detailed product information from the provided image"
            },
            {
                "role": "user",
                "content": [
                    "What product is shown in this image? Extract key details:",
                    image_path_or_url
                ]
            }
        ],
        autodetect_images=True
    )

# Example usage
if __name__ == "__main__":
    # Example with a sample image URL (replace with a valid image URL for testing)
    sample_url = "https://example.com/image.jpg"
    
    # Basic image analysis
    result = analyze_with_autodetect(sample_url)
    print("Basic Image Analysis:")
    print(f"Description: {result.description}")
    print(f"Objects: {', '.join(result.objects)}")
    print(f"Colors: {', '.join(result.colors)}")
    
    # Product-specific extraction
    # product_info = extract_product_info(sample_url)
    # print("\nProduct Information Extraction:")
    # print(f"Product: {product_info.product_name}")
    # print(f"Brand: {product_info.brand}")
    # print(f"Category: {product_info.category}")
    # print(f"Key Features: {', '.join(product_info.key_features)}")
    # print(f"Target Audience: {product_info.target_audience}")

