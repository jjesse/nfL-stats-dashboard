#!/usr/bin/env python3
"""
NFL Schedule and Results Processor
Fetches and processes NFL schedule and game results including:
- Weekly game schedule
- Game results and scores
- Team performance by week
- Season schedule overview
"""

import warnings
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

# Safe matplotlib configuration - must be before pyplot import
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

# COMPREHENSIVE warning suppression
warnings.filterwarnings("ignore")

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


class NFLScheduleProcessor:
    def __init__(self):
        self.base_url = "https://www.pro-football-reference.com"
        self.current_season = self.get_current_nfl_season()
        self.docs_dir = Path(__file__).parent.parent.parent / "docs"
        self.archive_dir = Path(__file__).parent.parent.parent / "archive"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print(f"🏈 NFL Schedule Processor - {self.current_season} Season")

        # Create directories if they don't exist
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)

    def get_current_nfl_season(self):
        """Determine the current/most recent NFL season"""
        now = datetime.now()
        if now.month <= 7:
            return now.year - 1
        else:
            return now.year

    def fetch_schedule_data(self):
        """Fetch NFL schedule and game results"""
        try:
            url = f"{self.base_url}/years/{self.current_season}/games.htm"
            print(f"📅 Fetching schedule from: {url}")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            # Parse the HTML and extract table data
            tables = pd.read_html(response.content)
            if tables:
                # The games table is usually the first one
                df = tables[0]

                # Clean up column names if multi-level
                if df.columns.nlevels > 1:
                    df.columns = df.columns.droplevel(0)

                # Remove rows with NaN weeks (playoff games or separators)
                df = df[df['Week'].notna()]
                df = df[df['Week'] != 'Week']  # Remove header rows

                print(f"✅ Found {len(df)} games")
                return df

            return pd.DataFrame()
        except Exception as e:
            print(f"❌ Error fetching schedule: {e}")
            return pd.DataFrame()

    def process_schedule_data(self, df):
        """Process and clean schedule data"""
        if df.empty:
            print("❌ No schedule data to process")
            return df

        try:
            # Map Pro Football Reference columns to our format
            column_mapping = {
                'Week': 'Week',
                'Day': 'Day',
                'Date': 'Date',
                'Time': 'Time',
                'Winner/tie': 'Winner',
                'Loser/tie': 'Loser',
                '@': 'Location',
                'PtsW': 'Winner_Pts',
                'PtsL': 'Loser_Pts',
                'TOW': 'Winner_TO',
                'TOL': 'Loser_TO'
            }

            # Rename columns that exist
            df_clean = df.copy()
            for orig_col, new_col in column_mapping.items():
                if orig_col in df_clean.columns:
                    df_clean = df_clean.rename(columns={orig_col: new_col})

            # Determine home and away teams based on Location column
            # '@' means the winner was away, blank means winner was home
            def assign_teams_and_scores(row):
                """Helper to assign home/away teams and scores based on location"""
                result = {
                    'Away_Team': '', 'Home_Team': '',
                    'Away_Score': '', 'Home_Score': ''
                }

                if pd.notna(row.get('Winner')) and pd.notna(row.get('Loser')):
                    # If Location is '@', winner was away
                    if row.get('Location') == '@':
                        result['Away_Team'] = row['Winner']
                        result['Home_Team'] = row['Loser']
                        result['Away_Score'] = row.get('Winner_Pts', '')
                        result['Home_Score'] = row.get('Loser_Pts', '')
                    else:
                        # Winner was home
                        result['Home_Team'] = row['Winner']
                        result['Away_Team'] = row['Loser']
                        result['Home_Score'] = row.get('Winner_Pts', '')
                        result['Away_Score'] = row.get('Loser_Pts', '')

                return pd.Series(result)

            # Apply the assignment function to all rows
            team_cols = df_clean.apply(assign_teams_and_scores, axis=1)
            df_clean[['Away_Team', 'Home_Team', 'Away_Score', 'Home_Score']] = team_cols

            # Add game status (Final for completed, Scheduled for upcoming)
            if 'Winner_Pts' in df_clean.columns:
                df_clean['Status'] = df_clean['Winner_Pts'].apply(
                    lambda x: 'Final' if pd.notna(x) and str(x).strip() != '' else 'Scheduled'
                )
            else:
                df_clean['Status'] = 'Scheduled'

            # Add default Time if not present
            if 'Time' not in df_clean.columns:
                df_clean['Time'] = 'TBD'

            # Select only the columns needed for the web interface
            output_columns = ['Week', 'Date', 'Time', 'Away_Team', 'Away_Score',
                              'Home_Team', 'Home_Score', 'Winner', 'Status']

            # Keep only columns that exist
            final_columns = [col for col in output_columns if col in df_clean.columns]
            df_clean = df_clean[final_columns]

            print(f"✅ Processed {len(df_clean)} games")
            return df_clean

        except Exception as e:
            print(f"❌ Error processing schedule: {e}")
            import traceback
            traceback.print_exc()
            return df

    def create_schedule_visualization(self, df):
        """Create visualization for schedule data"""
        if df.empty:
            print("❌ No data available for schedule visualization")
            return

        try:
            plt.style.use('dark_background')
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle(f'🏈 NFL {self.current_season} Schedule Overview', fontsize=16, color='white')

            # Count games by week
            if 'Week' in df.columns:
                week_counts = df['Week'].value_counts().sort_index()
                axes[0, 0].bar(range(len(week_counts)), week_counts.values, color='steelblue', alpha=0.8)
                axes[0, 0].set_title('Games per Week', fontsize=12)
                axes[0, 0].set_xlabel('Week')
                axes[0, 0].set_ylabel('Number of Games')
                axes[0, 0].grid(True, alpha=0.3, axis='y')

            # Count games by status
            if 'Status' in df.columns:
                status_counts = df['Status'].value_counts()
                colors = ['#2ECC71' if s == 'Completed' else '#F39C12' for s in status_counts.index]
                axes[0, 1].bar(range(len(status_counts)), status_counts.values, color=colors, alpha=0.8)
                axes[0, 1].set_title('Game Status', fontsize=12)
                axes[0, 1].set_xticks(range(len(status_counts)))
                axes[0, 1].set_xticklabels(status_counts.index, rotation=0)
                axes[0, 1].set_ylabel('Number of Games')
                axes[0, 1].grid(True, alpha=0.3, axis='y')

            # Games by day of week
            if 'Day' in df.columns:
                day_counts = df['Day'].value_counts()
                axes[1, 0].bar(range(len(day_counts)), day_counts.values, color='coral', alpha=0.8)
                axes[1, 0].set_title('Games by Day of Week', fontsize=12)
                axes[1, 0].set_xticks(range(len(day_counts)))
                axes[1, 0].set_xticklabels(day_counts.index, rotation=45, ha='right')
                axes[1, 0].set_ylabel('Number of Games')
                axes[1, 0].grid(True, alpha=0.3, axis='y')

            # Average scores (if available)
            if 'Winner_Pts' in df.columns and 'Loser_Pts' in df.columns:
                completed_games = df[df['Status'] == 'Completed'].copy()
                if not completed_games.empty:
                    completed_games['Winner_Pts'] = pd.to_numeric(completed_games['Winner_Pts'], errors='coerce')
                    completed_games['Loser_Pts'] = pd.to_numeric(completed_games['Loser_Pts'], errors='coerce')
                    completed_games = completed_games.dropna(subset=['Winner_Pts', 'Loser_Pts'])

                    if not completed_games.empty:
                        completed_games['Total_Pts'] = completed_games['Winner_Pts'] + completed_games['Loser_Pts']
                        avg_total = completed_games['Total_Pts'].mean()

                        axes[1, 1].hist(completed_games['Total_Pts'], bins=15, color='skyblue', alpha=0.7, edgecolor='white')
                        axes[1, 1].axvline(avg_total, color='red', linestyle='--', linewidth=2, label=f'Avg: {avg_total:.1f}')
                        axes[1, 1].set_title('Total Points Distribution', fontsize=12)
                        axes[1, 1].set_xlabel('Total Points')
                        axes[1, 1].set_ylabel('Frequency')
                        axes[1, 1].legend()
                        axes[1, 1].grid(True, alpha=0.3, axis='y')

            # Save the chart
            plt.tight_layout()
            chart_path = self.docs_dir / "schedule_overview.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='black')
            plt.close()

            print(f"✅ Schedule visualization saved to {chart_path}")

        except Exception as e:
            print(f"❌ Error creating schedule visualization: {e}")

    def save_data(self, df):
        """Save schedule data to CSV files"""
        if df.empty:
            print("❌ No data to save")
            return

        try:
            # Save current data
            current_file = self.docs_dir / "schedule_results.csv"
            df.to_csv(current_file, index=False)
            print(f"✅ Schedule data saved to {current_file}")

            # Save to archive with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_file = self.archive_dir / f"schedule_results_{timestamp}.csv"
            df.to_csv(archive_file, index=False)
            print(f"✅ Archive saved to {archive_file}")

            # Update timestamp file
            timestamp_file = self.docs_dir / "last_updated_schedule.txt"
            with open(timestamp_file, 'w') as f:
                f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        except Exception as e:
            print(f"❌ Error saving data: {e}")

    def process_all(self):
        """Main processing function"""
        print("🏈 NFL SCHEDULE PROCESSOR")
        print("=" * 60)
        print(f"Processing {self.current_season} NFL season schedule...")
        print()

        try:
            # Fetch schedule data
            df = self.fetch_schedule_data()

            if not df.empty:
                # Process the data
                df_processed = self.process_schedule_data(df)

                # Create visualizations
                self.create_schedule_visualization(df_processed)

                # Save data
                self.save_data(df_processed)

                print()
                print("=" * 60)
                print("✅ Schedule processing complete!")
                print(f"📊 Total games: {len(df_processed)}")
                if 'Status' in df_processed.columns:
                    status_counts = df_processed['Status'].value_counts()
                    for status, count in status_counts.items():
                        print(f"   {status}: {count}")
            else:
                print("❌ No schedule data available")

        except Exception as e:
            print(f"❌ Error in schedule processing: {e}")


def main():
    """Main entry point"""
    processor = NFLScheduleProcessor()
    processor.process_all()


if __name__ == "__main__":
    main()
