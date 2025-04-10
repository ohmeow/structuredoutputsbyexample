# Hooks and Callbacks
# Learn how to use hooks and callbacks to extend Instructor's functionality. This guide demonstrates custom behavior implementation for logging, monitoring, and error handling.
# Standard extraction pipelines offer limited visibility into what happens during processing and few opportunities for custom behaviors.
# Instructor's hooks system lets you intercept and handle events during completions and parsing, enabling powerful extensions for debugging, monitoring, and more.

# Import necessary libraries
import instructor
import openai
import pprint
import time
from pydantic import BaseModel

# Initialize the client with instructor
client = instructor.from_openai(openai.OpenAI())

# Define a simple response model
class User(BaseModel):
    name: str
    age: int

# Basic hooks example
print("\n=== Basic Hooks Example ===")

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

# Hooks management
print("\n=== Hook Management ===")

# Removing a specific hook
client.off("completion:kwargs", log_completion_kwargs)
print("Removed completion:kwargs hook")

# Clearing all hooks for a specific event
client.clear("completion:error")
print("Cleared all hooks for completion:error")

# Clearing all hooks
client.clear()
print("Cleared all hooks")

# Advanced example: Performance monitoring with hooks
print("\n=== Advanced Example: Performance Monitoring ===")

# Initialize a new client
client = instructor.from_openai(openai.OpenAI())

# Track performance metrics
class Metrics:
    def __init__(self):
        self.request_times = []
        self.token_counts = []
        self.error_count = 0
        self.request_start_time = None

    def start_request(self, *args, **kwargs):
        """Record when a request starts."""
        self.request_start_time = time.time()

    def end_request(self, response):
        """Calculate request duration and record token usage."""
        if self.request_start_time is not None:
            elapsed = time.time() - self.request_start_time
            self.request_times.append(elapsed)
            self.token_counts.append(response.usage.total_tokens)
            print(f"Request completed in {elapsed:.2f}s, {response.usage.total_tokens} tokens")

    def record_error(self, error):
        """Track errors that occur during requests."""
        self.error_count += 1
        print(f"Error recorded: {str(error)}")

    def report(self):
        """Generate a performance report from collected metrics."""
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

# Common use cases for hooks
print("\n=== Common Use Cases for Hooks ===")
print("1. Logging: Track requests and responses for debugging")
print("2. Telemetry: Measure performance metrics like latency and token usage")
print("3. Error Handling: Centralize error processing and recovery strategies")
print("4. Retries: Implement custom retry logic for specific error conditions")
print("5. Testing: Mock responses during development and testing")
print("6. Caching: Implement response caching to reduce API calls")
print("7. Rate Limiting: Add custom rate limiting to avoid quota issues")

