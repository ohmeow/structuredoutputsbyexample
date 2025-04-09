# Progressive Updates

# Instructor's partial streaming capability allows you to render UI updates as structured data becomes available.
# This example shows how to progressively update a user interface as data streams in.

# Import necessary libraries
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import instructor
from openai import OpenAI
import time
from enum import Enum
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TaskProgressColumn
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.text import Text

# Initialize Rich console
console = Console()


# Define our weather forecast data model
class WeatherForecast(BaseModel):
    location: str
    current_temp: float = Field(description="Current temperature in Celsius")
    conditions: str = Field(description="Current weather conditions")
    forecast: List[str] = Field(description="Weather forecast for the next few days")
    humidity: Optional[float] = Field(None, description="Current humidity percentage")
    wind_speed: Optional[float] = Field(None, description="Wind speed in km/h")


# Patch the OpenAI client with Instructor
client = instructor.from_openai(OpenAI())


# Define a simulated UI update function to display partial forecast data
def update_ui(partial_forecast):
    # Create a panel for weather information
    weather_table = Table(show_header=False, expand=True)
    weather_table.add_column("Label")
    weather_table.add_column("Value")

    # Location - show placeholder if not available yet
    location = (
        partial_forecast.location
        if partial_forecast.location
        else "Loading location..."
    )
    weather_table.add_row("📍 Location", location)

    # Temperature and conditions section
    temp = (
        f"{partial_forecast.current_temp}°C"
        if partial_forecast.current_temp is not None
        else "--°C"
    )
    conditions = (
        partial_forecast.conditions
        if partial_forecast.conditions
        else "Loading conditions..."
    )
    weather_table.add_row("🌡️ Temperature", temp)
    weather_table.add_row("☁️ Conditions", conditions)

    # Additional data
    humidity = (
        f"{partial_forecast.humidity}%"
        if partial_forecast.humidity is not None
        else "--%"
    )
    wind = (
        f"{partial_forecast.wind_speed} km/h"
        if partial_forecast.wind_speed is not None
        else "-- km/h"
    )
    weather_table.add_row("💧 Humidity", humidity)
    weather_table.add_row("💨 Wind", wind)

    # Forecast section
    forecast_text = Text()
    if not partial_forecast.forecast:
        forecast_text.append("Loading forecast data...")
    else:
        for i, day in enumerate(partial_forecast.forecast):
            forecast_text.append(
                f"• {day}\n" if i < len(partial_forecast.forecast) - 1 else f"• {day}"
            )

    # Calculate progress
    fields = [
        "location",
        "current_temp",
        "conditions",
        "forecast",
        "humidity",
        "wind_speed",
    ]
    populated = sum(
        1
        for f in fields
        if getattr(partial_forecast, f) is not None
        and getattr(partial_forecast, f) != []
    )
    progress_value = populated / len(fields)

    progress = Progress(
        TextColumn("[bold blue]Loading:"),
        BarColumn(),
        TaskProgressColumn(),
        expand=True,
    )
    task = progress.add_task("", total=1.0, completed=progress_value)

    # Combine everything in a panel
    layout = Layout()
    layout.split(
        Layout(Panel(weather_table, title="Weather Forecast"), name="weather"),
        Layout(Panel(forecast_text, title="Forecast"), name="forecast"),
        Layout(Panel(progress, title="Progress"), name="progress"),
    )

    console.clear()
    console.print(layout)


# Create a partial stream using Instructor's create_partial method
forecast_stream = client.chat.completions.create_partial(
    model="gpt-3.5-turbo",
    response_model=WeatherForecast,
    messages=[
        {
            "role": "user",
            "content": "Generate a fictional weather forecast for Tokyo, Japan.",
        }
    ],
)

# Update UI with each new partial object received from the stream
for partial_forecast in forecast_stream:
    update_ui(partial_forecast)
    time.sleep(0.3)  # Slow down for demonstration

console.print("[bold green]✅ Forecast fully loaded!")

# EXAMPLE 2: Sales Dashboard
# This example demonstrates using partial streaming for a business dashboard


# Define a data model for sales information
class SalesData(BaseModel):
    total_revenue: float = Field(description="Total revenue in USD")
    products_sold: int = Field(description="Total number of products sold")
    by_category: Dict[str, float] = Field(
        description="Revenue breakdown by product category"
    )
    top_products: List[str] = Field(description="List of top-selling products")
    growth_rate: Optional[float] = Field(
        None, description="Year-over-year growth rate percentage"
    )


