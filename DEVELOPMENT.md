# Development Guide

This document provides detailed information about the development workflow and technical details of the Structured Outputs By Example project.

## Architecture

The site is built using a static site generator that processes example files and generates HTML pages:

1. **Example Sources**: Raw Python, shell scripts, and documentation links in `/examples`
2. **Build Process**: Scripts in `/build_examples` parse these files and extract annotations
3. **Data Storage**: Processed example data is stored in JSON format in `/data`
4. **Static Generation**: The `build_static_site.py` script generates HTML files in `/docs`

## File Watcher

The `watch_and_build.py` script provides automatic rebuilding when files change:

```bash
# Start the file watcher
python watch_and_build.py
```

The watcher monitors the following directories:
- `/examples` - Source example files
- `/data` - JSON data files
- `/build_examples` - Build scripts

When changes are detected, it automatically runs the `build_static_site.py` script to rebuild the site.

### How the Watcher Works

1. **Setup**: The script uses the Python `watchdog` library to monitor file system events
2. **Event Handling**: When a file is modified or created, it triggers a rebuild
3. **Cooldown**: There's a 2-second cooldown period to prevent multiple rapid rebuilds
4. **Initial Build**: When started, it performs an initial build before watching for changes

### Customizing the Watcher

If you need to watch additional directories or change the cooldown period, edit the `watch_and_build.py` file:

```python
# Directories to watch
watch_paths = [
    project_root / "examples",  # Example files
    project_root / "data",      # JSON data files
    project_root / "build_examples"  # Build scripts
    # Add additional directories here
]

# Change the cooldown period (in seconds)
self.build_cooldown = 2  # Default is 2 seconds
```

## Build Process

The build process involves several steps:

1. **Processing Examples**: The `build_examples/build_examples.py` script:
   - Parses Python files to extract code and annotations
   - Processes shell scripts to extract commands and outputs
   - Collects documentation links
   - Generates a structured JSON representation

2. **Static Site Generation**: The `build_static_site.py` script:
   - Loads the JSON data
   - Generates HTML pages for each example
   - Creates the index page
   - Copies static assets
   - Generates text files for LLM context

## Project Structure

- `/examples` - Source examples organized by topic
- `/build_examples` - Build scripts for processing examples
- `/data` - Processed example data in JSON format
- `/docs` - Generated static site (HTML, CSS, JS)
- `/static` - Static assets (CSS, JS, images)

## Troubleshooting

- **Build Errors**: Check the Python console output for error messages
- **Missing Examples**: Ensure your example directory follows the naming convention
- **Annotation Issues**: Verify that annotations are properly formatted as comments
- **Static Assets**: If CSS or JS isn't loading, check that static assets are properly copied