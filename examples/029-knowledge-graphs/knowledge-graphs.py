# Knowledge Graphs

# - Visual representation of concepts

# Instructor can be used to extract structured knowledge graphs from text. A knowledge graph represents entities and their relationships, making complex information easier to understand and visualize.
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define the node structure
class Node(BaseModel):
    id: int
    label: str
    color: str

# Define the edge structure
class Edge(BaseModel):
    source: int
    target: int
    label: str
    color: str = "black"

# Define the knowledge graph structure
class KnowledgeGraph(BaseModel):
    nodes: list[Node] = Field(..., default_factory=list)
    edges: list[Edge] = Field(..., default_factory=list)

# Extract a knowledge graph from text
def generate_knowledge_graph(input_text: str) -> KnowledgeGraph:
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"Create a detailed knowledge graph for: {input_text}"
            }
        ],
        response_model=KnowledgeGraph
    )

# Example usage
graph = generate_knowledge_graph("Quantum mechanics and its applications")

# Print the nodes and edges
for node in graph.nodes:
    print(f"Node {node.id}: {node.label} ({node.color})")

for edge in graph.edges:
    print(f"Edge: {edge.source} --({edge.label})--> {edge.target}")

# To visualize the knowledge graph, you can use libraries like graphviz:
from graphviz import Digraph

def visualize_knowledge_graph(kg: KnowledgeGraph):
    dot = Digraph(comment="Knowledge Graph")

    # Add nodes
    for node in kg.nodes:
        dot.node(str(node.id), node.label, color=node.color)

    # Add edges
    for edge in kg.edges:
        dot.edge(str(edge.source), str(edge.target),
                 label=edge.label, color=edge.color)

    # Render the graph
    dot.render("knowledge_graph.gv", view=True)

# Visualize the graph
visualize_knowledge_graph(graph)

