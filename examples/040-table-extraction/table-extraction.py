# Table Extraction

# Extract structured tabular data from text using Instructor. Add descriptive metadata like captions to enhance table representation.

# Instructor makes it easy to extract structured tables from images and convert them to pandas dataframes for analysis.
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
import pandas as pd
from typing import Annotated, Any
from io import StringIO
from pydantic import (
    BaseModel,
    BeforeValidator,
    PlainSerializer,
    InstanceOf,
    WithJsonSchema,
)

# Initialize the client with instructor (MD_JSON mode works well for tables)
client = instructor.from_openai(OpenAI(), mode=instructor.Mode.MD_JSON)


# Define functions to convert between dataframe and markdown
def to_markdown(df: pd.DataFrame) -> str:
    """Convert a dataframe to markdown format."""
    return df.to_markdown()


def md_to_df(data: Any) -> Any:
    """Convert markdown table to a pandas dataframe."""
    if isinstance(data, str):
        return (
            pd.read_csv(
                StringIO(data),
                sep="|",
                index_col=1,
            )
            .dropna(axis=1, how="all")
            .iloc[1:]
            .map(lambda x: x.strip())
        )
    return data


# Define a custom type for markdown dataframes
MarkdownDataFrame = Annotated[
    InstanceOf[pd.DataFrame],
    BeforeValidator(md_to_df),
    PlainSerializer(to_markdown),
    WithJsonSchema(
        {
            "type": "string",
            "description": "The markdown representation of the table",
        }
    ),
]


# Define the table model
class Table(BaseModel):
    caption: str = Field(description="A descriptive caption for the table")
    dataframe: MarkdownDataFrame = Field(
        description="The table data as a markdown table"
    )


# Function to extract tables from images
# Create an image object or use autodetect
def extract_table_from_image(image_path_or_url: str) -> Table:
    """Extract a table from an image and return it as a structured object."""
    if image_path_or_url.startswith(("http://", "https://")):
        image = instructor.Image.from_url(image_path_or_url)
    else:
        image = instructor.Image.from_path(image_path_or_url)

    return client.chat.completions.create(
        model="gpt-4-vision-preview",
        response_model=Table,
        max_tokens=1800,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract the table from this image with a descriptive caption.",
                    },
                    image,
                ],
            }
        ],
    )


# Example usage
def analyze_table_data(image_path: str):
    """Extract and analyze a table from an image."""
    table = extract_table_from_image(image_path)

    print(f"Table Caption: {table.caption}")
    print("\nExtracted Table:")
    print(table.dataframe)

    # Perform data analysis if it's a pandas DataFrame
    if isinstance(table.dataframe, pd.DataFrame):
        print("\nData Analysis:")
        print(f"- Rows: {len(table.dataframe)}")
        print(f"- Columns: {len(table.dataframe.columns)}")

        # Basic statistics if numeric columns exist
        numeric_cols = table.dataframe.select_dtypes(include=["number"]).columns
        if len(numeric_cols) > 0:
            print("\nNumeric Column Statistics:")
            for col in numeric_cols:
                col_data = table.dataframe[col]
                print(
                    f"- {col}: Min={col_data.min()}, Max={col_data.max()}, Mean={col_data.mean():.2f}"
                )

        return table.dataframe

    return None


# This would be called as:# df = analyze_table_data("path/to/table_image.jpg")# After this, you can use pandas operations on the dataframe# For multiple tables in a single image, you can use the iterable response:
def extract_multiple_tables(image_path_or_url: str) -> list[Table]:
    """Extract all tables from an image."""
    if image_path_or_url.startswith(("http://", "https://")):
        image = instructor.Image.from_url(image_path_or_url)
    else:
        image = instructor.Image.from_path(image_path_or_url)

    tables = client.chat.completions.create_iterable(
        model="gpt-4-vision-preview",
        response_model=Table,
        max_tokens=1800,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract all tables from this image. Each table should be separate and have its own caption.",
                    },
                    image,
                ],
            }
        ],
    )

    return list(tables)


# Process multiple tables from one image
# Convert to dataframe and return list of dataframes
def analyze_multiple_tables(image_path: str):
    """Extract and analyze all tables from an image."""
    tables = extract_multiple_tables(image_path)

    print(f"Found {len(tables)} tables in the image.")

    for i, table in enumerate(tables):
        print(f"\n--- Table {i+1}: {table.caption} ---")
        print(table.dataframe)

        if isinstance(table.dataframe, pd.DataFrame):
            yield table.dataframe
