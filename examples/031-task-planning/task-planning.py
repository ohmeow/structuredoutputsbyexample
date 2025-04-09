# Task Planning

# - Creating step-by-step solutions

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

    async def execute(self, with_results: TaskResults) -> TaskResult:
        """Execute this task and return the result."""
        # In a real implementation, this would perform the actual task
        # Here we just return a placeholder result
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

        while dep_graph:
            # Find tasks with no remaining dependencies
            available = {task_id for task_id, deps in dep_graph.items() if not deps}
            if not available:
                raise ValueError("Circular dependency detected in tasks")

            # Add them to the result
            result.extend(sorted(available))

            # Remove these tasks from the graph
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

        while len(results) < len(self.task_graph):
            # Find tasks ready to execute (all dependencies satisfied)
            ready_tasks = [
                tasks_by_id[task_id]
                for task_id in execution_order
                if task_id not in results and
                all(dep_id in results for dep_id in tasks_by_id[task_id].subtasks)
            ]

            # Execute tasks in parallel
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

            # Store results
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

