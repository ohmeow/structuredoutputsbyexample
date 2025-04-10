# Task Planning

# Generate structured task plans from natural language prompts. Instructor helps create step-by-step solutions with dependencies and execution order.

# Instructor can be used to create sophisticated task planning systems that break down complex problems into manageable subtasks. This example shows how to implement a task planner with dependencies and execute them in the correct order.
import asyncio
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define models for task results
class TaskResult(BaseModel):
    task_id: int
    result: str

class TaskResults(BaseModel):
    results: list[TaskResult]

# Define the Task model
class Task(BaseModel):
    id: int = Field(..., description="Unique id of the task")
    task: str = Field(..., description="The task to be performed")
    subtasks: list[int] = Field(
        default_factory=list,
        description="IDs of subtasks that must be completed before this task"
    )

# This method executes a single task and returns its result
# In a real implementation, this would perform actual work rather than return a placeholder
    async def execute(self, with_results: TaskResults) -> TaskResult:
        """Execute this task and return the result."""
        return TaskResult(task_id=self.id, result=f"Result for task: {self.task}")

# Define the TaskPlan model
class TaskPlan(BaseModel):
    task_graph: list[Task] = Field(
        ...,
        description="List of tasks and their dependencies"
    )

    def _get_execution_order(self) -> list[int]:
        """Compute topological sort of tasks based on dependencies."""
        dep_graph = {task.id: set(task.subtasks) for task in self.task_graph}
        result = []

# Find and order tasks based on their dependencies
        while dep_graph:
            available = {task_id for task_id, deps in dep_graph.items() if not deps}  # Tasks with no dependencies
            if not available:
                raise ValueError("Circular dependency detected in tasks")

            result.extend(sorted(available))  # Add to execution order

            # Update dependency graph by removing completed tasks
            dep_graph = {
                task_id: (deps - available)
                for task_id, deps in dep_graph.items()
                if task_id not in available
            }

        return result

    async def execute(self) -> dict[int, TaskResult]:
        """Execute all tasks in dependency order."""
        execution_order = self._get_execution_order()
        tasks_by_id = {task.id: task for task in self.task_graph}
        results = {}

# Execute tasks in dependency order, processing parallel tasks when possible
        while len(results) < len(self.task_graph):
            # Identify tasks whose dependencies are all satisfied
            ready_tasks = [
                tasks_by_id[task_id]
                for task_id in execution_order
                if task_id not in results and
                all(dep_id in results for dep_id in tasks_by_id[task_id].subtasks)
            ]

            # Process all ready tasks concurrently
            new_results = await asyncio.gather(*[
                task.execute(
                    with_results=TaskResults(
                        results=[
                            results[dep_id]
                            for dep_id in task.subtasks
                        ]
                    )
                )
                for task in ready_tasks
            ])

            # Save results for dependent tasks to use
            for result in new_results:
                results[result.task_id] = result

        return results

# Generate a task plan for a complex question
def create_task_plan(question: str) -> TaskPlan:
    return client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Create a detailed task plan to answer the user's question. Break down the problem into smaller, dependent tasks."
            },
            {
                "role": "user",
                "content": question
            }
        ],
        response_model=TaskPlan
    )

# Example usage
async def main():
    plan = create_task_plan(
        "What is the economic impact of renewable energy adoption in developing countries?"
    )
    print("Task Plan:")
    for task in plan.task_graph:
        deps = f" (depends on: {task.subtasks})" if task.subtasks else ""
        print(f"Task {task.id}: {task.task}{deps}")

    print("\nExecuting plan...")
    results = await plan.execute()

    print("\nResults:")
    for task_id, result in sorted(results.items()):
        print(f"Task {task_id}: {result.result}")

# Run the example
if __name__ == "__main__":
    asyncio.run(main())

