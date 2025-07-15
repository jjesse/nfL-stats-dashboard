#!/usr/bin/env python3
"""
Quick fix for player-stats.py import order
"""

import re

def fix_player_stats():
    file_path = "/home/jjesse/github/nfL-stats-dashboard/src/data-processors/player-stats.py"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # New standardized imports and configuration
    new_imports = '''import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import time
from pathlib import Path
import warnings

# COMPREHENSIVE warning suppression
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
    
    # Find the docstring end and replace everything up to the class definition
    docstring_end = content.find('"""', content.find('"""') + 3) + 3
    class_start = content.find('class NFLPlayerStats:')
    
    if docstring_end > 0 and class_start > 0:
        new_content = (
            content[:docstring_end] + 
            '\n\n' + 
            new_imports + 
            '\n\n' + 
            content[class_start:]
        )
        
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        print("✅ Fixed player-stats.py imports")
    else:
        print("❌ Could not find docstring or class definition")

if __name__ == "__main__":
    fix_player_stats()