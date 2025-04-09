# Handling Stream Errors

# When working with streaming responses, validation errors can occur when the LLM generates invalid data.
# Instructor provides several ways to handle these errors and recover gracefully.

# First, let's import the necessary libraries
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI
from typing import List, Optional

# Define a Person model with validation constraints
class Person(BaseModel):
    name: str
    age: int = Field(gt=0, lt=150)  # Age validation constraint: must be between 1-149
    occupation: str

# Patch the OpenAI client with Instructor
client = instructor.from_openai(OpenAI())

# Basic error handling for a streaming response
def stream_with_error_handling():
    try:
        # Create a partial stream - we intentionally ask for an invalid age (200 years)
        # to demonstrate error handling
        person_stream = client.chat.completions.create_partial(
            model="gpt-3.5-turbo",
            response_model=Person,
            messages=[
                {"role": "user", "content": "Generate a profile for a fictional person who is 200 years old."}
            ]
        )

        # Process the stream and show progress
        for partial_person in person_stream:
            # Display each partial state as it arrives
            print(f"Current state: {partial_person}")

        # This line will only execute if no exception is raised
        print("\nFinal result:", partial_person)

    except Exception as e:
        # Catch and handle any errors that occur during streaming
        print(f"\nError occurred: {type(e).__name__}: {str(e)}")
        print("Handling the error gracefully...")

# Run the function to see the error handling in action
stream_with_error_handling()

# Expected output will show progress until validation fails:
# Current state: name=None age=None occupation=None
# Current state: name='Elizabeth' age=None occupation=None
# Current state: name='Elizabeth Morgan' age=None occupation=None
# Current state: name='Elizabeth Morgan' age=200 occupation=None
#
# Error occurred: ValidationError: 1 validation error for Person
# age
#   Input should be less than 150 [type=less_than, input_value=200, input_type=int]

from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List, Any

class Product(BaseModel):
    name: str
    price: float = Field(gt=0)  # Must be positive
    quantity: int = Field(ge=0)  # Must be non-negative
    category: str

def safe_stream_processing():
    # Create a partial stream
    try:
        product_stream = client.chat.completions.create_partial(
            model="gpt-3.5-turbo",
            response_model=Product,
            messages=[
                {"role": "user", "content": "Generate a product with negative price."},
            ]
        )

        # Try to process the stream
        last_valid_state = None

        try:
            for partial_product in product_stream:
                print(f"Processing: {partial_product}")
                last_valid_state = partial_product
        except ValidationError as e:
            print(f"\nValidation failed: {e}\n")

            if last_valid_state:
                print(f"Last valid state before error: {last_valid_state}")

                # You could attempt recovery here
                corrected_product = Product(
                    name=last_valid_state.name or "Unknown Product",
                    price=abs(last_valid_state.price) if last_valid_state.price is not None else 9.99,
                    quantity=last_valid_state.quantity or 0,
                    category=last_valid_state.category or "Uncategorized"
                )

                print(f"\nRecovered with corrected data: {corrected_product}")
            else:
                print("No valid state was received before the error")

    except Exception as outer_e:
        print(f"Outer exception: {outer_e}")

# Run the function
safe_stream_processing()

from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List, Dict, Union, Any

class StockData(BaseModel):
    symbol: str
    price: float = Field(gt=0)
    volume: int = Field(gt=0)
    change_percent: float

# Define a function to safely extract data with validation
def safe_extract_from_chunk(chunk_data: Dict[str, Any], model_class) -> Optional[Any]:
    try:
        # Try to create a model instance from the chunk data
        return model_class.model_validate(chunk_data)
    except ValidationError:
        # Return None if validation fails
        return None

