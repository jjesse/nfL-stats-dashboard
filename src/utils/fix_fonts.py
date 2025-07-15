#!/usr/bin/env python3
"""
Font Fix Script - Updates all NFL stats processors with standardized fonts
Run this to fix font errors across all data processors
"""

import os
from pathlib import Path

def update_file_fonts(file_path):
    """Update a single file with standardized font configuration"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Standard font configuration to inject
        font_config = '''import warnings

# Suppress font warnings and configure safe fonts
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
import matplotlib
matplotlib.use('Agg')

# Configure reliable fonts that exist on most systems
plt.rcParams['font.family'] = ['DejaVu Sans', 'Liberation Sans', 'Arial', 'Helvetica', 'sans-serif']
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans', 'Arial', 'Helvetica', 'Bitstream Vera Sans']
plt.rcParams['font.size'] = 10
plt.rcParams['figure.facecolor'] = 'black'
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['savefig.facecolor'] = 'black'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['axes.edgecolor'] = 'white'
'''
        
        # Remove old font configurations
        lines = content.split('\n')
        new_lines = []
        skip_next = False
        
        for i, line in enumerate(lines):
            # Skip problematic font configurations
            if any(font_issue in line for font_issue in [
                "font.family'] = ['Noto Color Emoji",
                "font.family'] = ['Noto Emoji", 
                "Configure matplotlib for emoji",
                "matplotlib for better charts",
                "plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial'"
            ]):
                continue
                
            # Insert our font config after matplotlib import
            if line.strip() == 'import matplotlib.pyplot as plt' and i < len(lines) - 1:
                new_lines.append(line)
                new_lines.append(font_config)
                continue
                
            new_lines.append(line)
        
        # Write back
        with open(file_path, 'w') as f:
            f.write('\n'.join(new_lines))
            
        print(f"✅ Updated fonts in {file_path.name}")
        
    except Exception as e:
        print(f"❌ Error updating {file_path.name}: {e}")

def main():
    """Update all Python files in the NFL stats dashboard"""
    base_dir = Path(__file__).parent.parent
    
    # Files to update
    files_to_update = [
        base_dir / "data-processors" / "player-stats.py",
        base_dir / "data-processors" / "team-stats-basic.py", 
        base_dir / "data-processors" / "team-weekly-trends.py",
        base_dir / "data-processors" / "awards-tracker.py",
        base_dir / "charts" / "team-charts.py"
    ]
    
    print("🔧 NFL Stats Dashboard Font Fixer")
    print("=" * 50)
    print("Updating matplotlib font configurations...")
    
    for file_path in files_to_update:
        if file_path.exists():
            update_file_fonts(file_path)
        else:
            print(f"⚠️ File not found: {file_path}")
    
    print("\n✅ Font configuration update complete!")
    print("All processors should now use safe, cross-platform fonts")
    print("=" * 50)

if __name__ == "__main__":
    main()