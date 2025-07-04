import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from pathlib import Path

class NFLTeamStats:
    def __init__(self):
        self.base_url = "https://www.pro-football-reference.com"
        self.current_season = datetime.now().year
        self.docs_dir = Path(__file__).parent.parent.parent / "docs"
        self.archive_dir = Path(__file__).parent.parent.parent / "archive"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def fetch_team_stats(self):
        """Fetch team statistics"""
        try:
            url = f"{self.base_url}/years/{self.current_season}/"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            tables = pd.read_html(response.content)
            if tables:
                # Find the AFC and NFC standings tables
                afc_table = None
                nfc_table = None
                
                for i, table in enumerate(tables):
                    if 'AFC' in str(table.columns) or any('AFC' in str(col) for col in table.columns):
                        afc_table = table
                    elif 'NFC' in str(table.columns) or any('NFC' in str(col) for col in table.columns):
                        nfc_table = table
                
                # If we found separate tables, combine them
                if afc_table is not None and nfc_table is not None:
                    df = pd.concat([afc_table, nfc_table], ignore_index=True)
                else:
                    # Use the first table that looks like team stats
                    df = tables[0]
                
                # Clean up the dataframe
                if df.columns.nlevels > 1:
                    df.columns = df.columns.droplevel(0)
                
                return df
            return pd.DataFrame()
        except Exception as e:
            print(f"Error fetching team stats: {e}")
            return pd.DataFrame()
    
    def create_team_charts(self, df):
        """Create team visualization charts"""
        if df.empty:
            return
            
        plt.style.use('dark_background')
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'NFL Team Statistics - {self.current_season}', fontsize=16, color='white')
        
        try:
            # Points scored vs points allowed
            if 'PF' in df.columns and 'PA' in df.columns:
                df['PF'] = pd.to_numeric(df['PF'], errors='coerce')
                df['PA'] = pd.to_numeric(df['PA'], errors='coerce')
                axes[0, 0].scatter(df['PF'], df['PA'], alpha=0.7, color='#1f77b4', s=60)
                axes[0, 0].set_xlabel('Points For')
                axes[0, 0].set_ylabel('Points Against')
                axes[0, 0].set_title('Points For vs Points Against')
                axes[0, 0].grid(True, alpha=0.3)
                
                # Add team labels to points
                for i, row in df.iterrows():
                    if pd.notna(row['PF']) and pd.notna(row['PA']):
                        team_name = row.get('Tm', row.get('Team', f'Team {i}'))
                        axes[0, 0].annotate(team_name, (row['PF'], row['PA']), 
                                          xytext=(5, 5), textcoords='offset points', 
                                          fontsize=8, alpha=0.8)
                
            # Win percentage
            if 'W' in df.columns and 'L' in df.columns:
                df['W'] = pd.to_numeric(df['W'], errors='coerce')
                df['L'] = pd.to_numeric(df['L'], errors='coerce')
                df['Win_Pct'] = df['W'] / (df['W'] + df['L'])
                
                # Sort by win percentage and get top teams
                top_teams = df.nlargest(16, 'Win_Pct')  # Show all teams
                team_names = [row.get('Tm', row.get('Team', f'Team {i}')) for i, row in top_teams.iterrows()]
                
                axes[0, 1].bar(range(len(top_teams)), top_teams['Win_Pct'], color='#ff7f0e')
                axes[0, 1].set_title('Team Win Percentage')
                axes[0, 1].set_ylabel('Win Percentage')
                axes[0, 1].set_xticks(range(len(top_teams)))
                axes[0, 1].set_xticklabels(team_names, rotation=45, ha='right')
                
            # Point differential
            if 'PF' in df.columns and 'PA' in df.columns:
                df['Point_Diff'] = df['PF'] - df['PA']
                top_diff = df.nlargest(16, 'Point_Diff')
                team_names = [row.get('Tm', row.get('Team', f'Team {i}')) for i, row in top_diff.iterrows()]
                
                colors = ['#2ca02c' if x > 0 else '#d62728' for x in top_diff['Point_Diff']]
                axes[1, 0].bar(range(len(top_diff)), top_diff['Point_Diff'], color=colors)
                axes[1, 0].set_title('Point Differential')
                axes[1, 0].set_ylabel('Point Differential')
                axes[1, 0].set_xticks(range(len(top_diff)))
                axes[1, 0].set_xticklabels(team_names, rotation=45, ha='right')
                axes[1, 0].axhline(y=0, color='white', linestyle='-', alpha=0.3)
                
            # Wins vs Losses
            if 'W' in df.columns and 'L' in df.columns:
                team_names = [row.get('Tm', row.get('Team', f'Team {i}')) for i, row in df.iterrows()]
                
                x_pos = range(len(df))
                width = 0.35
                
                axes[1, 1].bar([x - width/2 for x in x_pos], df['W'], width, 
                             label='Wins', color='#2ca02c', alpha=0.8)
                axes[1, 1].bar([x + width/2 for x in x_pos], df['L'], width, 
                             label='Losses', color='#d62728', alpha=0.8)
                
                axes[1, 1].set_title('Wins vs Losses')
                axes[1, 1].set_ylabel('Games')
                axes[1, 1].set_xticks(x_pos)
                axes[1, 1].set_xticklabels(team_names, rotation=45, ha='right')
                axes[1, 1].legend()
                
        except Exception as e:
            print(f"Error creating team charts: {e}")
            
        plt.tight_layout()
        chart_path = self.docs_dir / "team_stats.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()
        
    def save_data(self, df):
        """Save team data"""
        if df.empty:
            return
            
        # Save current data
        current_file = self.docs_dir / "team_stats.csv"
        df.to_csv(current_file, index=False)
        
        # Save to archive
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = self.archive_dir / f"team_stats_{timestamp}.csv"
        df.to_csv(archive_file, index=False)
        
        # Update timestamp
        timestamp_file = self.docs_dir / "last_updated_teams.txt"
        with open(timestamp_file, 'w') as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def process_team_stats(self):
        """Process team statistics"""
        print("Processing team stats...")
        df = self.fetch_team_stats()
        if not df.empty:
            self.create_team_charts(df)
            self.save_data(df)
            print("✓ Team stats processed successfully")
        else:
            print("✗ Failed to process team stats")

if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    os.makedirs("archive", exist_ok=True)
    
    processor = NFLTeamStats()
    processor.process_team_stats()