# Process a stream with manual validation
def stream_with_manual_validation():
    # Create a stream - note we're not using response_model here
    # to handle the validation ourselves
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        stream=True,  # Enable streaming
        messages=[
            {"role": "user", "content": "Generate stock data for ACME Corp with possible errors."}
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "stock_data",
                    "description": "Return stock data",
                    "parameters": StockData.model_json_schema()
                }
            }
        ],
        tool_choice={"type": "function", "function": {"name": "stock_data"}}
    )

    # Process the stream
    combined_data = {}
    invalid_chunks = []

    for chunk in stream:
        if hasattr(chunk, 'choices') and chunk.choices and hasattr(chunk.choices[0], 'delta'):
            delta = chunk.choices[0].delta

            # Extract any tool calls data
            if hasattr(delta, 'tool_calls') and delta.tool_calls:
                for tool_call in delta.tool_calls:
                    if hasattr(tool_call, 'function') and tool_call.function:
                        if hasattr(tool_call.function, 'arguments') and tool_call.function.arguments:
                            # Try to parse JSON
                            try:
                                import json
                                json_str = tool_call.function.arguments
                                data = json.loads(json_str)

                                # Update our combined data
                                combined_data.update(data)

                                # Try to validate the current state
                                result = safe_extract_from_chunk(combined_data, StockData)

                                if result:
                                    print(f"Valid partial data: {result}")
                                else:
                                    print(f"Current data invalid: {combined_data}")
                                    invalid_chunks.append(combined_data.copy())
                            except json.JSONDecodeError:
                                print(f"Invalid JSON: {tool_call.function.arguments}")

    # Final validation
    try:
        final_result = StockData.model_validate(combined_data)
        print(f"\nFinal valid result: {final_result}")
    except ValidationError as e:
        print(f"\nFinal validation failed: {e}")
        print("Invalid states encountered:", invalid_chunks)

        # Attempt recovery
        corrected_data = combined_data.copy()
        if 'price' in corrected_data and corrected_data['price'] <= 0:
            corrected_data['price'] = abs(corrected_data['price']) or 10.0
        if 'volume' in corrected_data and corrected_data['volume'] <= 0:
            corrected_data['volume'] = abs(corrected_data['volume']) or 1000

        try:
            recovered = StockData.model_validate(corrected_data)
            print(f"Recovered result: {recovered}")
        except ValidationError:
            print("Could not recover valid data")

# Run the function
stream_with_manual_validation()

from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List, Any, Union

# Define nested models with validation
class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str = Field(min_length=5)  # Validation that might fail

class Person(BaseModel):
    name: str
    age: int = Field(gt=0, lt=150)
    address: Address

# Define fallback models with fewer constraints
class SimpleAddress(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

class SimplePerson(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[SimpleAddress] = None

# Function to handle streaming with fallbacks
def stream_with_fallbacks():
    # Create a partial stream
    person_stream = client.chat.completions.create_partial(
        model="gpt-3.5-turbo",
        response_model=Person,
        max_retries=1,  # Limit retries
        messages=[
            {"role": "user", "content": "Generate a person with an invalid postal code."}
        ]
    )

    # Try to process with primary model
    primary_stream_failed = False
    try:
        for partial_person in person_stream:
            print(f"Primary model state: {partial_person}")
    except ValidationError as e:
        print(f"\nValidation error in primary model: {str(e)}\n")
        primary_stream_failed = True

    # If primary fails, try with the fallback model
    if primary_stream_failed:
        print("Falling back to simplified model...")

        # Create a new stream with the fallback model
        fallback_stream = client.chat.completions.create_partial(
            model="gpt-3.5-turbo",
            response_model=SimplePerson,
            messages=[
                {"role": "user", "content": "Generate a person with an invalid postal code."}
            ]
        )

        try:
            # Process with fallback model
            for partial_person in fallback_stream:
                print(f"Fallback model state: {partial_person}")

            print("\nCompleted with fallback model")
        except Exception as fallback_error:
            print(f"Even fallback model failed: {str(fallback_error)}")

# Run the function
stream_with_fallbacks()

from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List, Any

class Review(BaseModel):
    product_id: str
    rating: int = Field(ge=1, le=5)
    comment: str
    reviewer_name: str

# Function to handle errors in both partial and iterable streams
def robust_stream_processing():
    print("1. Testing partial stream with validation errors:\n")

    try:
        # Create a partial stream that might have validation errors
        review_stream = client.chat.completions.create_partial(
            model="gpt-3.5-turbo",
            response_model=Review,
            messages=[
                {"role": "user", "content": "Generate a product review with a rating of 10 stars."}
            ]
        )

        for partial_review in review_stream:
            print(f"Partial: {partial_review}")

    except ValidationError as e:
        print(f"\nPartial stream validation failed: {str(e)}\n")

    print("\n2. Testing iterable stream with validation errors:\n")

    try:
        # Create an iterable stream that might have validation errors
        reviews_iterable = client.chat.completions.create_iterable(
            model="gpt-3.5-turbo",
            response_model=Review,
            messages=[
                {"role": "user", "content": "Generate 3 product reviews, make one with an invalid rating of 0."}
            ]
        )

        # Process the iterable with error handling for each item
        for i, review in enumerate(reviews_iterable):
            try:
                print(f"Item {i+1}: {review}")
            except ValidationError as item_error:
                print(f"Item {i+1} validation failed: {str(item_error)}")

    except Exception as outer_error:
        print(f"Outer iterable error: {str(outer_error)}")

# Run the function
robust_stream_processing()

