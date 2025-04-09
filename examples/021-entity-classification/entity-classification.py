# Entity Classification

# 

# Categorize entities from text using Instructor.
from pydantic import BaseModel, Field
from typing import List, Literal
import instructor
from openai import OpenAI

class Entity(BaseModel):
    text: str = Field(description="The entity text as it appears in the document")
    type: Literal["PERSON", "ORGANIZATION", "LOCATION", "DATE", "PRODUCT"] = Field(
        description="The category/type of the entity"
    )
    start_index: int = Field(description="The starting character position in text")
    end_index: int = Field(description="The ending character position in text")

class EntitiesExtraction(BaseModel):
    entities: List[Entity] = Field(description="List of entities extracted from the text")

# Patch the client
client = instructor.from_openai(OpenAI())

def extract_entities(text: str) -> EntitiesExtraction:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=EntitiesExtraction,
        messages=[
            {
                "role": "system",
                "content": "Extract named entities from the text with their types and positions."
            },
            {"role": "user", "content": text}
        ]
    )

# Test with an example
sample_text = """Apple Inc. is planning to open a new store in Berlin, Germany in July 2024.
               CEO Tim Cook announced the expansion during a press conference yesterday."""

result = extract_entities(sample_text)

print(f"Text: '{sample_text}'")
print("\nExtracted Entities:")
for entity in result.entities:
    print(f"- {entity.text} ({entity.type}) at positions {entity.start_index}-{entity.end_index}")

# Example Output:
# Extracted Entities:
# - Apple Inc. (ORGANIZATION) at positions 0-10
# - Berlin (LOCATION) at positions 42-48
# - Germany (LOCATION) at positions 50-57
# - July 2024 (DATE) at positions 61-70
# - Tim Cook (PERSON) at positions 76-84
# - yesterday (DATE) at positions 128-137

from pydantic import BaseModel, Field
from typing import List, Literal

# Define custom entity types
EntityType = Literal[
    "COMPANY", "PERSON", "CITY", "COUNTRY", "PRODUCT", "TECHNOLOGY",
    "JOB_TITLE", "EVENT", "CURRENCY", "DATE_TIME"
]

class CustomEntity(BaseModel):
    text: str
    type: EntityType
    context: str = Field(description="Brief contextual information about this entity")

class CustomEntitiesExtraction(BaseModel):
    entities: List[CustomEntity]

def extract_custom_entities(text: str) -> CustomEntitiesExtraction:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=CustomEntitiesExtraction,
        messages=[
            {
                "role": "system",
                "content": """Extract named entities from the text using only these types:
                COMPANY, PERSON, CITY, COUNTRY, PRODUCT, TECHNOLOGY, JOB_TITLE, EVENT, CURRENCY, DATE_TIME.
                Include brief contextual information about each entity."""
            },
            {"role": "user", "content": text}
        ]
    )

# Test with a tech news example
tech_news = """Microsoft's CEO Satya Nadella revealed the new Surface Pro 10 at the Build 2024 conference in
               Seattle last week. The device features Qualcomm's Snapdragon X processor and will sell for $1,299
               in the United States starting June 15th."""

result = extract_custom_entities(tech_news)

print(f"Text: '{tech_news}'")
print("\nExtracted Entities:")
for entity in result.entities:
    print(f"- {entity.text} ({entity.type})")
    print(f"  Context: {entity.context}")

# Example Output:
# Extracted Entities:
# - Microsoft (COMPANY)
#   Context: The company that makes Surface products
# - Satya Nadella (PERSON)
#   Context: The CEO of Microsoft
# - Surface Pro 10 (PRODUCT)
#   Context: A new device revealed by Microsoft
# - Build 2024 (EVENT)
#   Context: Conference where the Surface Pro 10 was revealed
# - Seattle (CITY)
#   Context: Location of the Build 2024 conference
# - Qualcomm's Snapdragon X (TECHNOLOGY)
#   Context: Processor used in the Surface Pro 10
# - $1,299 (CURRENCY)
#   Context: The price of the Surface Pro 10
# - United States (COUNTRY)
#   Context: Where the Surface Pro 10 will be sold
# - June 15th (DATE_TIME)
#   Context: When the Surface Pro 10 will start selling

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union, Literal

class PersonEntity(BaseModel):
    name: str
    type: Literal["PERSON"] = "PERSON"
    title: Optional[str] = None
    organization: Optional[str] = None

