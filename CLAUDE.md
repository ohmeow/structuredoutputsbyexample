# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands
- Build static site: `python build_static_site.py`
- Watch for changes and rebuild: `python watch_and_build.py`
- Fix inline comments: `python fix_inline_comments.py`
- Fix triple backticks: `python fix_triple_backticks.py`

## Code Style Guidelines
- Python version: >=3.9
- Formatting: Follow PEP 8, 4-space indentation, 88-100 character line length (Black compatible)
- Linting: Use ruff (`pip install ruff`)
- Type checking: Use mypy (`pip install mypy`)
- Import order: Standard library → Third-party → Local, alphabetically sorted within groups
- Naming: snake_case for functions/variables, PascalCase for classes
- Error handling: Use specific exception types with appropriate logging
- Comments: Use descriptive annotations for example code (these become documentation)

## Development Patterns
- Example files follow strict naming pattern: `NNN-example-name/example-name.py`
- Each example needs a .py file, .sh file, and _links.txt file
- Annotations in Python examples become documentation in the generated site
- Use type hints consistently throughout the codebase