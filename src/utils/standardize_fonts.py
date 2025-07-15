#!/usr/bin/env python3
"""
NFL Stats Font Standardization Script
Updates all data processors to use consistent, safe font configuration
"""

import os
import re
from pathlib import Path

def get_standard_font_config():
    """Return the standardized font configuration"""
    return '''import warnings

# Suppress font warnings and configure safe fonts
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
warnings.filterwarnings("ignore", category=RuntimeWarning, module="matplotlib")
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

def fix_file_fonts(file_path):
    """Fix font configuration in a single file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if it's a Python file that uses matplotlib
        if not content or 'matplotlib.pyplot' not in content:
            return False, "Not a matplotlib file"
        
        # Check if warnings import exists
        if 'import warnings' not in content:
            # Add warnings import after other imports
            import_pattern = r'(from pathlib import Path\n|import time\n|import sys\n)'
            content = re.sub(import_pattern, r'\1import warnings\n', content, count=1)
        
        # Remove old problematic font configurations
        patterns_to_remove = [
            r"plt\.rcParams\['font\.family'\] = \['Noto Color Emoji'.*?\]\n",
            r"# Configure matplotlib for emoji support\n",
            r"warnings\.filterwarnings\(\"ignore\", category=UserWarning, module=\"matplotlib\"\)\n",
            r"matplotlib\.use\('Agg'\)\n",
            r"plt\.rcParams\['font\.family'\] = \[.*?\]\n",
            r"plt\.rcParams\['font\.sans-serif'\] = \[.*?\]\n",
            r"plt\.rcParams\['font\.size'\] = \d+\n",
            r"plt\.rcParams\['figure\.facecolor'\] = 'black'\n",
            r"plt\.rcParams\['axes\.facecolor'\] = 'black'\n",
            r"plt\.rcParams\['savefig\.facecolor'\] = 'black'\n",
            r"plt\.rcParams\['text\.color'\] = 'white'\n",
            r"plt\.rcParams\['axes\.labelcolor'\] = 'white'\n",
            r"plt\.rcParams\['xtick\.color'\] = 'white'\n",
            r"plt\.rcParams\['ytick\.color'\] = 'white'\n",
            r"plt\.rcParams\['axes\.edgecolor'\] = 'white'\n",
        ]
        
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.MULTILINE)
        
        # Find where to insert the new font configuration
        # Look for the line right after matplotlib.pyplot import
        plt_import_pattern = r'(import matplotlib\.pyplot as plt\n)'
        
        if re.search(plt_import_pattern, content):
            # Insert the standard font configuration after matplotlib.pyplot import
            standard_config = get_standard_font_config()
            content = re.sub(plt_import_pattern, r'\1\n' + standard_config + '\n', content)
        else:
            return False, "Could not find matplotlib.pyplot import"
        
        # Write the updated content back
        with open(file_path, 'w') as f:
            f.write(content)
        
        return True, "Font configuration updated"
        
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Update all NFL stats processor files"""
    base_dir = Path(__file__).parent.parent
    
    files_to_fix = [
        base_dir / "data-processors" / "awards-tracker.py",
        base_dir / "data-processors" / "player-stats.py", 
        base_dir / "data-processors" / "team-stats-basic.py",
        base_dir / "data-processors" / "team-weekly-trends.py",
        base_dir / "charts" / "team-charts.py"
    ]
    
    print("🔧 NFL Stats Font Standardization")
    print("=" * 50)
    
    for file_path in files_to_fix:
        if file_path.exists():
            success, message = fix_file_fonts(file_path)
            status = "✅" if success else "❌"
            print(f"{status} {file_path.name}: {message}")
        else:
            print(f"⚠️ {file_path.name}: File not found")
    
    print("\n✅ Font standardization complete!")
    print("All processors should now use:")
    print("  - DejaVu Sans primary font")
    print("  - Comprehensive warning suppression")
    print("  - Dark theme configuration")
    print("  - No emoji fonts (no glyph warnings)")

if __name__ == "__main__":
    main()