#!/usr/bin/env python3
"""
Quick Font Fix for awards-tracker.py
"""

awards_tracker_path = "/home/jjesse/github/nfL-stats-dashboard/src/data-processors/awards-tracker.py"

# Read the current file
with open(awards_tracker_path, 'r') as f:
    content = f.read()

# Replace the problematic font configuration with the standard one
import re

# Remove old configurations
old_patterns = [
    r"# Configure matplotlib for emoji support.*?\n",
    r"plt\.rcParams\['font\.family'\] = \['Noto Color Emoji'.*?\]\n",
]

for pattern in old_patterns:
    content = re.sub(pattern, '', content, flags=re.DOTALL)

# Find the matplotlib.pyplot import and add proper font config after it
plt_import_pattern = r'(import matplotlib\.pyplot as plt\n)'

if re.search(plt_import_pattern, content):
    standard_config = '''
import warnings

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
    content = re.sub(plt_import_pattern, standard_config, content)

# Write the updated content back
with open(awards_tracker_path, 'w') as f:
    f.write(content)

print("✅ Fixed awards-tracker.py font configuration")