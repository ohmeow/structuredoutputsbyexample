# PDF Extraction

# - Integrate PDF processing into data pipelines

# Instructor provides support for working with PDF documents through a combination of vision capabilities and structured extraction.
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
import tempfile
from pdf2image import convert_from_path

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define models for document extraction
class Section(BaseModel):
    title: str = Field(description="Section title")
    content: str = Field(description="Section content")

class Document(BaseModel):
    title: str = Field(description="Document title")
    author: str = Field(description="Document author")
    sections: List[Section] = Field(description="Document sections")
    summary: str = Field(description="Brief document summary")

# Extract content from a PDF page as an image
def extract_from_pdf_page(pdf_path: str, page_number: int = 0) -> Document:
    """Extract structured information from a PDF page."""
    # Convert the PDF page to an image
    images = convert_from_path(pdf_path, first_page=page_number+1, last_page=page_number+1)

    # Save the image to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp:
        temp_path = temp.name
        images[0].save(temp_path, 'JPEG')

    # Create an Image object
    image = instructor.Image.from_path(temp_path)

    # Extract information using vision capabilities
    return client.chat.completions.create(
        model="gpt-4-vision-preview",
        response_model=Document,
        messages=[
            {
                "role": "system",
                "content": "Extract structured information from this document page."
            },
            {
                "role": "user",
                "content": [
                    "Extract the complete document structure from this page:",
                    image
                ]
            }
        ]
    )

# Process multiple pages
def process_pdf_document(pdf_path: str, max_pages: int = 5) -> List[Document]:
    """Process multiple pages from a PDF document."""
    results = []

    # Get the number of pages
    from pypdf import PdfReader
    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)
    actual_pages = min(num_pages, max_pages)

    # Process each page
    for i in range(actual_pages):
        page_result = extract_from_pdf_page(pdf_path, i)
        results.append(page_result)
        print(f"Processed page {i+1}/{actual_pages}")

    return results

# Example usage
# documents = process_pdf_document("path/to/document.pdf", max_pages=3)
# for i, doc in enumerate(documents):
#     print(f"Page {i+1}: {doc.title} by {doc.author}")
#     print(f"Summary: {doc.summary}")
#     print(f"Sections: {len(doc.sections)}")

# For more specific document types, you can create specialized models:
from typing import List, Optional
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI
from pdf2image import convert_from_path
import tempfile

# Initialize the client
client = instructor.from_openai(OpenAI())

# Define a model for invoice extraction
class LineItem(BaseModel):
    description: str = Field(description="Description of the item or service")
    quantity: float = Field(description="Quantity of the item")
    unit_price: float = Field(description="Price per unit")
    amount: float = Field(description="Total amount for this line")

class Invoice(BaseModel):
    invoice_number: str = Field(description="Invoice identifier")
    date: str = Field(description="Invoice date")
    vendor: str = Field(description="Name of the vendor/seller")
    customer: str = Field(description="Name of the customer/buyer")
    items: List[LineItem] = Field(description="Line items in the invoice")
    subtotal: float = Field(description="Sum of all items before tax")
    tax: Optional[float] = Field(None, description="Tax amount")
    total: float = Field(description="Total invoice amount")

# Extract invoice from PDF
def extract_invoice(pdf_path: str) -> Invoice:
    """Extract structured invoice data from a PDF."""
    # Convert first page to image
    images = convert_from_path(pdf_path, first_page=1, last_page=1)

    # Save to temp file
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp:
        temp_path = temp.name
        images[0].save(temp_path, 'JPEG')

    # Create image object
    image = instructor.Image.from_path(temp_path)

    # Extract invoice data
    return client.chat.completions.create(
        model="gpt-4-vision-preview",
        response_model=Invoice,
        messages=[
            {
                "role": "system",
                "content": "You are an invoice processing assistant that extracts structured data from invoice images."
            },
            {
                "role": "user",
                "content": [
                    "Extract complete invoice details from this document:",
                    image
                ]
            }
        ]
    )

# Example usage
# invoice = extract_invoice("path/to/invoice.pdf")
# print(f"Invoice #{invoice.invoice_number} from {invoice.vendor}")
# print(f"Date: {invoice.date}")
# print(f"Total: ${invoice.total:.2f}")
# print("Line items:")
# for item in invoice.items:
#     print(f"- {item.description}: {item.quantity} x ${item.unit_price:.2f} = ${item.amount:.2f}")

