#!/usr/bin/env python3
"""
Check description comments in Python example files.

This script examines each Python example file to verify it has a proper 
description comment in the correct format.
"""

import os
import glob
from pathlib import Path

def check_file_descriptions(file_path):
    """
    Check if a file has the proper description comment format.
    
    The expected format is:
    # Title
    
    # Description paragraph
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    if len(lines) < 3:
        return False, "File too short"
    
    # Check first line is a title comment
    if not lines[0].startswith('# '):
        return False, "First line is not a title comment"
    
    # Check second line is blank
    if lines[1].strip() != '':
        return False, "Second line is not blank"
    
    # Check third line is a description comment
    if not lines[2].startswith('# '):
        return False, "Third line is not a description comment"
    
    # Check if third line is just "# " (empty comment)
    if lines[2].strip() == '#' or lines[2].strip() == '# ':
        return False, "Description comment is empty"
    
    return True, "OK"

def main():
    # Get all Python files in examples directory
    examples_dir = Path(__file__).parent / "examples"
    python_files = glob.glob(str(examples_dir / "**" / "*.py"), recursive=True)
    
    files_needing_fixes = []
    
    for file_path in sorted(python_files):
        is_valid, reason = check_file_descriptions(file_path)
        rel_path = os.path.relpath(file_path, start=Path(__file__).parent)
        
        if not is_valid:
            files_needing_fixes.append((rel_path, reason))
    
    if files_needing_fixes:
        print(f"Found {len(files_needing_fixes)} files needing description fixes:")
        for file_path, reason in files_needing_fixes:
            print(f"- {file_path}: {reason}")
    else:
        print("All files have proper description comments.")

if __name__ == "__main__":
    main()