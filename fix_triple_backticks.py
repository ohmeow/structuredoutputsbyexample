#!/usr/bin/env python3
"""
This script removes Markdown-style triple backticks from Python files
to make them compatible with the build system.
"""

import os
import re
import glob

# Directory containing the examples
examples_dir = "/Users/jasonliu/dev/instructor/structured-outputs-by-example/examples"

# Find all Python files
py_files = glob.glob(f"{examples_dir}/*/*.py")

# Pattern to match Markdown code blocks
backtick_pattern = re.compile(r'^# ```.*?$|^# ```bash.*?$|^# ```$', re.MULTILINE)

# Process each file
for file_path in py_files:
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if the file has triple backticks
    if '```' in content:
        print(f"Processing {file_path}")
        
        # Remove the triple backticks while preserving content
        modified_content = backtick_pattern.sub('# ', content)
        
        # Write the modified content back
        with open(file_path, 'w') as f:
            f.write(modified_content)
        
        print(f"  Fixed {file_path}")

print("Done! All Python files have been processed.")