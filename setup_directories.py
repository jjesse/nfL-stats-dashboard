#!/usr/bin/env python3
"""
Directory Setup Script
Ensures proper directory structure for NFL Stats Dashboard
"""

import os
from pathlib import Path

def setup_directories():
    """Set up the required directory structure"""
    
    print("🏈 Setting up NFL Stats Dashboard directories...")
    
    # Define paths
    project_root = Path(__file__).parent
    docs_dir = project_root / "docs"
    archive_dir = project_root / "archive"
    
    print(f"Project root: {project_root}")
    
    # Check and handle archive file/directory issue
    if archive_dir.exists() and not archive_dir.is_dir():
        print(f"⚠️  Found file named 'archive' - removing to create directory")
        archive_dir.unlink()  # Remove the file
    
    # Create directories
    directories = [docs_dir, archive_dir]
    
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created/verified: {directory}")
        except Exception as e:
            print(f"❌ Error creating {directory}: {e}")
            return False
    
    # Create subdirectories if needed
    src_dirs = [
        project_root / "src" / "data-processors",
        project_root / "src" / "charts"
    ]
    
    for directory in src_dirs:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created/verified: {directory}")
        except Exception as e:
            print(f"❌ Error creating {directory}: {e}")
            return False
    
    print("\n🎉 Directory setup complete!")
    return True

if __name__ == "__main__":
    setup_directories()