#!/usr/bin/env python3
"""
Create accuracy summary for GitHub workflows
"""

import json
from pathlib import Path
from datetime import datetime

def create_accuracy_summary():
    """Create simple accuracy summary for workflows"""
    docs_dir = Path("docs")
    accuracy_file = docs_dir / "awards_accuracy_history.json"
    
    try:
        if accuracy_file.exists():
            with open(accuracy_file, 'r') as f:
                data = json.load(f)
            
            perf = data.get('model_performance', {})
            overall = perf.get('overall_accuracy', 0)
            total = perf.get('total_predictions', 0)
            correct = perf.get('total_correct', 0)
            
            summary = f"{overall:.1f}% accuracy ({correct}/{total} predictions)"
            
            # Create simple summary file
            with open(docs_dir / "accuracy_summary.txt", 'w') as f:
                f.write(summary)
            
            print(f"Accuracy summary created: {summary}")
            
            # Create alert if accuracy is low
            if overall < 40 and total > 0:
                with open(docs_dir / "accuracy_alert.txt", 'w') as f:
                    f.write(f"LOW ACCURACY ALERT: {overall:.1f}%")
                print(f"WARNING: Low accuracy detected ({overall:.1f}%)")
        else:
            with open(docs_dir / "accuracy_summary.txt", 'w') as f:
                f.write("No accuracy data available")
            print("No accuracy data found")
            
    except Exception as e:
        print(f"Error creating accuracy summary: {e}")
        with open(docs_dir / "accuracy_summary.txt", 'w') as f:
            f.write("Error generating accuracy data")

if __name__ == "__main__":
    create_accuracy_summary()