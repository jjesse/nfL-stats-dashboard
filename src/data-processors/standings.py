#!/usr/bin/env python3
"""
NFL Standings Processor
Fetches and processes NFL team standings data with proper division/conference structure.
This processor generates clean standings data that works with the standings.html page.
"""

import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Safe matplotlib configuration - must be before pyplot import
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

# Configure matplotlib for dark theme
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


class NFLStandingsProcessor:
    def __init__(self):
        self.base_url = "https://www.pro-football-reference.com"
        self.current_season = self.get_current_nfl_season()
        self.docs_dir = Path(__file__).parent.parent.parent / "docs"
        self.archive_dir = Path(__file__).parent.parent.parent / "archive"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # NFL team to division mapping (using Pro Football Reference abbreviations)
        self.team_divisions = {
            # AFC East
            'Buffalo Bills': 'AFC East',
            'Miami Dolphins': 'AFC East',
            'New England Patriots': 'AFC East',
            'New York Jets': 'AFC East',
            # AFC North
            'Baltimore Ravens': 'AFC North',
            'Cincinnati Bengals': 'AFC North',
            'Cleveland Browns': 'AFC North',
            'Pittsburgh Steelers': 'AFC North',
            # AFC South
            'Houston Texans': 'AFC South',
            'Indianapolis Colts': 'AFC South',
            'Jacksonville Jaguars': 'AFC South',
            'Tennessee Titans': 'AFC South',
            # AFC West
            'Denver Broncos': 'AFC West',
            'Kansas City Chiefs': 'AFC West',
            'Las Vegas Raiders': 'AFC West',
            'Los Angeles Chargers': 'AFC West',
            # NFC East
            'Dallas Cowboys': 'NFC East',
            'New York Giants': 'NFC East',
            'Philadelphia Eagles': 'NFC East',
            'Washington Commanders': 'NFC East',
            # NFC North
            'Chicago Bears': 'NFC North',
            'Detroit Lions': 'NFC North',
            'Green Bay Packers': 'NFC North',
            'Minnesota Vikings': 'NFC North',
            # NFC South
            'Atlanta Falcons': 'NFC South',
            'Carolina Panthers': 'NFC South',
            'New Orleans Saints': 'NFC South',
            'Tampa Bay Buccaneers': 'NFC South',
            # NFC West
            'Arizona Cardinals': 'NFC West',
            'Los Angeles Rams': 'NFC West',
            'San Francisco 49ers': 'NFC West',
            'Seattle Seahawks': 'NFC West',
        }

        print(f"🏈 NFL Standings Processor - {self.current_season} Season")

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

    def fetch_standings_data(self):
        """Fetch NFL team standings from Pro Football Reference"""
        try:
            url = f"{self.base_url}/years/{self.current_season}/"
            print(f"📊 Fetching standings from: {url}")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            # Parse HTML tables
            tables = pd.read_html(response.content)

            # Look for the main standings table
            for table in tables:
                if 'W' in table.columns and 'L' in table.columns and 'Tm' in table.columns:
                    # Clean up multi-level columns if present
                    if table.columns.nlevels > 1:
                        table.columns = table.columns.droplevel(0)

                    # Remove header rows and NaN teams
                    clean_table = table[table['Tm'].notna()].copy()
                    clean_table = clean_table[clean_table['Tm'] != 'Tm']

                    # Filter out division header rows (they appear in all columns)
                    # Division headers have division name in all columns
                    clean_table = clean_table[~clean_table['W'].isin(['AFC East', 'AFC North', 'AFC South', 'AFC West',
                                                                      'NFC East', 'NFC North', 'NFC South', 'NFC West'])]

                    if len(clean_table) >= 20:  # Should have most/all NFL teams
                        print(f"✅ Found standings table with {len(clean_table)} teams")
                        return clean_table

            print("❌ No suitable standings table found")
            return pd.DataFrame()

        except Exception as e:
            print(f"❌ Error fetching standings: {e}")
            return pd.DataFrame()

    def process_standings_data(self, df):
        """Process and enhance standings data with division/conference info"""
        if df.empty:
            print("❌ No standings data to process")
            return df

        try:
            df = df.copy()

            # Clean team names (remove playoff indicators like * or +)
            if 'Tm' in df.columns:
                df['Team'] = df['Tm'].str.replace(r'[*+]', '', regex=True).str.strip()

            # Add division and conference based on team name
            df['Division'] = df['Team'].map(self.team_divisions).fillna('Unknown')
            df['Conference'] = df['Division'].apply(
                lambda x: 'AFC' if x.startswith('AFC') else 'NFC' if x.startswith('NFC') else 'Unknown'
            )

            # Ensure numeric columns are properly typed
            numeric_cols = ['W', 'L', 'W-L%', 'PF', 'PA', 'PD', 'MoV']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Add ties column if not present
            if 'T' not in df.columns:
                df['T'] = 0
            else:
                df['T'] = pd.to_numeric(df['T'], errors='coerce').fillna(0)

            # Sort by division and then by wins (descending)
            df = df.sort_values(['Conference', 'Division', 'W'], ascending=[True, True, False])

            print(f"✅ Processed {len(df)} teams across {df['Division'].nunique()} divisions")

            return df

        except Exception as e:
            print(f"❌ Error processing standings: {e}")
            import traceback
            traceback.print_exc()
            return df

    def save_standings_data(self, df):
        """Save standings data to CSV files"""
        if df.empty:
            print("❌ No data to save")
            return

        try:
            # Save current standings
            standings_file = self.docs_dir / "team_standings.csv"
            df.to_csv(standings_file, index=False)
            print(f"✅ Standings saved to {standings_file}")

            # Save to archive with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_file = self.archive_dir / f"team_standings_{timestamp}.csv"
            df.to_csv(archive_file, index=False)
            print(f"✅ Archive saved to {archive_file}")

            # Update timestamp file
            timestamp_file = self.docs_dir / "last_updated_standings.txt"
            with open(timestamp_file, 'w') as f:
                f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        except Exception as e:
            print(f"❌ Error saving data: {e}")

    def create_standings_visualization(self, df):
        """Create standings visualization charts"""
        if df.empty:
            print("❌ No data available for visualization")
            return

        try:
            plt.style.use('dark_background')
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle(f'🏈 NFL {self.current_season} Standings Overview',
                         fontsize=16, color='white', y=0.98)

            # 1. Conference Win Percentages
            if 'Conference' in df.columns and 'W-L%' in df.columns:
                conf_data = df.groupby('Conference')['W-L%'].mean()
                axes[0, 0].bar(conf_data.index, conf_data.values,
                               color=['#FF6B35', '#004E89'], alpha=0.8)
                axes[0, 0].set_title('Average Win % by Conference', fontsize=12)
                axes[0, 0].set_ylabel('Win Percentage')
                axes[0, 0].grid(True, alpha=0.3, axis='y')

            # 2. Division Leaders
            if 'Division' in df.columns and 'W-L%' in df.columns:
                div_leaders = df.loc[df.groupby('Division')['W-L%'].idxmax()]
                div_leaders = div_leaders.sort_values('W-L%', ascending=True)

                colors = ['#FF6B35' if c == 'AFC' else '#004E89'
                          for c in div_leaders['Conference']]

                axes[0, 1].barh(range(len(div_leaders)), div_leaders['W-L%'],
                                color=colors, alpha=0.8)
                axes[0, 1].set_yticks(range(len(div_leaders)))
                axes[0, 1].set_yticklabels([f"{row['Team']}" for _, row in div_leaders.iterrows()])
                axes[0, 1].set_title('Division Leaders', fontsize=12)
                axes[0, 1].set_xlabel('Win Percentage')
                axes[0, 1].grid(True, alpha=0.3, axis='x')

            # 3. Points Scored vs Allowed
            if 'PF' in df.columns and 'PA' in df.columns:
                colors = ['#FF6B35' if c == 'AFC' else '#004E89'
                          for c in df['Conference']]

                axes[1, 0].scatter(df['PF'], df['PA'], c=colors, alpha=0.7,
                                   s=100, edgecolors='white', linewidth=1)

                # Add diagonal line
                max_pts = max(df['PF'].max(), df['PA'].max())
                min_pts = min(df['PF'].min(), df['PA'].min())
                axes[1, 0].plot([min_pts, max_pts], [min_pts, max_pts],
                                'r--', alpha=0.5, linewidth=2)

                axes[1, 0].set_xlabel('Points For')
                axes[1, 0].set_ylabel('Points Against')
                axes[1, 0].set_title('Offensive vs Defensive Performance', fontsize=12)
                axes[1, 0].grid(True, alpha=0.3)

            # 4. Top Teams by Point Differential
            if 'PD' in df.columns:
                top_teams = df.nlargest(10, 'PD')
                colors = ['#2ECC71' if pd > 0 else '#E74C3C'
                          for pd in top_teams['PD']]

                axes[1, 1].barh(range(len(top_teams)), top_teams['PD'],
                                color=colors, alpha=0.8)
                axes[1, 1].set_yticks(range(len(top_teams)))
                axes[1, 1].set_yticklabels([f"{row['Team']}" for _, row in top_teams.iterrows()])
                axes[1, 1].set_title('Top Point Differentials', fontsize=12)
                axes[1, 1].set_xlabel('Point Differential')
                axes[1, 1].axvline(x=0, color='white', linestyle='-', alpha=0.5)
                axes[1, 1].grid(True, alpha=0.3, axis='x')

            plt.tight_layout()

            # Save chart
            chart_path = self.docs_dir / "standings_overview.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='black')
            plt.close()

            print(f"✅ Standings visualization saved to {chart_path}")

        except Exception as e:
            print(f"❌ Error creating visualization: {e}")
            import traceback
            traceback.print_exc()

    def process_all(self):
        """Main processing function"""
        print("🏈 NFL STANDINGS PROCESSOR")
        print("=" * 60)
        print(f"Processing {self.current_season} NFL season standings...")
        print()

        try:
            # Fetch standings data
            df = self.fetch_standings_data()

            if not df.empty:
                # Process the data
                df_processed = self.process_standings_data(df)

                # Save data
                self.save_standings_data(df_processed)

                # Create visualizations
                self.create_standings_visualization(df_processed)

                print()
                print("=" * 60)
                print("✅ Standings processing complete!")
                print(f"📊 Total teams: {len(df_processed)}")
                if 'Division' in df_processed.columns:
                    print(f"📁 Divisions: {df_processed['Division'].nunique()}")
                    for div in sorted(df_processed['Division'].unique()):
                        if div != 'Unknown':
                            team_count = len(df_processed[df_processed['Division'] == div])
                            print(f"   {div}: {team_count} teams")
            else:
                print("❌ No standings data available")

        except Exception as e:
            print(f"❌ Error in standings processing: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Main entry point"""
    processor = NFLStandingsProcessor()
    processor.process_all()


if __name__ == "__main__":
    main()
