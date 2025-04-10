# Nested Structures
# Learn how to extract complex nested data structures from text using Instructor. This guide demonstrates working with hierarchical and recursive models.
# Real-world data often contains complex relationships between different entities and attributes.
# Instructor enables extraction of deeply nested structures while maintaining proper typing and validation.

# Import necessary libraries
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# Basic nested structure example
class Address(BaseModel):
    street: str
    city: str
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: str

class PhoneNumber(BaseModel):
    number: str
    type: str  # e.g., "home", "work", "mobile"

class Person(BaseModel):
    name: str
    age: int
    addresses: List[Address]
    phone_numbers: List[PhoneNumber]
    email: Optional[str] = None

# Patch the client
client = instructor.from_openai(OpenAI())

# Extract nested data
person = client.chat.completions.create(
    model="gpt-4",  # Complex extraction works better with more capable models
    response_model=Person,
    messages=[
        {"role": "user", "content": """
        John Smith is a 35-year-old professional. He has two addresses:
        1. Home: 123 Main St, Austin, TX 78701, USA
        2. Work: 456 Business Ave, Austin, TX 78702, USA

        His phone numbers are:
        - Mobile: (555) 123-4567
        - Work: (555) 987-6543

        You can reach him at john.smith@example.com
        """}
    ]
)

print(f"Name: {person.name}, Age: {person.age}")
print(f"Email: {person.email}")

print("\nAddresses:")
for i, address in enumerate(person.addresses, 1):
    print(f"  {i}. {address.street}, {address.city}, {address.state} {address.zip_code}, {address.country}")

print("\nPhone Numbers:")
for phone in person.phone_numbers:
    print(f"  {phone.type}: {phone.number}")

# More complex nested structure example
class Skill(BaseModel):
    name: str
    level: str  # e.g., "beginner", "intermediate", "expert"
    years_of_experience: int

class Education(BaseModel):
    degree: str
    institution: str
    year: int

class WorkExperience(BaseModel):
    company: str
    position: str
    start_year: int
    end_year: Optional[int] = None
    is_current: bool
    responsibilities: List[str]

class Resume(BaseModel):
    name: str
    age: int
    skills: List[Skill]
    education: List[Education]
    work_experience: List[WorkExperience]
    contact_info: Dict[str, str]  # e.g., "email", "phone", "linkedin"

# Extract with a more capable model
resume = client.chat.completions.create(
    model="gpt-4",
    response_model=Resume,
    messages=[
        {"role": "user", "content": """
        Resume: Sarah Johnson

        Sarah is a 42-year-old software architect with 15 years in the industry.

        Contact Information:
        - Email: sarah.j@example.com
        - Phone: (555) 234-5678
        - LinkedIn: linkedin.com/in/sarahjohnson

        Skills:
        - Python (Expert, 12 years)
        - JavaScript (Intermediate, 8 years)
        - Cloud Architecture (Expert, 7 years)

        Education:
        - Master's in Computer Science, Stanford University, 2008
        - Bachelor's in Software Engineering, MIT, 2006

        Work Experience:
        - TechCorp Inc.
          Senior Software Architect
          2018-Present
          Responsibilities:
          * Lead architecture design for cloud solutions
          * Manage team of 12 developers
          * Implement CI/CD pipelines

        - DataSystems LLC
          Software Developer
          2012-2018
          Responsibilities:
          * Developed backend services in Python
          * Optimized database performance
          * Created RESTful APIs
        """}
    ]
)

print(f"Name: {resume.name}, Age: {resume.age}")

print("\nContact Info:")
for key, value in resume.contact_info.items():
    print(f"  {key}: {value}")

print("\nSkills:")
for skill in resume.skills:
    print(f"  {skill.name}: {skill.level} ({skill.years_of_experience} years)")

print("\nEducation:")
for edu in resume.education:
    print(f"  {edu.degree}, {edu.institution}, {edu.year}")

print("\nWork Experience:")
for job in resume.work_experience:
    current = "(Current)" if job.is_current else f"({job.start_year}-{job.end_year})"
    print(f"  {job.position} at {job.company} {current}")
    print("  Responsibilities:")
    for resp in job.responsibilities:
        print(f"    - {resp}")

# Recursive structure example
class Comment(BaseModel):
    text: str
    author: str
    replies: List['Comment'] = []

# This is needed for recursive Pydantic models
Comment.model_rebuild()

class Post(BaseModel):
    title: str
    content: str
    author: str
    comments: List[Comment]

# Extract recursive structure
post = client.chat.completions.create(
    model="gpt-4",
    response_model=Post,
    messages=[
        {"role": "user", "content": """
        Blog Post: "Python Tips and Tricks"
        By: JohnDev

        Python has many features that make it a versatile language. Here are some tips to improve your code...

        Comments:
        1. Comment by Alice: "Great post! I especially liked the section on list comprehensions."
          - Reply by JohnDev: "Thanks Alice! Glad you found it useful."
            - Reply by Bob: "List comprehensions are my favorite too!"
               - Reply by Alice: "They're so elegant compared to traditional loops."

        2. Comment by Charlie: "Could you do a follow-up on decorators?"
          - Reply by JohnDev: "Great idea! I'll add it to my list of topics."
        """}
    ]
)

print(f"Post: {post.title} by {post.author}")

for i, comment in enumerate(post.comments, 1):
    print(f"\nTop-level Comment {i}: {comment.author} said: '{comment.text}'")

    def print_replies(replies, indent=2):
        for reply in replies:
            print(f"{'  ' * indent}{reply.author} replied: '{reply.text}'")
            if reply.replies:
                print_replies(reply.replies, indent + 1)

    print_replies(comment.replies)

