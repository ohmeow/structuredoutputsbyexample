# Recursive Structures
# Learn how to create and work with self-referential data structures using Instructor. This guide demonstrates extraction of hierarchical data like directory trees, organizational charts, and nested comments.
# Traditional data extraction often struggles with representing nested, self-referential data structures.
# Instructor makes it easy to define and extract recursive models with proper typing and validation.

# Import necessary libraries
import instructor
import enum
from openai import OpenAI
from pydantic import BaseModel, Field

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define the node type enum
class NodeType(str, enum.Enum):
    FILE = "file"
    FOLDER = "folder"

# Define the Node class with a self-reference for children
class Node(BaseModel):
    name: str = Field(..., description="Name of the node")
    children: list["Node"] = Field(
        default_factory=list,
        description="List of children nodes, only applicable for folders"
    )
    node_type: NodeType = Field(
        default=NodeType.FILE,
        description="Either a file or folder"
    )

# Important! For recursive models, we need to rebuild the model
Node.model_rebuild()

# Create a container model for the root node
class DirectoryTree(BaseModel):
    root: Node = Field(..., description="Root folder of the directory tree")

# Extract a directory tree from text representation
def parse_directory_structure(text_representation: str) -> DirectoryTree:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=DirectoryTree,
        messages=[
            {
                "role": "system",
                "content": "Parse the following directory structure into a tree."
            },
            {
                "role": "user",
                "content": f"Parse this directory structure:\n{text_representation}"
            }
        ]
    )

# Example usage
directory_structure = '''
root
├── images
│   ├── logo.png
│   └── banner.jpg
└── docs
    ├── readme.md
    └── config
        └── settings.json
'''

result = parse_directory_structure(directory_structure)

# Print the result (you could add a pretty printer here)
print(f"Root folder: {result.root.name}")
print("Contains:")
for child in result.root.children:
    print(f"  - {child.node_type}: {child.name} with {len(child.children)} children")

