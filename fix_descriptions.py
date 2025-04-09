#!/usr/bin/env python3
"""
Fix description comments in Python example files.

This script improves the description comments in Python example files
that have inadequate or bullet-style descriptions.
"""

import os
import sys
from pathlib import Path

# Dictionary of improved descriptions for each file
DESCRIPTIONS = {
    # Bullet-style descriptions
    "examples/028-recursive-structures/recursive-structures.py": 
        "# Create and work with self-referential data structures using Instructor. Enables extraction of hierarchical data like organizational charts and family trees.",
    
    "examples/029-knowledge-graphs/knowledge-graphs.py": 
        "# Extract interconnected knowledge graphs from text using Instructor. This approach helps visualize relationships between concepts and entities.",
    
    "examples/030-dependency-trees/dependency-trees.py": 
        "# Model hierarchical dependencies using Instructor. This technique helps identify bottlenecks and critical paths in processes and systems.",
    
    "examples/031-task-planning/task-planning.py": 
        "# Generate structured task plans from natural language prompts. Instructor helps create step-by-step solutions with dependencies and execution order.",
    
    "examples/032-document-structure/document-structure.py": 
        "# Extract document structure and organization using Instructor. Helps with document classification, section analysis, and content organization.",
    
    "examples/034-custom-validators/custom-validators.py": 
        "# Implement custom validators for domain-specific validation rules with Instructor. Enables context-dependent validation for complex business logic.",
    
    "examples/035-retry-mechanisms/retry-mechanisms.py": 
        "# Build robust extraction pipelines with automatic retry mechanisms. Instructor provides tools for creating reliable production applications.",
    
    "examples/036-fallback-strategies/fallback-strategies.py": 
        "# Implement fallback strategies for handling missing or invalid information. Instructor helps provide default values when extraction is uncertain.",
    
    "examples/037-field-level-validation/field-level-validation.py": 
        "# Apply field-level validation rules to enforce domain-specific business logic. Instructor allows fine-grained control over data validation.",
    
    "examples/038-vision-inputs/vision-inputs.py": 
        "# Process and extract data from images with Instructor. Supports automatic detection of image paths and URLs for multimodal extraction.",
    
    "examples/039-image-to-structured-data/image-to-structured-data.py": 
        "# Convert image content into structured data with Instructor. Enables integration with downstream processing pipelines for visual data.",
    
    "examples/041-audio-extraction/audio-extraction.py": 
        "# Extract structured information from audio content using Instructor. Supports handling multilingual audio and transcription data.",
    
    "examples/042-pdf-extraction/pdf-extraction.py": 
        "# Extract structured data from PDF documents with Instructor. Enables integration of PDF processing into data extraction pipelines.",
    
    "examples/043-caching-responses/caching-responses.py": 
        "# Implement caching strategies for LLM responses with Instructor. Supports Redis caching for distributed systems and performance optimization.",
    
    "examples/044-parallel-extraction/parallel-extraction.py": 
        "# Process multiple extractions in parallel with Instructor. Enables more efficient use of context window for related extractions.",
    
    "examples/045-batch-processing/batch-processing.py": 
        "# Implement batch processing for efficient data extraction. Instructor provides structured output for easier data analysis of large datasets.",
    
    "examples/046-hooks-and-callbacks/hooks-and-callbacks.py": 
        "# Use hooks and callbacks to extend Instructor's functionality. Enables custom behavior for testing, mocking, logging, and error handling.",
    
    "examples/047-type-adapters/type-adapters.py": 
        "# Leverage Pydantic Type Adapters with Instructor for advanced validation. Provides better error messaging and custom type conversion.",
    
    "examples/050-resources/resources.py": 
        "# Discover essential resources and tools for working with structured extraction. Instructor builds on Pydantic and integrates with various LLM providers.",
    
    # Short descriptions
    "examples/001-getting-started/getting-started.py": 
        "# Learn the basics of structured LLM outputs with Instructor. This guide demonstrates how to extract consistent, validated data from language models.",
    
    # Generic descriptions
    "examples/002-installation/installation.py": 
        "# Set up Instructor and configure API keys for different LLM providers. Best practices for secure API key management and environment setup.",
    
    "examples/003-first-extraction/first-extraction.py": 
        "# Create your first structured extraction with Instructor. Learn the step-by-step process from model definition to validated response.",
    
    "examples/005-client-setup/client-setup.py": 
        "# Configure Instructor clients for different LLM providers. Learn about extraction modes and client configuration options.",
    
    "examples/017-working-with-enums/working-with-enums.py": 
        "# Use enumerated types with Instructor for consistent, validated extractions. Enums help enforce a fixed set of allowed values.",
    
    "examples/033-validation-basics/validation-basics.py": 
        "# Learn the fundamentals of validation in Instructor. Understand the automatic validation and retry process for ensuring data quality.",
    
    "examples/040-table-extraction/table-extraction.py": 
        "# Extract structured tabular data from text using Instructor. Add descriptive metadata like captions to enhance table representation.",
}

def fix_description(file_path, new_description):
    """Replace the description comment in a file with a new one."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    if len(lines) < 3:
        print(f"Error: {file_path} is too short to fix")
        return False
    
    # Keep the title (first line), replace the description (third line)
    if lines[2].startswith('# '):
        lines[2] = new_description + '\n'
        
        # Write back to file
        with open(file_path, 'w') as f:
            f.writelines(lines)
        return True
    else:
        print(f"Error: {file_path} does not have a proper description line to replace")
        return False

def main():
    project_root = Path(__file__).parent
    count = 0
    
    for rel_path, description in DESCRIPTIONS.items():
        file_path = project_root / rel_path
        if file_path.exists():
            print(f"Fixing: {rel_path}")
            if fix_description(file_path, description):
                count += 1
        else:
            print(f"File not found: {rel_path}")
    
    print(f"\nFixed descriptions in {count} files")
    
    if count > 0:
        print("\nRemember to rebuild the site with:")
        print("    python build_static_site.py")

if __name__ == "__main__":
    main()