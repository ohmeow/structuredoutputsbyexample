#!/usr/bin/env python3
"""
Analyze description comments in Python example files.

This script examines each Python example file and categorizes the description
quality and style to help identify files that need improved descriptions.
"""

import os
import glob
from pathlib import Path
import re

def analyze_file_description(file_path):
    """
    Analyze a file's description comment and return details about its format and quality.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    if len(lines) < 3:
        return {"status": "missing", "description": "File too short"}
    
    # Check first line is a title comment
    if not lines[0].startswith('# '):
        return {"status": "invalid", "description": "First line is not a title comment"}
    
    # Check second line is blank
    if lines[1].strip() != '':
        return {"status": "invalid", "description": "Second line is not blank"}
    
    # Check third line is a description comment
    if not lines[2].startswith('# '):
        return {"status": "invalid", "description": "Third line is not a description comment"}
    
    # Get the description text
    description_text = lines[2].lstrip('# ').strip()
    
    # Analyze description quality
    if description_text == '':
        return {"status": "empty", "description": "Empty description comment"}
    elif description_text.startswith('-'):
        return {"status": "bullet", "description": description_text}
    elif len(description_text) < 20:
        return {"status": "short", "description": description_text}
    elif "Instructor" not in description_text and "structured" not in description_text.lower():
        return {"status": "generic", "description": description_text}
    else:
        return {"status": "good", "description": description_text}

def main():
    # Get all Python files in examples directory
    examples_dir = Path(__file__).parent / "examples"
    python_files = glob.glob(str(examples_dir / "**" / "*.py"), recursive=True)
    
    # Categorize files by description quality
    categories = {
        "empty": [],
        "bullet": [],
        "short": [],
        "generic": [],
        "good": [],
        "invalid": [],
        "missing": []
    }
    
    for file_path in sorted(python_files):
        rel_path = os.path.relpath(file_path, start=Path(__file__).parent)
        analysis = analyze_file_description(file_path)
        categories[analysis["status"]].append((rel_path, analysis["description"]))
    
    # Print analysis summary
    print("Description Analysis Summary:")
    print(f"Total files: {len(python_files)}")
    
    for category, files in categories.items():
        if files:
            print(f"\n{category.upper()} descriptions ({len(files)}):")
            for file_path, desc in files:
                if category == "good":
                    print(f"- {file_path}")
                else:
                    print(f"- {file_path}: {desc}")
    
    # Generate a list of files that need better descriptions
    needs_improvement = (
        categories["empty"] + 
        categories["bullet"] + 
        categories["short"] + 
        categories["generic"] + 
        categories["invalid"] + 
        categories["missing"]
    )
    
    if needs_improvement:
        print("\nFiles needing better descriptions:")
        for file_path, _ in needs_improvement:
            print(f"- {file_path}")

if __name__ == "__main__":
    main()