# Vision

# - Providing automatic detection of image paths and URLs

# Instructor provides simple, unified handling of vision inputs across different LLM providers through its `Image` class, which automatically handles the details of image formatting for each provider.
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

# Creating an Image object from a file path
def analyze_image_from_file(file_path: str) -> ImageContent:
    # Load the image using Instructor's Image class
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

# Creating an Image object from a URL
def analyze_image_from_url(image_url: str) -> ImageContent:
    # Load the image from a URL
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

# Using autodetect_images for convenience
def analyze_with_autodetect(image_path_or_url: str) -> ImageContent:
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

# Example usage
result = analyze_with_autodetect("https://example.com/image.jpg")
print(f"Description: {result.description}")
print(f"Objects: {', '.join(result.objects)}")
print(f"Colors: {', '.join(result.colors)}")

