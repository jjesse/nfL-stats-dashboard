#!/usr/bin/env python3
"""
Font Configuration for NFL Stats Dashboard
Standardizes matplotlib fonts to prevent errors across different systems

Usage:
    from utils.font_config import setup_fonts
    setup_fonts()  # Call this before any matplotlib operations
"""

import matplotlib.pyplot as plt
import matplotlib
import warnings

def setup_fonts():
    """
    Configure matplotlib to use reliable, cross-platform fonts
    Call this function before creating any plots
    """
    # Suppress font warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
    warnings.filterwarnings("ignore", category=RuntimeWarning, module="matplotlib")
    
    # Set backend to Agg for headless environments
    try:
        matplotlib.use('Agg')
    except:
        pass  # If backend is already set, continue
    
    # Configure reliable fonts that exist on most systems
    plt.rcParams['font.family'] = ['DejaVu Sans', 'Liberation Sans', 'Arial', 'Helvetica', 'sans-serif']
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans', 'Arial', 'Helvetica', 'Bitstream Vera Sans', 'sans-serif']
    plt.rcParams['font.size'] = 10
    
    # Configure figure settings for dark theme
    plt.rcParams['figure.facecolor'] = 'black'
    plt.rcParams['axes.facecolor'] = 'black'
    plt.rcParams['savefig.facecolor'] = 'black'
    plt.rcParams['savefig.edgecolor'] = 'none'
    
    # Text and axis colors for dark theme
    plt.rcParams['text.color'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'
    plt.rcParams['axes.edgecolor'] = 'white'
    
    # Grid settings
    plt.rcParams['grid.color'] = 'gray'
    plt.rcParams['grid.alpha'] = 0.3
    
    # Legend settings
    plt.rcParams['legend.facecolor'] = 'black'
    plt.rcParams['legend.edgecolor'] = 'white'
    
    print("✅ Matplotlib fonts configured for cross-platform compatibility")

def safe_title(text):
    """
    Create titles that work across different systems
    Removes problematic Unicode characters if needed
    """
    try:
        return text
    except UnicodeEncodeError:
        # Remove non-ASCII characters as fallback
        return text.encode('ascii', 'ignore').decode('ascii')

# Auto-configure when module is imported
setup_fonts()