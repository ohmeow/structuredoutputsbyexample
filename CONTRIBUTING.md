# Contributing to Structured Outputs By Example

Thank you for your interest in contributing to Structured Outputs By Example! This document provides guidelines and instructions for contributing new examples or improving existing ones.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/jxnl/instructor.git
   cd instructor/structured-outputs-by-example
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the development environment:
   ```bash
   # Run the file watcher to automatically rebuild when files change
   python watch_and_build.py
   ```

## Adding a New Example

1. **Create a new directory** in `/examples` following the pattern `NNN-example-name` where `NNN` is a three-digit number in sequence.

2. **Add the required files** to your new directory:
   - `example-name.py` - Python file with your example code
   - `example-name.sh` - Shell commands showing how to run the example
   - `example-name_links.txt` - Links to relevant documentation (one URL per line)

3. **Format your Python file** with the proper annotations:

   ```python
   # Annotations are comments at the top of code blocks
   # They explain what the code does
   from typing import List
   import instructor
   from pydantic import BaseModel
   
   # You can add more annotations before new blocks of code
   # These should explain the purpose of the code that follows
   class MyModel(BaseModel):
       field: str
   ```

4. **Run the build script** to generate the site:
   ```bash
   python build_static_site.py
   ```

5. **Check your example** by opening the generated HTML in `/docs/NNN-example-name/index.html`

## Example Annotation Format

- Use comments to annotate code blocks (these will appear in the left column)
- Use clear, concise language to explain concepts
- Include real-world context where helpful
- Group related concepts into sections

## Style Guidelines

- Follow PEP 8 for Python code
- Use type hints consistently
- Keep examples focused on demonstrating one concept
- Provide complete, runnable examples when possible
- Include expected output in shell examples

## Development Workflow

1. **Watch for changes**: Run `python watch_and_build.py` to automatically rebuild when files change
2. **Edit examples**: Make changes to the files in the `/examples` directory
3. **Review**: The site will rebuild automatically, check `/docs` for the results
4. **Submit**: Create a pull request with your changes

## Questions?

If you have questions or need help, please open an issue in the repository.