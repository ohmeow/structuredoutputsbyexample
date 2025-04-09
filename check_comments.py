import os

def check_file_comments(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # File must have at least 3 lines for the pattern
        if len(lines) < 3:
            return "Too few lines, missing proper comment structure"
        
        # Check first line is a title comment
        if not lines[0].strip().startswith('# '):
            return "First line is not a title comment"
        
        # Check second line is blank
        if lines[1].strip() != '':
            return "No blank line after title"
        
        # Check if we have the pattern:
        # Line 1: Title
        # Line 2: Blank
        # Line 3: Just a '#'
        # Line 4: Blank
        # Line 5: Actual description
        if len(lines) >= 5 and lines[2].strip() in ['#', '# '] and \
           not lines[3].strip() and lines[4].strip().startswith('# ') and len(lines[4].strip()) > 2:
            return "Incorrect format (description on line 5 instead of line 3)"
        
        # Check third line for a proper description
        if not lines[2].strip().startswith('# '):
            return "Missing description after blank line"
        
        # Check if third line is just a '#' without content
        if lines[2].strip() in ['#', '# ']:
            return "Missing description (line 3 just has '#')"
        
        return None
    except Exception as e:
        return f"Error checking file: {str(e)}"

def main():
    base_path = '/Users/jasonliu/dev/structured-outputs-by-example/examples'
    files_with_issues = []
    
    # Walk through all directories in examples
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                issue = check_file_comments(file_path)
                
                if issue:
                    relative_path = os.path.relpath(file_path, '/Users/jasonliu/dev/structured-outputs-by-example')
                    files_with_issues.append((relative_path, issue))
    
    # Print report in the requested format
    print("FILES NEEDING FIXES:")
    
    # Print all files with issues in the requested format
    for i, (file_path, issue) in enumerate(files_with_issues, 1):
        if "description on line 5" in issue:
            print(f"{i}. {file_path} - Incorrect format (no blank line)")
        elif "Missing description" in issue:
            print(f"{i}. {file_path} - Missing description")
        else:
            print(f"{i}. {file_path} - {issue}")
    
    if not files_with_issues:
        print("All files have the correct comment structure.")

if __name__ == "__main__":
    main()