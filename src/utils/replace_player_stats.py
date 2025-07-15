import os
import shutil

# Replace the broken file with the fixed version
broken_file = "/home/jjesse/github/nfL-stats-dashboard/src/data-processors/player-stats.py"
fixed_file = "/home/jjesse/github/nfL-stats-dashboard/src/data-processors/player-stats-fixed.py"

if os.path.exists(fixed_file):
    shutil.copy2(fixed_file, broken_file)
    os.remove(fixed_file)
    print("✅ Successfully replaced player-stats.py with fixed version")
else:
    print("❌ Fixed file not found")