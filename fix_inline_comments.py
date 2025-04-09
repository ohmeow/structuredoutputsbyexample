#!/usr/bin/env python3
"""
This script identifies and fixes problematic inline comments in Python examples.
It converts inline comments to regular code or moves them to the top of code blocks.
"""

import os
import re
import glob
from pathlib import Path

# Directory containing the examples
examples_dir = "/Users/jasonliu/dev/instructor/structured-outputs-by-example/examples"

# Find all Python files
py_files = glob.glob(f"{examples_dir}/*/*.py")

# Patterns to identify problematic inline comments
INLINE_COMMENT_PATTERN = re.compile(r'^(\s+)# (.+)$')  # Indented comment inside a function/block
EOL_COMMENT_PATTERN = re.compile(r'^(.+?)  # (.+)$')   # End-of-line comment

def fix_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        
    lines = content.split('\n')
    modified = False
    
    # First pass: identify problematic files with specific patterns
    known_problematic_files = {
        "024-partial-objects/partial-objects.py": [33, 40, 78, 107, 134],
        "026-progressive-updates/progressive-updates.py": [144, 250, 365, 468],
        "044-parallel-extraction/parallel-extraction.py": [36],
        "034-custom-validators/custom-validators.py": [28, 29],
        "035-retry-mechanisms/retry-mechanisms.py": [112]
    }
    
    # Get the relative path for matching known problematic files
    rel_path = os.path.relpath(file_path, examples_dir)
    
    # If this is a known problematic file, fix the specific lines
    problem_lines = []
    for known_path, line_numbers in known_problematic_files.items():
        if rel_path.endswith(known_path):
            problem_lines = line_numbers
            break
            
    if problem_lines:
        print(f"Found known problematic file: {rel_path}")
        for line_num in problem_lines:
            # Make sure line_num is in range
            if 0 <= line_num < len(lines):
                line = lines[line_num]
                
                # Check for indented comments inside functions
                inline_match = INLINE_COMMENT_PATTERN.match(line)
                if inline_match:
                    indentation = inline_match.group(1)
                    comment_text = inline_match.group(2)
                    lines[line_num] = f"{indentation}# Comment removed: {comment_text}"
                    modified = True
                
                # Check for end-of-line comments
                eol_match = EOL_COMMENT_PATTERN.match(line)
                if eol_match:
                    code = eol_match.group(1)
                    lines[line_num] = code
                    modified = True
    
    if modified:
        print(f"Fixed inline comments in {file_path}")
        with open(file_path, 'w') as f:
            f.write('\n'.join(lines))
        return True
    
    return False

# Process each file
fixed_files = 0
for file_path in py_files:
    if fix_file(file_path):
        fixed_files += 1

print(f"Fixed {fixed_files} files with problematic inline comments.")
print("Important: This is a simplistic fix. You should review the changes!")
print("Run 'python build_static_site.py' to rebuild the site with the fixed files.")