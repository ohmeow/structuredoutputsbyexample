# Parallel Extraction
# Process multiple extractions in parallel with Instructor for improved efficiency.
#
# Problem:
# Traditional extraction methods process one piece of information at a time, causing increased latency
# and inefficient use of context window when dealing with multiple related extractions.
#
# Solution:
# Instructor's parallel mode enables simultaneous extraction of multiple structured objects,
# improving response time and making better use of the model's capabilities.

# Import necessary libraries
import instructor
from openai import OpenAI
from typing import Iterable, Literal, Union, List
from pydantic import BaseModel, Field

# ------------------------------
# Basic Parallel Extraction Example
# ------------------------------

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
    """
    Extract both weather requests and search queries from a single user input.
    
    This allows the model to process multiple intents in one go, such as checking
    weather for multiple locations while also performing searches.
    """
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

    return list(function_calls)  # Convert the iterable to a list

# Example usage
def demonstrate_basic_parallel():
    results = extract_parallel_info(
        "What's the weather in New York and Tokyo? Also, find information about renewable energy."
    )

    for result in results:
        if isinstance(result, Weather):
            print(f"Weather request for {result.location} in {result.units} units")
        elif isinstance(result, SearchQuery):
            print(f"Search query: {result.query}")

# ------------------------------
# Advanced Parallel Entity Extraction
# ------------------------------

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
def extract_entities(text: str) -> List[Union[Person, Company, Location]]:
    """
    Extract multiple entity types from a text simultaneously.
    
    This function identifies and structures information about people,
    companies, and locations from unstructured text in a single pass.
    """
    results = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Extract all relevant entities from the text."},
            {"role": "user", "content": text}
        ],
        response_model=Iterable[Person | Company | Location]
    )

    return list(results)

def demonstrate_entity_extraction():
    # Sample text containing multiple entity types
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
    
    # Display extracted entities
    for person in people:
        print(f"Person: {person.name}, {person.age}, {person.occupation}")
    
    for company in companies:
        print(f"Company: {company.name}, {company.industry}, founded in {company.year_founded}")
    
    for location in locations:
        print(f"Location: {location.city}, {location.country}, pop. {location.population}")

# ------------------------------
# Main Execution
# ------------------------------

if __name__ == "__main__":
    print("\n--- Basic Parallel Extraction ---")
    demonstrate_basic_parallel()
    
    print("\n--- Advanced Entity Extraction ---")
    demonstrate_entity_extraction()