# Simulated chart rendering function
def render_charts(data):
    layout = Layout()

    # Header
    header = Panel("Sales Dashboard", style="bold white on blue")

    # Revenue and products display
    stats_table = Table(expand=True)
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="green")

    revenue = (
        f"${data.total_revenue:,.2f}"
        if data.total_revenue is not None
        else "Loading..."
    )
    products = (
        f"{data.products_sold:,}" if data.products_sold is not None else "Loading..."
    )

    stats_table.add_row("Revenue", revenue)
    stats_table.add_row("Products Sold", products)

    # Growth rate
    growth_text = "Loading..."
    if data.growth_rate is not None:
        growth = f"{data.growth_rate:+.1f}%"
        color = "green" if data.growth_rate > 0 else "red"
        growth_text = Text(growth, style=color)
    stats_table.add_row("Growth Rate", growth_text)

    # Category breakdown
    category_table = Table(title="Revenue by Category", expand=True)
    category_table.add_column("Category")
    category_table.add_column("Amount")
    category_table.add_column("Chart")

    if not data.by_category:
        category_table.add_row("Loading category data...", "", "")
    else:
        max_value = max(data.by_category.values()) if data.by_category else 0
        for category, amount in data.by_category.items():
            bar_length = int(20 * (amount / max_value)) if max_value > 0 else 0
            bar = "█" * bar_length
            category_table.add_row(category, f"${amount:,.2f}", bar)

    # Top products
    products_table = Table(title="Top Products", expand=True)
    products_table.add_column("Rank")
    products_table.add_column("Product")

    if not data.top_products:
        products_table.add_row("", "Loading top products...")
    else:
        for i, product in enumerate(data.top_products, 1):
            products_table.add_row(f"{i}", product)

    # Create layout
    layout.split(
        Layout(header, size=3),
        Layout(Panel(stats_table, title="Key Metrics"), name="stats", size=10),
        Layout(Panel(category_table, title="Categories"), name="categories"),
        Layout(Panel(products_table, title="Top Products"), name="products"),
    )

    console.clear()
    console.print(layout)


# Create a partial stream
sales_stream = client.chat.completions.create_partial(
    model="gpt-3.5-turbo",
    response_model=SalesData,
    messages=[
        {
            "role": "user",
            "content": "Generate fictional quarterly sales data for an electronics company.",
        }
    ],
)

# Update visualization as data comes in
for partial_data in sales_stream:
    render_charts(partial_data)
    time.sleep(0.5)  # Slow down for demonstration

console.print("[bold green]✅ Dashboard fully loaded!")


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class SubTask(BaseModel):
    name: str
    status: TaskStatus = TaskStatus.PENDING
    details: Optional[str] = None


class AnalysisTask(BaseModel):
    document_name: str
    total_words: Optional[int] = None
    subtasks: List[SubTask] = Field(default_factory=list)
    key_findings: List[str] = Field(default_factory=list)
    completion_percentage: Optional[float] = None


# Create a partial stream for a document analysis task
analysis_stream = client.chat.completions.create_partial(
    model="gpt-3.5-turbo",
    response_model=AnalysisTask,
    messages=[
        {
            "role": "user",
            "content": """
            Simulate a document analysis process for a research paper titled
            'Advances in Renewable Energy Storage'. Include multiple subtasks
            and key findings.
        """,
        }
    ],
)


