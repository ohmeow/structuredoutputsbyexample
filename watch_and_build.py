#!/usr/bin/env python3
"""
File watcher for Structured Outputs by Example.

This script watches for changes in example files and rebuilds the static site 
when changes are detected.
"""

import logging
import subprocess
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ExampleChangeHandler(FileSystemEventHandler):
    """Handles file system events for examples and rebuilds the site when needed."""
    
    def __init__(self, project_root):
        self.project_root = project_root
        self.last_build_time = 0
        self.build_cooldown = 2  # seconds
        
    def on_any_event(self, event):
        """Handle file system events."""
        # Skip if it's not a file creation or modification event
        if not isinstance(event, (FileModifiedEvent, FileCreatedEvent)):
            return
            
        # Skip if it's a hidden file or directory
        if Path(event.src_path).name.startswith('.'):
            return
            
        # Skip if build cooldown hasn't expired
        current_time = time.time()
        if current_time - self.last_build_time < self.build_cooldown:
            return
            
        # Rebuild the site
        logger.info(f"Change detected in {event.src_path}")
        logger.info("Rebuilding static site...")
        
        try:
            # Run the build_static_site.py script
            build_script = self.project_root / "build_static_site.py"
            subprocess.run(["python", str(build_script)], check=True)
            logger.info("Site rebuilt successfully!")
            self.last_build_time = time.time()
        except subprocess.CalledProcessError as e:
            logger.error(f"Error rebuilding site: {e}")

def watch_for_changes():
    """Watch for changes in the project directory and rebuild when needed."""
    project_root = Path(__file__).parent
    
    # Directories to watch
    watch_paths = [
        project_root / "examples",  # Example files
        project_root / "data",      # JSON data files
        project_root / "build_examples"  # Build scripts
    ]
    
    # Create observer and event handler
    observer = Observer()
    event_handler = ExampleChangeHandler(project_root)
    
    # Add watched directories
    for path in watch_paths:
        if path.exists():
            logger.info(f"Watching {path} for changes")
            observer.schedule(event_handler, str(path), recursive=True)
        else:
            logger.warning(f"Directory {path} does not exist, skipping")
    
    # Start the observer
    observer.start()
    logger.info("File watcher started. Press Ctrl+C to stop.")
    
    try:
        # Run an initial build
        build_script = project_root / "build_static_site.py"
        subprocess.run(["python", str(build_script)], check=True)
        logger.info("Initial site build complete!")
        
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping file watcher...")
        observer.stop()
    finally:
        observer.join()

if __name__ == "__main__":
    watch_for_changes()