# Dependency Trees

# Model hierarchical dependencies using Instructor. This technique helps identify bottlenecks and critical paths in processes and systems.

# Dependency trees represent relationships where some items depend on others. Instructor can extract these structures for tasks like workflow management, build systems, or data processing pipelines.
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a dependency node
class DependencyNode(BaseModel):
    id: str
    description: str
    dependencies: list[str] = Field(default_factory=list,
                                   description="IDs of nodes this node depends on")

# Define the dependency tree
class DependencyTree(BaseModel):
    nodes: list[DependencyNode]

    def get_execution_order(self) -> list[str]:
        """Returns topologically sorted execution order."""
        # Build dependency graph
        dep_graph = {node.id: set(node.dependencies) for node in self.nodes}
        result = []

        # Find nodes with no dependencies
        while dep_graph:
            # Find nodes with no dependencies
            roots = {node for node, deps in dep_graph.items() if not deps}
            if not roots:
                raise ValueError("Circular dependency detected")

            # Add these nodes to the result
            result.extend(sorted(roots))

            # Remove these nodes from the graph
            dep_graph = {
                node: (deps - roots)
                for node, deps in dep_graph.items()
                if node not in roots
            }

        return result

# Extract dependencies from a project description
def extract_dependencies(project_description: str) -> DependencyTree:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Extract the dependencies between tasks in this project."
            },
            {
                "role": "user",
                "content": project_description
            }
        ],
        response_model=DependencyTree
    )

# Example usage
project = """
Building a web application requires:
1. Setup development environment
2. Design database schema (after setup)
3. Create API endpoints (after database schema)
4. Build frontend UI (after API design)
5. Write tests (after API and UI)
6. Deploy application (after tests pass)
"""

dependencies = extract_dependencies(project)
execution_order = dependencies.get_execution_order()
print("Execution order:", execution_order)

