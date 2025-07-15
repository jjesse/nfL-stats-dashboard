#!/usr/bin/env python3
"""
Font Standardization Script for NFL Stats Dashboard
Ensures all processors use identical, error-free font configuration
"""

import os
import re
from pathlib import Path

def get_standard_font_config():
    """Return the exact font configuration that works"""
    return '''# COMPREHENSIVE warning suppression
warnings.filterwarnings("ignore")

# Safe matplotlib configuration
import matplotlib
matplotlib.use('Agg')

# MINIMAL font configuration - only DejaVu Sans
plt.rcParams['font.family'] = ['DejaVu Sans']
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
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

def fix_font_config(file_path):
    """Standardize font configuration in a single file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        if 'matplotlib.pyplot' not in content:
            return False, "Not a matplotlib file"
        
        # Remove ALL existing font configurations
        patterns_to_remove = [
            # Remove old warning suppressions
            r'warnings\.filterwarnings\("ignore".*?\)\n',
            r'warnings\.filterwarnings\("ignore"\)\n',
            
            # Remove matplotlib configs
            r'import matplotlib\nmatplotlib\.use\(\'Agg\'\)\n',
            r'matplotlib\.use\(\'Agg\'\)\n',
            
            # Remove font configurations
            r'plt\.rcParams\[\'font\.family\'\] = \[.*?\]\n',
            r'plt\.rcParams\[\'font\.sans-serif\'\] = \[.*?\]\n',
            r'plt\.rcParams\[\'font\.size\'\] = .*?\n',
            r'plt\.rcParams\[\'figure\.facecolor\'\] = .*?\n',
            r'plt\.rcParams\[\'axes\.facecolor\'\] = .*?\n',
            r'plt\.rcParams\[\'savefig\.facecolor\'\] = .*?\n',
            r'plt\.rcParams\[\'text\.color\'\] = .*?\n',
            r'plt\.rcParams\[\'axes\.labelcolor\'\] = .*?\n',
            r'plt\.rcParams\[\'xtick\.color\'\] = .*?\n',
            r'plt\.rcParams\[\'ytick\.color\'\] = .*?\n',
            r'plt\.rcParams\[\'axes\.edgecolor\'\] = .*?\n',
            
            # Remove comment blocks
            r'# Suppress font warnings.*?\n',
            r'# Safe matplotlib configuration.*?\n',
            r'# Configure.*?fonts.*?\n',
            r'# MINIMAL font configuration.*?\n',
            r'# COMPREHENSIVE warning suppression.*?\n',
        ]
        
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.MULTILINE)
        
        # Clean up extra blank lines
        content = re.sub(r'\n\n\n+', '\n\n', content)
        
        # Find where to insert the standard configuration
        # Insert after the last import but before the class definition
        
        # Find the position after matplotlib.pyplot import
        plt_pattern = r'(import matplotlib\.pyplot as plt\n)'
        match = re.search(plt_pattern, content)
        
        if match:
            # Insert standard config after pyplot import
            insert_pos = match.end()
            new_content = (
                content[:insert_pos] + 
                '\n' + get_standard_font_config() + '\n' + 
                content[insert_pos:]
            )
        else:
            return False, "Could not find matplotlib.pyplot import"
        
        # Write back
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        return True, "Font configuration standardized"
        
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Standardize fonts across all NFL processors"""
    base_dir = Path(__file__).parent.parent
    
    files_to_fix = [
        base_dir / "data-processors" / "team-stats-basic.py",
        base_dir / "data-processors" / "player-stats.py",
        base_dir / "data-processors" / "team-weekly-trends.py", 
        base_dir / "data-processors" / "awards-tracker.py",
        base_dir / "charts" / "team-charts.py",
        base_dir / "analysis" / "awards_accuracy_tracker.py"
    ]
    
    print("🔧 NFL Stats Font Standardization")
    print("=" * 50)
    print("Applying identical font configuration to all processors...")
    
    success_count = 0
    
    for file_path in files_to_fix:
        if file_path.exists():
            success, message = fix_font_config(file_path)
            status = "✅" if success else "❌"
            print(f"{status} {file_path.name}: {message}")
            if success:
                success_count += 1
        else:
            print(f"⚠️ {file_path.name}: File not found")
    
    print("\n" + "=" * 50)
    print(f"✅ Font standardization complete! ({success_count}/{len(files_to_fix)} files updated)")
    print("\nStandardized configuration:")
    print("• DejaVu Sans font only")
    print("• All warnings suppressed") 
    print("• Agg backend for headless operation")
    print("• Dark theme colors")
    print("• No emoji fonts (prevents glyph warnings)")
    
    print("\n🧪 Test your processors now:")
    for file_path in files_to_fix:
        if file_path.exists():
            print(f"  python {file_path}")

if __name__ == "__main__":
    main()