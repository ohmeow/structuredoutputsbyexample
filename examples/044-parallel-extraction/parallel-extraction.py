# Parallel Extraction

# - More efficient use of context window for related extractions

# Instructor supports parallel function calling, allowing you to extract multiple pieces of information simultaneously. This can significantly reduce latency in your applications.
import instructor
from openai import OpenAI
from typing import Iterable, Literal, Union
from pydantic import BaseModel

# Initialize the client with instructor in parallel mode
client = instructor.from_openai(OpenAI(), mode=instructor.Mode.PARALLEL_TOOLS)

# Define multiple response models
class Weather(BaseModel):
    location: str
    units: Literal["imperial", "metric"]

class SearchQuery(BaseModel):
    query: str

# Extract multiple pieces of information in parallel
def extract_parallel_info(user_query: str) -> list[Union[Weather, SearchQuery]]:
    function_calls = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You must always use tools"},
            {
                "role": "user",
                "content": user_query
            }
        ],
        response_model=Iterable[Weather | SearchQuery]
    )

    # Convert the iterable to a list
    return list(function_calls)

# Example usage
results = extract_parallel_info(
    "What's the weather in New York and Tokyo? Also, find information about renewable energy."
)

for result in results:
    if isinstance(result, Weather):
        print(f"Weather request for {result.location} in {result.units} units")
    elif isinstance(result, SearchQuery):
        print(f"Search query: {result.query}")

# You can also define more complex parallel extractions:
from typing import Iterable, Union
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI

# Initialize client with parallel mode
client = instructor.from_openai(OpenAI(), mode=instructor.Mode.PARALLEL_TOOLS)

# Define extraction models
class Person(BaseModel):
    name: str
    age: int
    occupation: str

class Company(BaseModel):
    name: str
    industry: str
    year_founded: int

class Location(BaseModel):
    city: str
    country: str
    population: int = Field(description="Approximate population")

# Extract multiple entity types from text
def extract_entities(text: str) -> list[Union[Person, Company, Location]]:
    results = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Extract all relevant entities from the text."},
            {"role": "user", "content": text}
        ],
        response_model=Iterable[Person | Company | Location]
    )

    return list(results)

# Example usage
text = """
John Smith is a 35-year-old software engineer living in San Francisco, USA,
a city with about 815,000 people. He works at TechCorp, a software development
company founded in 2005 that specializes in AI applications. His colleague
Maria Rodriguez, 29, is a data scientist who recently moved from Madrid, Spain,
a city of approximately 3.2 million people.
"""

entities = extract_entities(text)

# Process different entity types
people = [e for e in entities if isinstance(e, Person)]
companies = [e for e in entities if isinstance(e, Company)]
locations = [e for e in entities if isinstance(e, Location)]

print(f"Found {len(people)} people, {len(companies)} companies, and {len(locations)} locations")