class OrganizationEntity(BaseModel):
    name: str
    type: Literal["ORGANIZATION"] = "ORGANIZATION"
    industry: Optional[str] = None
    location: Optional[str] = None

class ProductEntity(BaseModel):
    name: str
    type: Literal["PRODUCT"] = "PRODUCT"
    category: Optional[str] = None
    manufacturer: Optional[str] = None
    price: Optional[str] = None

class LocationEntity(BaseModel):
    name: str
    type: Literal["LOCATION"] = "LOCATION"
    location_type: Optional[str] = None  # city, country, address, etc.
    region: Optional[str] = None

class DateEntity(BaseModel):
    text: str
    type: Literal["DATE"] = "DATE"
    is_range: bool = False
    precision: Optional[str] = None  # day, month, year, etc.

class EntitiesWithAttributes(BaseModel):
    entities: List[Union[PersonEntity, OrganizationEntity, ProductEntity, LocationEntity, DateEntity]]

def extract_entities_with_attributes(text: str) -> EntitiesWithAttributes:
    return client.chat.completions.create(
        model="gpt-4",  # More complex task, better with GPT-4
        response_model=EntitiesWithAttributes,
        messages=[
            {
                "role": "system",
                "content": "Extract entities with their attributes. Each entity type has specific attributes."
            },
            {"role": "user", "content": text}
        ]
    )

# Test with a complex example
complex_text = """Tesla CEO Elon Musk announced the new Cybertruck will be available in Austin, Texas
                 from December 2023. The electric vehicle starts at $39,900 and will be manufactured
                 at Tesla's Gigafactory."""

result = extract_entities_with_attributes(complex_text)

print(f"Text: '{complex_text}'")
print("\nExtracted Entities with Attributes:")
for entity in result.entities:
    print(f"\n- {entity.name if hasattr(entity, 'name') else entity.text} ({entity.type})")
    # Print all attributes except name and type
    for key, value in entity.model_dump().items():
        if key not in ['name', 'text', 'type'] and value is not None:
            print(f"  {key}: {value}")

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class EntityWithId(BaseModel):
    id: str = Field(description="Unique identifier for the entity")
    text: str = Field(description="The entity text as found in the document")
    type: str = Field(description="The entity type/category")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Additional entity attributes")

class Relationship(BaseModel):
    source_id: str = Field(description="ID of the source entity")
    target_id: str = Field(description="ID of the target entity")
    relation_type: str = Field(description="Type of relationship between entities")
    description: Optional[str] = None

class EntityRelationExtraction(BaseModel):
    entities: List[EntityWithId] = Field(description="List of entities with unique IDs")
    relationships: List[Relationship] = Field(description="Relationships between entities")

def extract_entity_relationships(text: str) -> EntityRelationExtraction:
    return client.chat.completions.create(
        model="gpt-4",  # Complex relationships need GPT-4
        response_model=EntityRelationExtraction,
        messages=[
            {
                "role": "system",
                "content": """Extract entities and their relationships from the text.
                Assign each entity a unique ID and identify relationships between entities.

                Example relationship types: WORKS_FOR, LOCATED_IN, MANUFACTURES, OWNS, PART_OF, etc."""
            },
            {"role": "user", "content": text}
        ]
    )

# Test with a corporate news example
corporate_news = """
    Amazon CEO Andy Jassy announced that the e-commerce giant is acquiring Anthropic,
    an AI startup based in San Francisco. The deal, worth $4 billion, will help Amazon
    compete with Microsoft, which has invested heavily in OpenAI. Anthropic's founder
    Dario Amodei will continue to lead the company after the acquisition.
"""

result = extract_entity_relationships(corporate_news)

print("Entities:")
for entity in result.entities:
    attrs = ", ".join([f"{k}: {v}" for k, v in entity.attributes.items()]) if entity.attributes else ""
    print(f"- [{entity.id}] {entity.text} ({entity.type}) {attrs}")

print("\nRelationships:")
for rel in result.relationships:
    source = next((e.text for e in result.entities if e.id == rel.source_id), "Unknown")
    target = next((e.text for e in result.entities if e.id == rel.target_id), "Unknown")
    print(f"- {source} {rel.relation_type} {target}")
    if rel.description:
        print(f"  Description: {rel.description}")

