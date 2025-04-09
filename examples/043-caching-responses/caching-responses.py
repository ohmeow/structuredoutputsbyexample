# Caching Responses

# Implement caching strategies for LLM responses with Instructor. Supports Redis caching for distributed systems and performance optimization.

# Caching LLM responses can significantly improve performance and reduce costs. Instructor supports several caching strategies to suit different needs.
import functools
import instructor
from openai import OpenAI
from pydantic import BaseModel

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a simple model
class User(BaseModel):
    name: str
    age: int

# Simple in-memory caching with functools.cache
@functools.cache
def extract_user(text: str) -> User:
    """Extract user information with in-memory caching."""
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=User,
        messages=[
            {
                "role": "user",
                "content": f"Extract user information from: {text}"
            }
        ]
    )

# Example usage
user1 = extract_user("John is 30 years old")
print(user1)

# This call will use the cached result (no API call)
user2 = extract_user("John is 30 years old")
print(user2)

# For persistent caching across sessions, you can use disk-based caching:
import functools
import inspect
import instructor
import diskcache
from openai import OpenAI
from pydantic import BaseModel

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Initialize disk cache
cache = diskcache.Cache('./my_cache_directory')

# Define a caching decorator for Pydantic models
def instructor_cache(func):
    """Cache a function that returns a Pydantic model."""
    return_type = inspect.signature(func).return_annotation
    if not issubclass(return_type, BaseModel):
        raise ValueError("The return type must be a Pydantic model")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a cache key from the function name and arguments
        key = f"{func.__name__}-{functools._make_key(args, kwargs, typed=False)}"

        # Check if result is already cached
        if (cached := cache.get(key)) is not None:
            # Deserialize from JSON based on the return type
            return return_type.model_validate_json(cached)

        # Call the function and cache its result
        result = func(*args, **kwargs)
        serialized_result = result.model_dump_json()
        cache.set(key, serialized_result)

        return result

    return wrapper

# Define a model
class Product(BaseModel):
    name: str
    price: float
    category: str

# Use the caching decorator
@instructor_cache
def extract_product(text: str) -> Product:
    """Extract product information with disk caching."""
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=Product,
        messages=[
            {
                "role": "user",
                "content": f"Extract product information from: {text}"
            }
        ]
    )

# Example usage
product = extract_product("iPhone 14 Pro costs $999 and is in the smartphones category")
print(product)

# For distributed systems, Redis caching is a great option:
import redis
import functools
import inspect
import instructor
from openai import OpenAI
from pydantic import BaseModel

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Initialize Redis cache
cache = redis.Redis(host="localhost", port=6379, db=0)

# Define a caching decorator for Redis
def redis_cache(func):
    """Cache a function that returns a Pydantic model using Redis."""
    return_type = inspect.signature(func).return_annotation
    if not issubclass(return_type, BaseModel):
        raise ValueError("The return type must be a Pydantic model")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a cache key from the function name and arguments
        key = f"{func.__name__}-{functools._make_key(args, kwargs, typed=False)}"

        # Check if result is already cached
        if (cached := cache.get(key)) is not None:
            # Deserialize from JSON based on the return type
            return return_type.model_validate_json(cached)

        # Call the function and cache its result
        result = func(*args, **kwargs)
        serialized_result = result.model_dump_json()
        cache.set(key, serialized_result)

        return result

    return wrapper

