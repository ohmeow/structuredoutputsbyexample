# Hooks and Callbacks

# - Testing and mocking

# Instructor provides a powerful hooks system that allows you to intercept and handle events during the completion and parsing process. Hooks can be used for logging, error handling, and custom behaviors.
import instructor
import openai
import pprint
from pydantic import BaseModel

# Initialize the client with instructor
client = instructor.from_openai(openai.OpenAI())

# Define a simple response model
class User(BaseModel):
    name: str
    age: int

# Define hook handlers
def log_completion_kwargs(*args, **kwargs):
    """Log all arguments passed to the completion function."""
    print("Arguments sent to completion:")
    pprint.pprint(kwargs)

def log_completion_response(response):
    """Log the raw response from the API."""
    print("API Response received:")
    print(f"Model: {response.model}")
    print(f"Usage: {response.usage.total_tokens} tokens")

def handle_error(error):
    """Handle any errors that occur during completion."""
    print(f"Error type: {type(error).__name__}")
    print(f"Error message: {str(error)}")

# Register the hooks
client.on("completion:kwargs", log_completion_kwargs)
client.on("completion:response", log_completion_response)
client.on("completion:error", handle_error)
client.on("parse:error", handle_error)

# Make a request with registered hooks
user = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Extract the user info: John is 25 years old."}
    ],
    response_model=User
)

print("Extracted user:", user)

# Removing a specific hook
client.off("completion:kwargs", log_completion_kwargs)

# Clearing all hooks for a specific event
client.clear("completion:error")

# Clearing all hooks
client.clear()

# You can also use hooks for more advanced use cases such as telemetry or performance monitoring:
import time
import instructor
import openai
from pydantic import BaseModel

# Initialize the client with instructor
client = instructor.from_openai(openai.OpenAI())

# Track performance metrics
class Metrics:
    def __init__(self):
        self.request_times = []
        self.token_counts = []
        self.error_count = 0
        self.request_start_time = None

    def start_request(self, *args, **kwargs):
        self.request_start_time = time.time()

    def end_request(self, response):
        if self.request_start_time is not None:
            elapsed = time.time() - self.request_start_time
            self.request_times.append(elapsed)
            self.token_counts.append(response.usage.total_tokens)
            print(f"Request completed in {elapsed:.2f}s, {response.usage.total_tokens} tokens")

    def record_error(self, error):
        self.error_count += 1
        print(f"Error recorded: {str(error)}")

    def report(self):
        if not self.request_times:
            return "No requests recorded."

        avg_time = sum(self.request_times) / len(self.request_times)
        avg_tokens = sum(self.token_counts) / len(self.token_counts)
        total_tokens = sum(self.token_counts)

        return {
            "total_requests": len(self.request_times),
            "avg_request_time": f"{avg_time:.2f}s",
            "avg_tokens_per_request": int(avg_tokens),
            "total_tokens": total_tokens,
            "error_count": self.error_count
        }

# Create metrics tracker
metrics = Metrics()

# Register hooks
client.on("completion:kwargs", metrics.start_request)
client.on("completion:response", metrics.end_request)
client.on("completion:error", metrics.record_error)
client.on("parse:error", metrics.record_error)

# Run a few example requests
class Product(BaseModel):
    name: str
    price: float
    category: str

for i, query in enumerate([
    "iPhone 13, $799, Smartphones",
    "Air Fryer, $129.99, Kitchen Appliances",
    "Nike Running Shoes, $89.95, Athletic Footwear"
]):
    try:
        product = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Extract product info: {query}"}
            ],
            response_model=Product
        )
        print(f"Product {i+1}: {product.name}, ${product.price}, {product.category}")
    except Exception as e:
        print(f"Failed to extract product {i+1}: {e}")

# Print performance report
performance_report = metrics.report()
print("\nPerformance Report:")
for key, value in performance_report.items():
    print(f"  {key}: {value}")

