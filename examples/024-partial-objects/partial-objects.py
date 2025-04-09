# Streaming Partial Objects

# 

# Stream progressively populated structured objects with Instructor.
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI
from typing import Optional, List

class Person(BaseModel):
    name: str
    age: int
    occupation: str
    skills: List[str] = Field(description="List of professional skills")
    bio: Optional[str] = None

# Patch the client
client = instructor.from_openai(OpenAI())

# Create a partial stream
person_stream = client.chat.completions.create_partial(
    model="gpt-3.5-turbo",
    response_model=Person,
    messages=[
        {"role": "user", "content": "Generate profile: John Smith is a 35-year-old software engineer who knows Python, JavaScript, and SQL."}
    ]
)

# Print updates as they arrive
print("Receiving partial updates:")
for person in person_stream:
    # Get a snapshot of current state
    name = person.name if person.name is not None else "[pending]"
    age = person.age if person.age is not None else "[pending]"
    occupation = person.occupation if person.occupation is not None else "[pending]"
    skills = ", ".join(person.skills) if person.skills else "[pending]"
    bio = person.bio if person.bio is not None else "[pending]"

    # Print current state
    print(f"\nCurrent state:")
    print(f"Name: {name}")
    print(f"Age: {age}")
    print(f"Occupation: {occupation}")
    print(f"Skills: {skills}")
    print(f"Bio: {bio}")

# Example partial outputs:
# Current state:
# Name: [pending]
# Age: [pending]
# Occupation: [pending]
# Skills: [pending]
# Bio: [pending]
#
# Current state:
# Name: John Smith
# Age: [pending]
# Occupation: [pending]
# Skills: [pending]
# Bio: [pending]
#
# ...
#
# Current state:
# Name: John Smith
# Age: 35
# Occupation: software engineer
# Skills: Python, JavaScript, SQL
# Bio: John Smith is an experienced software engineer with a passion for building scalable applications...

class FieldTracker:
    def __init__(self, model_class):
        self.field_names = list(model_class.model_fields.keys())
        self.completed_fields = set()

    def update(self, partial_obj):
        # Check which fields are now populated
        newly_completed = []

        for field in self.field_names:
            value = getattr(partial_obj, field)
            if value is not None and field not in self.completed_fields:
                self.completed_fields.add(field)
                newly_completed.append(field)

        return newly_completed

# Create a partial stream
person_stream = client.chat.completions.create_partial(
    model="gpt-3.5-turbo",
    response_model=Person,
    messages=[
        {"role": "user", "content": "Generate profile: Sarah Johnson is a 42-year-old marketing director skilled in SEO, content strategy, and social media."}
    ]
)

# Track field completion
tracker = FieldTracker(Person)

for person in person_stream:
    new_fields = tracker.update(person)

    if new_fields:
        print(f"Newly completed fields: {', '.join(new_fields)}")

        # Show newly available data
        for field in new_fields:
            value = getattr(person, field)
            print(f"  {field}: {value}")

# Example output:
# Newly completed fields: name
#   name: Sarah Johnson
# Newly completed fields: age
#   age: 42
# Newly completed fields: occupation
#   occupation: marketing director
# Newly completed fields: skills
#   skills: ['SEO', 'content strategy', 'social media']
# Newly completed fields: bio
#   bio: Sarah Johnson is an accomplished marketing director with over 15 years of experience...

import time

class CompletionBar:
    def __init__(self, model_class, width=40):
        self.fields = list(model_class.model_fields.keys())
        self.total_fields = len(self.fields)
        self.width = width
        self.last_progress = 0

    def update(self, partial_obj):
        # Count populated fields
        populated = sum(1 for field in self.fields if getattr(partial_obj, field) is not None)
        progress = populated / self.total_fields

        # Only update if progress changed
        if progress > self.last_progress:
            self.last_progress = progress

            # Create progress bar
            filled_width = int(self.width * progress)
            empty_width = self.width - filled_width
            bar = "█" * filled_width + "░" * empty_width
            percent = int(progress * 100)

            # Print progress
            print(f"\rProgress: [{bar}] {percent}% ({populated}/{self.total_fields} fields)", end="")
            return True

        return False

def stream_with_progress_bar():
    # Create progress bar
    bar = CompletionBar(Person)

    # Create partial stream
    person_stream = client.chat.completions.create_partial(
        model="gpt-3.5-turbo",
        response_model=Person,
        messages=[
            {"role": "user", "content": "Generate profile: Michael Chen is a 39-year-old data scientist who knows Python, R, and machine learning techniques."}
        ]
    )

    # Track progress
    for person in person_stream:
        bar.update(person)
        time.sleep(0.1)  # Slow down updates for visibility

    # Complete the progress display
    print("\n\nFinal result:")
    print(f"Name: {person.name}")
    print(f"Age: {person.age}")
    print(f"Occupation: {person.occupation}")
    print(f"Skills: {', '.join(person.skills)}")
    if person.bio:
        print(f"Bio: {person.bio}")

# Example output:
# Progress: [████████████████████████████████████] 100% (5/5 fields)
#
# Final result:
# Name: Michael Chen
# Age: 39
# Occupation: data scientist
# Skills: Python, R, machine learning
# Bio: Michael Chen is an experienced data scientist with a strong background in statistical analysis...

from pydantic import BaseModel, Field
from typing import List, Optional

class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: Optional[str] = None

class Experience(BaseModel):
    title: str
    company: str
    years: int
    description: Optional[str] = None

class ProfileWithNested(BaseModel):
    name: str
    age: int
    addresses: List[Address] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)

# Stream with nested data
profile_stream = client.chat.completions.create_partial(
    model="gpt-4",  # More complex model handles nested data better
    response_model=ProfileWithNested,
    messages=[
        {"role": "user", "content": """
            Generate a profile for Emma Wilson, a 45-year-old executive who has homes in:
            - 123 Main St, New York, USA, 10001
            - 45 Beach Road, Sydney, Australia, 2000

            Work experience:
            - CEO at TechCorp for 5 years
            - VP of Operations at GlobalSystems for 8 years
        """}
    ]
)

# Track the evolving nested data
for profile in profile_stream:
    print("\nCurrent profile state:")
    print(f"Name: {profile.name if profile.name else '[pending]'}")
    print(f"Age: {profile.age if profile.age is not None else '[pending]'}")

    # Show addresses as they come in
    print("Addresses:")
    if not profile.addresses:
        print("  [pending]")
    else:
        for i, addr in enumerate(profile.addresses):
            print(f"  Address {i+1}:")
            print(f"    Street: {addr.street if addr.street else '[pending]'}")
            print(f"    City: {addr.city if addr.city else '[pending]'}")
            print(f"    Country: {addr.country if addr.country else '[pending]'}")
            print(f"    Postal Code: {addr.postal_code if addr.postal_code else '[pending]'}")

    # Show experience as it comes in
    print("Experience:")
    if not profile.experience:
        print("  [pending]")
    else:
        for i, exp in enumerate(profile.experience):
            print(f"  Job {i+1}:")
            print(f"    Title: {exp.title if exp.title else '[pending]'}")
            print(f"    Company: {exp.company if exp.company else '[pending]'}")
            print(f"    Years: {exp.years if exp.years is not None else '[pending]'}")
            print(f"    Description: {exp.description if exp.description else '[pending]'}")

