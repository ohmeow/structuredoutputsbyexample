# Structured Outputs By Example

A comprehensive guide to using structured outputs with LLMs, showcased through annotated examples.

## Overview

Structured Outputs By Example is a hands-on introduction to working with structured data extraction from LLMs using libraries like Instructor and Pydantic. The site demonstrates how to extract structured information reliably from LLM outputs across various providers and use cases.

[![PyPI version](https://badge.fury.io/py/instructor.svg)](https://badge.fury.io/py/instructor)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Attribution

This project was created by Jason Liu and is a fork of [Gemini by Example](https://geminibyexample.com/)'s codebase ([GitHub repo](https://github.com/strickvl/geminibyexample)). While the content has been completely replaced with Instructor and Pydantic examples for structured data extraction from LLMs, the site generator code and presentation format are from the original Gemini by Example project. Full credit to the original authors for creating this excellent example-based learning framework.

## Examples

The site is organized into sections:

- **Getting Started** - Introduction and setup
- **LLM Providers** - Using different LLM providers 
- **Basic Extraction** - Simple data extraction patterns
- **Classification** - Using structured outputs for classification
- **Streaming** - Working with streaming responses
- **Advanced Structures** - Complex data structures and relationships
- **Validation** - Ensuring data quality
- **Multimodal** - Working with images, audio, and documents
- **Performance** - Optimizing for production use

## Development

This site is built using a static site generator that processes examples into an annotated format.

### Setup

```shell
# Install dependencies
pip install -r requirements.txt

# Build the site
python build_static_site.py

# Or watch for changes and rebuild automatically
python watch_and_build.py
```

### Project Structure

- `/examples` - Source examples in organized directories
- `/build_examples` - Scripts for processing examples
- `/data` - Processed example data
- `/docs` - Generated static site
- `/static` - CSS, JS, and image assets

### Contributing

To add a new example:

1. Create a new directory in `/examples` with the pattern `NNN-example-name`
2. Add required files:
   - `example-name.py` - Annotated Python file with examples
   - `example-name.sh` - Shell commands demonstrating the example
   - `example-name_links.txt` - Related documentation links
3. Run the build to generate the site

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on adding new examples and [DEVELOPMENT.md](DEVELOPMENT.md) for technical details about the site generation process.

## License

MIT