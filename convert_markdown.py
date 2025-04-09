#!/usr/bin/env python3
"""
Markdown to Structured Outputs Examples Converter
Converts Markdown files to the Structured Outputs by Example format.
"""
import re
import os
import sys
from pathlib import Path
import shutil
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def convert_markdown_files(markdown_dir, output_dir="examples"):
    """Convert all markdown files in a directory to structured output examples."""
    markdown_dir = Path(markdown_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Load sections data to map examples to sections
    sections_file = Path("data/sections.json")
    sections_data = {}
    if sections_file.exists():
        try:
            with open(sections_file, "r") as f:
                sections_data = json.load(f)
        except Exception as e:
            logger.error(f"Error loading sections.json: {e}")
    
    # Map to track which examples belong to which sections
    example_to_section = {}
    if sections_data and "sections" in sections_data:
        for section in sections_data["sections"]:
            for example_id in section.get("examples", []):
                example_to_section[example_id] = section["id"]
    
    # Process each markdown file
    for md_file in sorted(markdown_dir.glob("*.md")):
        if md_file.name == "index.md":
            continue  # Skip index file
            
        logger.info(f"Processing {md_file}...")
        
        # Generate example name from filename
        example_id = md_file.stem  # e.g., "001-getting-started"
        
        # Check if directory already exists
        example_dir = output_dir / example_id
        if example_dir.exists():
            logger.info(f"Directory {example_dir} already exists, skipping...")
            continue
            
        # Create example directory
        example_dir.mkdir(exist_ok=True)
        
        # Parse markdown content
        content = md_file.read_text()
        
        # Extract title (first heading)
        title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else example_id.replace("-", " ").title()
        
        # Extract description (text after first heading but before next heading)
        desc_match = re.search(r"^# .+\n+(.+?)(?=\n##|\Z)", content, re.MULTILINE | re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else ""
        
        # Extract code blocks
        python_code = []
        python_annotations = []
        
        # Find all Python code blocks and capture preceding text as annotations
        code_pattern = r"```python\n(.+?)```"
        last_end = 0
        for match in re.finditer(code_pattern, content, re.DOTALL):
            code = match.group(1)
            start = match.start()
            
            # Find the preceding text to use as annotation
            preceding_text = content[last_end:start].strip()
            # Remove any headings from the annotation
            preceding_text = re.sub(r"^#+\s+.*$", "", preceding_text, flags=re.MULTILINE)
            
            # Add to our collections
            python_annotations.append(preceding_text)
            python_code.append(code)
            
            last_end = match.end()
        
        # Extract shell code blocks
        shell_code = []
        shell_annotations = []
        
        # Find all shell/bash code blocks
        shell_pattern = r"```(?:bash|shell)\n(.+?)```"
        last_end = 0
        for match in re.finditer(shell_pattern, content, re.DOTALL):
            code = match.group(1)
            start = match.start()
            
            # Find the preceding text to use as annotation
            preceding_text = content[last_end:start].strip()
            # Only use text after the last Python code block if there is one
            if python_code and last_end < start:
                preceding_text = content[last_end:start].strip()
                # Remove any headings from the annotation
                preceding_text = re.sub(r"^#+\s+.*$", "", preceding_text, flags=re.MULTILINE)
                
            # Add to our collections
            shell_annotations.append(preceding_text)
            shell_code.append(code)
            
            last_end = match.end()
        
        # Extract links
        links = []
        for match in re.finditer(r"\[(.*?)\]\((https?://[^\s)]+)\)", content):
            links.append(match.group(2))
        
        # Extract image references
        images = []
        for match in re.finditer(r"!\[(.*?)\]\((.+?)\)", content):
            img_path = match.group(2)
            img_alt = match.group(1)
            if os.path.exists(markdown_dir.parent / img_path):
                img_filename = Path(img_path).name
                target_path = example_dir / img_filename
                shutil.copy(markdown_dir.parent / img_path, target_path)
                logger.info(f"Copied image: {img_filename}")
                images.append(img_filename)
        
        # Generate Python file with annotations as comments
        example_name = example_id.split("-", 1)[1] if "-" in example_id else example_id
        py_content = f"# {title}\n\n"
        py_content += "# " + description.replace("\n", "\n# ") + "\n\n"
        
        # Combine code blocks with annotations as comments
        for i, (annotation, code) in enumerate(zip(python_annotations, python_code)):
            if annotation:
                # Clean up annotation and add as comments
                clean_annotation = annotation.strip().replace("\n", "\n# ")
                py_content += f"# {clean_annotation}\n"
            py_content += code.strip() + "\n\n"
        
        py_file = example_dir / f"{example_name}.py"
        py_file.write_text(py_content)
        logger.info(f"Created Python file: {py_file}")
        
        # Generate shell file
        shell_content = "# Run the example\n"
        
        # If we have shell blocks, use them
        if shell_code:
            for i, (annotation, code) in enumerate(zip(shell_annotations, shell_code)):
                if annotation:
                    shell_content += f"# {annotation.strip().replace('\n', '\n# ')}\n"
                
                # Format shell commands with $ prefix if not already there
                formatted_code = ""
                for line in code.strip().split("\n"):
                    if line.startswith("$"):
                        formatted_code += line + "\n"
                    else:
                        formatted_code += f"$ {line}\n"
                shell_content += formatted_code + "\n"
        else:
            # Default shell commands if none provided
            shell_content += "# First, install Instructor and any dependencies\n"
            shell_content += "$ pip install instructor pydantic\n\n"
            shell_content += f"# Run the Python script\n$ python {example_name}.py\n"
        
        sh_file = example_dir / f"{example_name}.sh"
        sh_file.write_text(shell_content)
        logger.info(f"Created shell file: {sh_file}")
        
        # Generate links file
        if not links:
            # Default links if none found
            links = ["https://github.com/jxnl/instructor"]
            
        links_file = example_dir / f"{example_name}_links.txt"
        links_file.write_text("\n".join(links))
        logger.info(f"Created links file: {links_file}")
        
        logger.info(f"Converted example: {example_id}")
    
    logger.info(f"Conversion complete!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_markdown.py <markdown_directory> [output_directory]")
        sys.exit(1)
    
    markdown_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "examples"
    convert_markdown_files(markdown_dir, output_dir)