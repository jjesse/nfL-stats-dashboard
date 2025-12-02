#!/usr/bin/env python3
"""
Master NFL Data Processor Script
Runs all data processors in sequence to generate complete NFL statistics dashboard data.

This script orchestrates:
- Player statistics (passing, rushing, receiving, defense)
- Team statistics (standings, offense, defense)
- Team charts and analytics
- Team weekly trends and momentum
- Schedule and game results
- Awards predictions (MVP, OROY, DROY)
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

# Import all processors
try:
    from player_stats import NFLPlayerStats
    from team_stats_basic import BasicNFLTeamStats
    from team_charts import NFLTeamCharts
    from team_weekly_trends import NFLTeamWeeklyTrends
    from schedule_processor import NFLScheduleProcessor
    from awards_tracker import NFLAwardsTracker

    PROCESSORS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Warning: Some processors could not be imported: {e}")
    print("Will attempt to run individual processors...")
    PROCESSORS_AVAILABLE = False


class MasterProcessor:
    """Orchestrates all NFL data processors"""

    def __init__(self):
        self.start_time = datetime.now()
        self.results = {
            'success': [],
            'failed': [],
            'skipped': []
        }

    def print_header(self):
        """Print header banner"""
        print("=" * 80)
        print(" " * 20 + "🏈 NFL STATS DASHBOARD - MASTER PROCESSOR")
        print("=" * 80)
        print(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print()

    def print_separator(self):
        """Print section separator"""
        print()
        print("-" * 80)
        print()

    def run_processor(self, name, processor_func):
        """Run a single processor and track results"""
        print(f"▶️ Starting {name}...")
        print()

        try:
            start = time.time()
            processor_func()
            elapsed = time.time() - start

            self.results['success'].append({
                'name': name,
                'time': elapsed
            })

            print()
            print(f"✅ {name} completed in {elapsed:.2f}s")
            return True

        except Exception as e:
            self.results['failed'].append({
                'name': name,
                'error': str(e)
            })

            print()
            print(f"❌ {name} failed: {e}")
            return False

    def run_all_object_based(self):
        """Run all processors using imported classes"""
        processors = [
            ("Player Statistics", lambda: NFLPlayerStats().process_all_stats()),
            ("Team Statistics", lambda: BasicNFLTeamStats().process_all()),
            ("Team Charts", lambda: NFLTeamCharts().process_all()),
            ("Team Weekly Trends", lambda: NFLTeamWeeklyTrends().process_all()),
            ("Schedule Processor", lambda: NFLScheduleProcessor().process_all()),
            ("Awards Tracker", lambda: NFLAwardsTracker().process_all())
        ]

        for name, processor_func in processors:
            self.print_separator()
            self.run_processor(name, processor_func)
            time.sleep(2)  # Brief pause between processors

    def run_all_subprocess(self):
        """Run all processors as separate subprocesses"""
        import subprocess

        scripts = [
            ("Player Statistics", "player-stats.py"),
            ("Team Statistics", "team-stats-basic.py"),
            ("Team Charts", "team-charts.py"),
            ("Team Weekly Trends", "team-weekly-trends.py"),
            ("Schedule Processor", "schedule-processor.py"),
            ("Awards Tracker", "awards-tracker.py")
        ]

        script_dir = Path(__file__).parent

        for name, script_name in scripts:
            self.print_separator()
            print(f"▶️ Starting {name} ({script_name})...")
            print()

            script_path = script_dir / script_name

            if not script_path.exists():
                print(f"⚠️ Script not found: {script_path}")
                self.results['skipped'].append({
                    'name': name,
                    'reason': 'Script file not found'
                })
                continue

            try:
                start = time.time()
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout per processor
                )
                elapsed = time.time() - start

                # Print the processor output
                if result.stdout:
                    print(result.stdout)

                if result.returncode == 0:
                    self.results['success'].append({
                        'name': name,
                        'time': elapsed
                    })
                    print()
                    print(f"✅ {name} completed in {elapsed:.2f}s")
                else:
                    self.results['failed'].append({
                        'name': name,
                        'error': result.stderr or 'Unknown error'
                    })
                    print()
                    print(f"❌ {name} failed:")
                    if result.stderr:
                        print(result.stderr)

            except subprocess.TimeoutExpired:
                self.results['failed'].append({
                    'name': name,
                    'error': 'Timeout (>5 minutes)'
                })
                print(f"❌ {name} timed out")

            except Exception as e:
                self.results['failed'].append({
                    'name': name,
                    'error': str(e)
                })
                print(f"❌ {name} failed: {e}")

            time.sleep(2)  # Brief pause between processors

    def print_summary(self):
        """Print execution summary"""
        self.print_separator()

        end_time = datetime.now()
        total_time = (end_time - self.start_time).total_seconds()

        print("=" * 80)
        print(" " * 30 + "📊 EXECUTION SUMMARY")
        print("=" * 80)
        print()

        print(f"Started:  {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Finished: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total time: {total_time:.2f}s ({total_time / 60:.1f} minutes)")
        print()

        # Success
        if self.results['success']:
            print(f"✅ Successful ({len(self.results['success'])})")
            for item in self.results['success']:
                print(f"   • {item['name']}: {item['time']:.2f}s")
            print()

        # Failed
        if self.results['failed']:
            print(f"❌ Failed ({len(self.results['failed'])})")
            for item in self.results['failed']:
                print(f"   • {item['name']}: {item['error']}")
            print()

        # Skipped
        if self.results['skipped']:
            print(f"⚠️ Skipped ({len(self.results['skipped'])})")
            for item in self.results['skipped']:
                print(f"   • {item['name']}: {item['reason']}")
            print()

        # Overall status
        total = len(self.results['success']) + len(self.results['failed']) + len(self.results['skipped'])
        success_rate = (len(self.results['success']) / total * 100) if total > 0 else 0

        print("=" * 80)
        if success_rate == 100:
            print(f"🎉 All processors completed successfully! ({success_rate:.0f}%)")
        elif success_rate >= 50:
            print(f"⚠️ Most processors completed ({success_rate:.0f}% success rate)")
        else:
            print(f"❌ Many processors failed ({success_rate:.0f}% success rate)")
        print("=" * 80)

        return success_rate >= 50  # Return True if at least 50% succeeded

    def run(self):
        """Main execution method"""
        self.print_header()

        # Try object-based execution first, fall back to subprocess
        if PROCESSORS_AVAILABLE:
            print("ℹ️ Running processors using direct imports...")
            print()
            self.run_all_object_based()
        else:
            print("ℹ️ Running processors as subprocesses...")
            print()
            self.run_all_subprocess()

        # Print summary
        success = self.print_summary()

        # Exit with appropriate code
        sys.exit(0 if success else 1)


def main():
    """Main entry point"""
    try:
        processor = MasterProcessor()
        processor.run()
    except KeyboardInterrupt:
        print()
        print()
        print("=" * 80)
        print("⚠️ Processing interrupted by user")
        print("=" * 80)
        sys.exit(1)
    except Exception as e:
        print()
        print()
        print("=" * 80)
        print(f"❌ Fatal error: {e}")
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
