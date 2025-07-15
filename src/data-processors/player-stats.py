import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from pathlib import Path

class NFLPlayerStats:
    def __init__(self):
        self.base_url = "https://www.pro-football-reference.com"
        self.current_season = self.get_current_nfl_season()
        self.docs_dir = Path(__file__).parent.parent.parent / "docs"
        self.archive_dir = Path(__file__).parent.parent.parent / "archive"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print(f"Initialized NFL Player Stats processor for {self.current_season}-{self.current_season + 1} season")
        
    def get_current_nfl_season(self):
        """Determine the current/most recent NFL season"""
        now = datetime.now()
        
        # NFL season typically runs September to February
        # If we're in January-July, use previous year
        # If we're in August-December, use current year
        if now.month <= 7:
            return now.year - 1
        else:
            return now.year
        
    def fetch_player_stats(self, stat_type='passing'):
        """Fetch player statistics from Pro Football Reference"""
        try:
            url = f"{self.base_url}/years/{self.current_season}/{stat_type}.htm"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Parse the HTML and extract table data
            tables = pd.read_html(response.content)
            if tables:
                df = tables[0]
                # Clean up column names
                if df.columns.nlevels > 1:
                    df.columns = df.columns.droplevel(0)
                
                # Clean up common issues
                df = df[df['Player'].notna()]  # Remove rows with NaN players
                df = df[df['Player'] != 'Player']  # Remove header rows
                
                return df
            return pd.DataFrame()
        except Exception as e:
            print(f"Error fetching {stat_type} stats: {e}")
            return pd.DataFrame()
    
    def create_player_charts(self, df, stat_type):
        """Create visualization charts for player stats"""
        if df.empty:
            return
            
        plt.style.use('dark_background')
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'NFL {stat_type.title()} Statistics - {self.current_season}', fontsize=16, color='white')
        
        try:
            if stat_type == 'passing':
                # Top 10 passing yards
                if 'Yds' in df.columns:
                    df['Yds'] = pd.to_numeric(df['Yds'], errors='coerce')
                    top_players = df.nlargest(10, 'Yds')
                    axes[0, 0].bar(range(len(top_players)), top_players['Yds'], color='#1f77b4')
                    axes[0, 0].set_title('Top 10 Passing Yards')
                    axes[0, 0].set_xticks(range(len(top_players)))
                    axes[0, 0].set_xticklabels(top_players['Player'], rotation=45, ha='right')
                
                # Top 10 passing TDs
                if 'TD' in df.columns:
                    df['TD'] = pd.to_numeric(df['TD'], errors='coerce')
                    top_tds = df.nlargest(10, 'TD')
                    axes[0, 1].bar(range(len(top_tds)), top_tds['TD'], color='#ff7f0e')
                    axes[0, 1].set_title('Top 10 Passing TDs')
                    axes[0, 1].set_xticks(range(len(top_tds)))
                    axes[0, 1].set_xticklabels(top_tds['Player'], rotation=45, ha='right')
                
                # Completion percentage
                if 'Cmp%' in df.columns:
                    df['Cmp%'] = pd.to_numeric(df['Cmp%'], errors='coerce')
                    top_comp = df.nlargest(10, 'Cmp%')
                    axes[1, 0].bar(range(len(top_comp)), top_comp['Cmp%'], color='#2ca02c')
                    axes[1, 0].set_title('Top 10 Completion %')
                    axes[1, 0].set_xticks(range(len(top_comp)))
                    axes[1, 0].set_xticklabels(top_comp['Player'], rotation=45, ha='right')
                
                # QB Rating
                if 'Rate' in df.columns:
                    df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce')
                    top_rate = df.nlargest(10, 'Rate')
                    axes[1, 1].bar(range(len(top_rate)), top_rate['Rate'], color='#d62728')
                    axes[1, 1].set_title('Top 10 QB Rating')
                    axes[1, 1].set_xticks(range(len(top_rate)))
                    axes[1, 1].set_xticklabels(top_rate['Player'], rotation=45, ha='right')
                    
            elif stat_type == 'rushing':
                # Top 10 rushing yards
                if 'Yds' in df.columns:
                    df['Yds'] = pd.to_numeric(df['Yds'], errors='coerce')
                    top_players = df.nlargest(10, 'Yds')
                    axes[0, 0].bar(range(len(top_players)), top_players['Yds'], color='#ff7f0e')
                    axes[0, 0].set_title('Top 10 Rushing Yards')
                    axes[0, 0].set_xticks(range(len(top_players)))
                    axes[0, 0].set_xticklabels(top_players['Player'], rotation=45, ha='right')
                
                # Top 10 rushing TDs
                if 'TD' in df.columns:
                    df['TD'] = pd.to_numeric(df['TD'], errors='coerce')
                    top_tds = df.nlargest(10, 'TD')
                    axes[0, 1].bar(range(len(top_tds)), top_tds['TD'], color='#2ca02c')
                    axes[0, 1].set_title('Top 10 Rushing TDs')
                    axes[0, 1].set_xticks(range(len(top_tds)))
                    axes[0, 1].set_xticklabels(top_tds['Player'], rotation=45, ha='right')
                
                # Yards per attempt
                if 'Y/A' in df.columns:
                    df['Y/A'] = pd.to_numeric(df['Y/A'], errors='coerce')
                    top_ypa = df.nlargest(10, 'Y/A')
                    axes[1, 0].bar(range(len(top_ypa)), top_ypa['Y/A'], color='#9467bd')
                    axes[1, 0].set_title('Top 10 Yards per Attempt')
                    axes[1, 0].set_xticks(range(len(top_ypa)))
                    axes[1, 0].set_xticklabels(top_ypa['Player'], rotation=45, ha='right')
                
                # Attempts
                if 'Att' in df.columns:
                    df['Att'] = pd.to_numeric(df['Att'], errors='coerce')
                    top_att = df.nlargest(10, 'Att')
                    axes[1, 1].bar(range(len(top_att)), top_att['Att'], color='#8c564b')
                    axes[1, 1].set_title('Top 10 Attempts')
                    axes[1, 1].set_xticks(range(len(top_att)))
                    axes[1, 1].set_xticklabels(top_att['Player'], rotation=45, ha='right')
                    
            elif stat_type == 'receiving':
                # Top 10 receiving yards
                if 'Yds' in df.columns:
                    df['Yds'] = pd.to_numeric(df['Yds'], errors='coerce')
                    top_players = df.nlargest(10, 'Yds')
                    axes[0, 0].bar(range(len(top_players)), top_players['Yds'], color='#1f77b4')
                    axes[0, 0].set_title('Top 10 Receiving Yards')
                    axes[0, 0].set_xticks(range(len(top_players)))
                    axes[0, 0].set_xticklabels(top_players['Player'], rotation=45, ha='right')
                
                # Top 10 receptions
                if 'Rec' in df.columns:
                    df['Rec'] = pd.to_numeric(df['Rec'], errors='coerce')
                    top_rec = df.nlargest(10, 'Rec')
                    axes[0, 1].bar(range(len(top_rec)), top_rec['Rec'], color='#ff7f0e')
                    axes[0, 1].set_title('Top 10 Receptions')
                    axes[0, 1].set_xticks(range(len(top_rec)))
                    axes[0, 1].set_xticklabels(top_rec['Player'], rotation=45, ha='right')
                
                # Top 10 receiving TDs
                if 'TD' in df.columns:
                    df['TD'] = pd.to_numeric(df['TD'], errors='coerce')
                    top_tds = df.nlargest(10, 'TD')
                    axes[1, 0].bar(range(len(top_tds)), top_tds['TD'], color='#2ca02c')
                    axes[1, 0].set_title('Top 10 Receiving TDs')
                    axes[1, 0].set_xticks(range(len(top_tds)))
                    axes[1, 0].set_xticklabels(top_tds['Player'], rotation=45, ha='right')
                
                # Yards per reception
                if 'Y/R' in df.columns:
                    df['Y/R'] = pd.to_numeric(df['Y/R'], errors='coerce')
                    top_ypr = df.nlargest(10, 'Y/R')
                    axes[1, 1].bar(range(len(top_ypr)), top_ypr['Y/R'], color='#d62728')
                    axes[1, 1].set_title('Top 10 Yards per Reception')
                    axes[1, 1].set_xticks(range(len(top_ypr)))
                    axes[1, 1].set_xticklabels(top_ypr['Player'], rotation=45, ha='right')
                    
            elif stat_type == 'defense':
                # Top 10 tackles
                if 'Tkl' in df.columns:
                    df['Tkl'] = pd.to_numeric(df['Tkl'], errors='coerce')
                    top_tkl = df.nlargest(10, 'Tkl')
                    axes[0, 0].bar(range(len(top_tkl)), top_tkl['Tkl'], color='#1f77b4')
                    axes[0, 0].set_title('Top 10 Tackles')
                    axes[0, 0].set_xticks(range(len(top_tkl)))
                    axes[0, 0].set_xticklabels(top_tkl['Player'], rotation=45, ha='right')
                
                # Top 10 sacks
                if 'Sk' in df.columns:
                    df['Sk'] = pd.to_numeric(df['Sk'], errors='coerce')
                    top_sacks = df.nlargest(10, 'Sk')
                    axes[0, 1].bar(range(len(top_sacks)), top_sacks['Sk'], color='#ff7f0e')
                    axes[0, 1].set_title('Top 10 Sacks')
                    axes[0, 1].set_xticks(range(len(top_sacks)))
                    axes[0, 1].set_xticklabels(top_sacks['Player'], rotation=45, ha='right')
                
                # Top 10 interceptions
                if 'Int' in df.columns:
                    df['Int'] = pd.to_numeric(df['Int'], errors='coerce')
                    top_int = df.nlargest(10, 'Int')
                    axes[1, 0].bar(range(len(top_int)), top_int['Int'], color='#2ca02c')
                    axes[1, 0].set_title('Top 10 Interceptions')
                    axes[1, 0].set_xticks(range(len(top_int)))
                    axes[1, 0].set_xticklabels(top_int['Player'], rotation=45, ha='right')
                
                # Top 10 pass deflections
                if 'PD' in df.columns:
                    df['PD'] = pd.to_numeric(df['PD'], errors='coerce')
                    top_pd = df.nlargest(10, 'PD')
                    axes[1, 1].bar(range(len(top_pd)), top_pd['PD'], color='#d62728')
                    axes[1, 1].set_title('Top 10 Pass Deflections')
                    axes[1, 1].set_xticks(range(len(top_pd)))
                    axes[1, 1].set_xticklabels(top_pd['Player'], rotation=45, ha='right')
                    
        except Exception as e:
            print(f"Error creating charts for {stat_type}: {e}")
            
        # Save the chart
        plt.tight_layout()
        chart_path = self.docs_dir / f"{stat_type}_stats.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()
        
    def save_data(self, df, stat_type):
        """Save data to CSV files"""
        if df.empty:
            return
            
        # Save current data
        current_file = self.docs_dir / f"{stat_type}_stats.csv"
        df.to_csv(current_file, index=False)
        
        # Save to archive with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = self.archive_dir / f"{stat_type}_stats_{timestamp}.csv"
        df.to_csv(archive_file, index=False)
        
        # Update timestamp file
        timestamp_file = self.docs_dir / f"last_updated_{stat_type}.txt"
        with open(timestamp_file, 'w') as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def process_all_stats(self):
        """Process all player stat types"""
        stat_types = ['passing', 'rushing', 'receiving', 'defense']
        
        for stat_type in stat_types:
            print(f"Processing {stat_type} stats...")
            df = self.fetch_player_stats(stat_type)
            if not df.empty:
                self.create_player_charts(df, stat_type)
                self.save_data(df, stat_type)
                print(f"✓ {stat_type.title()} stats processed successfully")
            else:
                print(f"✗ Failed to process {stat_type} stats")

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs("docs", exist_ok=True)
    os.makedirs("archive", exist_ok=True)
    
    processor = NFLPlayerStats()
    processor.process_all_stats()