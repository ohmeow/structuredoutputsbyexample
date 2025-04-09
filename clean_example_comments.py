#!/usr/bin/env python3
"""
Clean up comments in example files to make them more concise.

This script processes all Python example files and makes their comments
more concise while preserving the necessary information.
"""

import os
import glob
import re
from pathlib import Path

def clean_comment_blocks(file_path):
    """
    Clean up verbose comment blocks in a file.
    Preserves the title and description comments WITH NO BLANK LINES BETWEEN THEM.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Don't modify empty files
    if not lines:
        return False
    
    # Identify the header comments - title is first line, subsequent consecutive comment lines are description
    header_lines = []
    
    # Find all consecutive comment lines at the start of the file
    for i, line in enumerate(lines):
        if line.strip().startswith('#'):
            header_lines.append(line)
        else:
            # Found first non-comment line
            break
    
    # Remove blank lines between comments in header
    clean_header = []
    if header_lines:
        # Always keep the first line (title)
        clean_header.append(header_lines[0])
        
        # Add the rest of the header comments with no blank lines
        for line in header_lines[1:]:
            if line.strip() != '#':  # Skip completely empty comment lines
                clean_header.append(line)
    
    # Replace the original header with our clean one
    header_end = len(header_lines)
    
    # If the original header was empty, we didn't do anything
    if not header_lines:
        header_end = 0
    
    # Also clean up the code throughout the file
    modified_lines = []
    
    # Keep title and description unchanged
    modified_lines.extend(lines[:desc_block_end + 1])
    
    # Process the rest of the file
    i = desc_block_end + 1
    while i < len(lines):
        line = lines[i]
        
        # Skip processing inside multiline strings
        if '"""' in line or "'''" in line:
            modified_lines.append(line)
            i += 1
            continue
        
        # Check for comment blocks
        if line.strip().startswith('#'):
            # Found a comment block, collect all lines
            comment_block = [line]
            j = i + 1
            
            while j < len(lines) and lines[j].strip().startswith('#'):
                comment_block.append(lines[j])
                j += 1
            
            # Clean up the comment block if it's more than 3 lines
            if len(comment_block) > 3:
                cleaned_block = clean_comments(comment_block)
                modified_lines.extend(cleaned_block)
            else:
                modified_lines.extend(comment_block)
            
            i = j  # Skip to after the comment block
        else:
            # Not a comment, keep as is
            modified_lines.append(line)
            i += 1
    
    # Always rewrite the file to ensure all files get processed
    with open(file_path, 'w') as f:
        f.writelines(modified_lines)
    
    # For reporting purposes, indicate if we've changed something
    changed = "".join(modified_lines) != "".join(lines)
    return changed

def clean_comments(comment_lines):
    """
    Clean a block of comment lines to make them more concise.
    
    Rules:
    1. Remove empty comment lines (just '#' or '# ')
    2. Condense multiple consecutive empty lines into one
    3. Remove redundant markers like "**bold**"
    4. Clean up common patterns (numeric lists, bullet points, etc.)
    5. Remove excessive spaces between sections
    """
    # Step 1: Remove completely empty comment lines
    non_empty_comments = []
    prev_line_empty = False
    
    for line in comment_lines:
        line = line.rstrip()
        line_content = line.lstrip('#').strip()
        
        # Check if this is an empty comment line
        is_empty = not line_content
        
        # Keep non-empty lines or only one empty line in a row
        if not is_empty or not prev_line_empty:
            # Remove ** markdown bold markers (common in the examples)
            if line_content:
                line = line.replace('**', '')
            
            non_empty_comments.append(line)
        
        prev_line_empty = is_empty
    
    # Step 2: Make all comments more concise
    condensed_comments = []
    i = 0
    while i < len(non_empty_comments):
        line = non_empty_comments[i]
        line_content = line.lstrip('#').strip()
        
        # Special case for "Output:" comments - keep them as is
        if line_content == "Output:" or line_content.startswith("Output might be:"):
            condensed_comments.append(line)
            i += 1
            continue
            
        # Special case for numbered steps
        if re.match(r'^\d+\.\s+', line_content):
            # A numbered list item like "1. Step one"
            condensed_comments.append(line)
            i += 1
            continue
            
        # Check if this is a bullet point
        if line_content.startswith('- ') or line_content.startswith('* '):
            # Start collecting bullet points
            bullet_group = [line]
            j = i + 1
            
            # Look for contiguous bullet points
            while j < len(non_empty_comments):
                next_line = non_empty_comments[j].lstrip('#').strip()
                if next_line.startswith('- ') or next_line.startswith('* '):
                    bullet_group.append(non_empty_comments[j])
                    j += 1
                else:
                    break
            
            # If we have a group of bullet points, condense them
            if len(bullet_group) > 2:
                # Keep all bullet points but ensure they're concise
                for bullet in bullet_group:
                    bullet_content = bullet.lstrip('#').strip()
                    # Simple condensing of common verbose patterns
                    for verbose, concise in [
                        ("This is ", ""),
                        ("is responsible for ", ""),
                        ("allows you to ", ""),
                        ("provides ", ""),
                        ("enables ", ""),
                    ]:
                        bullet_content = bullet_content.replace(verbose, concise)
                    
                    # Reconstruct the comment with the condensed content
                    prefix = bullet.split(bullet.lstrip('#').strip())[0]
                    condensed_comments.append(f"{prefix}{bullet_content}")
                
                i = j  # Skip to after the bullet points
            else:
                # Just a single bullet point, add it as is
                for bullet in bullet_group:
                    condensed_comments.append(bullet)
                i += len(bullet_group)
        else:
            # Not a bullet point, check for common patterns
            if line_content.startswith("This ") and len(line_content) > 30:
                # Often these are verbose explanations
                content = line_content.replace("This is ", "").replace("This ", "")
                prefix = line.split(line_content)[0]
                condensed_comments.append(f"{prefix}{content}")
            else:
                # No special pattern, add as is
                condensed_comments.append(line)
            i += 1
    
    # Step 3: Final cleanup - ensure no excessive blank lines
    final_comments = []
    prev_line_empty = False
    
    for line in condensed_comments:
        line_content = line.lstrip('#').strip()
        is_empty = not line_content
        
        if not is_empty or not prev_line_empty:
            final_comments.append(line)
        
        prev_line_empty = is_empty
    
    # Add a newline to the last line
    if final_comments:
        final_comments[-1] += '\n'
    
    return final_comments

def main():
    examples_dir = Path(__file__).parent / "examples"
    python_files = glob.glob(str(examples_dir / "**" / "*.py"), recursive=True)
    
    cleaned_files = []
    processed_files = []
    
    for file_path in sorted(python_files):
        rel_path = os.path.relpath(file_path, start=Path(__file__).parent)
        processed_files.append(rel_path)
        
        if clean_comment_blocks(file_path):
            cleaned_files.append(rel_path)
            print(f"Cleaned comments in: {rel_path}")
        else:
            print(f"Processed (no changes): {rel_path}")
    
    print(f"\nProcessed {len(processed_files)} files, cleaned {len(cleaned_files)} files")
    
    print("\nRemember to rebuild the site with:")
    print("    python build_static_site.py")

if __name__ == "__main__":
    main()