# Display progress updates
def render_progress_ui(task):
    layout = Layout()

    # Header
    doc_name = task.document_name if task.document_name else "Loading document..."
    header = Panel(f"Analyzing: {doc_name}", style="bold white on blue")

    # Document stats
    doc_info = Text()
    if task.total_words is not None:
        doc_info.append(f"Document length: {task.total_words:,} words")
    else:
        doc_info.append("Document length: Calculating...")

    # Subtasks progress
    tasks_table = Table(expand=True)
    tasks_table.add_column("Status")
    tasks_table.add_column("Task")
    tasks_table.add_column("Details")

    if not task.subtasks:
        tasks_table.add_row("⏱️", "Preparing analysis tasks...", "")
    else:
        for subtask in task.subtasks:
            # Status symbol
            if subtask.status == TaskStatus.COMPLETED:
                symbol = "✅"
            elif subtask.status == TaskStatus.IN_PROGRESS:
                symbol = "⏳"
            else:
                symbol = "⏱️"

            details = subtask.details if subtask.details else ""
            tasks_table.add_row(symbol, subtask.name, details)

    # Findings so far
    findings_text = Text()
    if not task.key_findings:
        findings_text.append("No findings yet...")
    else:
        for i, finding in enumerate(task.key_findings, 1):
            findings_text.append(
                f"{i}. {finding}\n" if i < len(task.key_findings) else f"{i}. {finding}"
            )

    # Overall progress
    progress = Progress(
        TextColumn("[bold blue]Overall Progress:"),
        BarColumn(),
        TaskProgressColumn(),
        expand=True,
    )
    task_progress = progress.add_task(
        "", total=1.0, completed=task.completion_percentage or 0
    )

    # Create layout
    layout.split(
        Layout(header, size=3),
        Layout(Panel(doc_info, title="Document Info"), size=5),
        Layout(Panel(tasks_table, title="Analysis Progress"), name="tasks"),
        Layout(Panel(findings_text, title="Key Findings"), name="findings"),
        Layout(Panel(progress, title="Progress"), name="progress", size=5),
    )

    console.clear()
    console.print(layout)


# Update UI as analysis progresses
for partial_analysis in analysis_stream:
    render_progress_ui(partial_analysis)
    time.sleep(0.3)  # Slow down for demonstration

console.print("[bold green]✅ Analysis complete!")


class DocumentSummary(BaseModel):
    title: str
    author: Optional[str] = None
    publication_date: Optional[str] = None
    word_count: Optional[int] = None
    summary: str = Field(description="Complete summary of the document")
    key_points: List[str] = Field(default_factory=list)
    categories: List[str] = Field(default_factory=list)


# Create a streaming document summary
summary_stream = client.chat.completions.create_partial(
    model="gpt-3.5-turbo",
    response_model=DocumentSummary,
    messages=[
        {
            "role": "user",
            "content": """
            Generate a summary for an academic paper titled:
            "The Impact of Artificial Intelligence on Global Labor Markets:
            A Comprehensive Analysis of Automation Trends from 2020-2023"
        """,
        }
    ],
)


# Display document summary with progressive updates
def render_document_summary(partial_summary):
    layout = Layout()

    # Document title
    title = partial_summary.title if partial_summary.title else "Loading title..."
    header = Panel(title, style="bold white on blue")

    # Metadata table
    meta_table = Table(expand=True, show_header=False)
    meta_table.add_column("Field")
    meta_table.add_column("Value")

    author = partial_summary.author if partial_summary.author else "Unknown"
    date = (
        partial_summary.publication_date
        if partial_summary.publication_date
        else "Unknown"
    )
    word_count = (
        f"{partial_summary.word_count:,} words"
        if partial_summary.word_count is not None
        else "Calculating..."
    )

    meta_table.add_row("👤 Author", author)
    meta_table.add_row("📅 Published", date)
    meta_table.add_row("📊 Word Count", word_count)

    # Categories
    categories_text = Text()
    if not partial_summary.categories:
        categories_text.append("Loading categories...")
    else:
        categories_text.append(", ".join(partial_summary.categories))

    # Key points
    points_text = Text()
    if not partial_summary.key_points:
        points_text.append("Extracting key points...")
    else:
        for i, point in enumerate(partial_summary.key_points, 1):
            points_text.append(
                f"{i}. {point}\n"
                if i < len(partial_summary.key_points)
                else f"{i}. {point}"
            )

    # Summary
    summary_text = Text()
    if not partial_summary.summary:
        summary_text.append("Generating summary...")
    else:
        summary_text.append(partial_summary.summary)

    # Create layout
    layout.split(
        Layout(header, size=3),
        Layout(Panel(meta_table, title="Document Metadata"), size=10),
        Layout(Panel(categories_text, title="Categories"), size=5),
        Layout(Panel(points_text, title="Key Points")),
        Layout(Panel(summary_text, title="Summary")),
    )

    console.clear()
    console.print(layout)


# Update UI as summary progresses
for partial_summary in summary_stream:
    render_document_summary(partial_summary)
    time.sleep(0.3)  # Slow down for demonstration

console.print("[bold green]✅ Document summary complete!")
