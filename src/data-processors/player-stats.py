#!/usr/bin/env python3
"""
NFL Player Statistics Processor - CORRECTED VERSION
Fetches and processes individual player statistics including:
- Passing stats: yards, TDs, completion %, QB rating
- Rushing stats: yards, TDs, attempts, YPC
- Receiving stats: catches, yards, TDs, YPR
- Defensive stats: tackles, sacks, interceptions
"""

import requests
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

class NFLPlayerStats:
    def __init__(self):
        self.base_url = "https://www.pro-football-reference.com"
        self.current_season = self.get_current_nfl_season()
        self.docs_dir = Path(__file__).parent.parent.parent / "docs"
        self.archive_dir = Path(__file__).parent.parent.parent / "archive"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print(f"🏈 NFL Player Stats Processor - {self.current_season} Season")
        
    def get_current_nfl_season(self):
        """Determine the current/most recent NFL season"""
        now = datetime.now()
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
            print(f"❌ Error fetching {stat_type} stats: {e}")
            return pd.DataFrame()
    
    def create_player_charts(self, df, stat_type):
        """Create visualization charts for player stats"""
        if df.empty:
            print(f"❌ No data available for {stat_type} charts")
            return
            
        plt.style.use('dark_background')
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'🏈 NFL {stat_type.title()} Leaders - {self.current_season}', fontsize=16, color='white')
        
        try:
            if stat_type == 'passing':
                # Top 10 passing yards
                if 'Yds' in df.columns:
                    df['Yds'] = pd.to_numeric(df['Yds'], errors='coerce')
                    top_players = df.nlargest(10, 'Yds')
                    
                    bars = axes[0,0].bar(range(len(top_players)), top_players['Yds'], color='gold', alpha=0.8)
                    axes[0,0].set_title('Top 10 Passing Yards', fontsize=12)
                    axes[0,0].set_ylabel('Yards')
                    axes[0,0].set_xticks(range(len(top_players)))
                    axes[0,0].set_xticklabels([name[:8] for name in top_players['Player']], rotation=45, ha='right')
                    axes[0,0].grid(True, alpha=0.3, axis='y')
                    
                    # Add value labels on bars
                    for bar in bars:
                        height = bar.get_height()
                        axes[0,0].text(bar.get_x() + bar.get_width()/2., height + 50,
                                     f'{int(height)}', ha='center', va='bottom', fontsize=8)
                
                # Top 10 passing TDs
                if 'TD' in df.columns:
                    df['TD'] = pd.to_numeric(df['TD'], errors='coerce')
                    top_td = df.nlargest(10, 'TD')
                    
                    bars = axes[0,1].bar(range(len(top_td)), top_td['TD'], color='orange', alpha=0.8)
                    axes[0,1].set_title('Top 10 Passing TDs', fontsize=12)
                    axes[0,1].set_ylabel('Touchdowns')
                    axes[0,1].set_xticks(range(len(top_td)))
                    axes[0,1].set_xticklabels([name[:8] for name in top_td['Player']], rotation=45, ha='right')
                    axes[0,1].grid(True, alpha=0.3, axis='y')
                
                # Completion percentage
                if 'Cmp%' in df.columns:
                    df['Cmp%'] = pd.to_numeric(df['Cmp%'], errors='coerce')
                    top_cmp = df.nlargest(10, 'Cmp%')
                    
                    bars = axes[1,0].bar(range(len(top_cmp)), top_cmp['Cmp%'], color='green', alpha=0.8)
                    axes[1,0].set_title('Top 10 Completion %', fontsize=12)
                    axes[1,0].set_ylabel('Completion %')
                    axes[1,0].set_xticks(range(len(top_cmp)))
                    axes[1,0].set_xticklabels([name[:8] for name in top_cmp['Player']], rotation=45, ha='right')
                    axes[1,0].grid(True, alpha=0.3, axis='y')
                
                # QB Rating
                if 'Rate' in df.columns:
                    df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce')
                    top_rate = df.nlargest(10, 'Rate')
                    
                    bars = axes[1,1].bar(range(len(top_rate)), top_rate['Rate'], color='blue', alpha=0.8)
                    axes[1,1].set_title('Top 10 QB Rating', fontsize=12)
                    axes[1,1].set_ylabel('QB Rating')
                    axes[1,1].set_xticks(range(len(top_rate)))
                    axes[1,1].set_xticklabels([name[:8] for name in top_rate['Player']], rotation=45, ha='right')
                    axes[1,1].grid(True, alpha=0.3, axis='y')
                    
            elif stat_type == 'rushing':
                # Top 10 rushing yards
                if 'Yds' in df.columns:
                    df['Yds'] = pd.to_numeric(df['Yds'], errors='coerce')
                    top_rush = df.nlargest(10, 'Yds')
                    
                    bars = axes[0,0].bar(range(len(top_rush)), top_rush['Yds'], color='red', alpha=0.8)
                    axes[0,0].set_title('Top 10 Rushing Yards', fontsize=12)
                    axes[0,0].set_ylabel('Yards')
                    axes[0,0].set_xticks(range(len(top_rush)))
                    axes[0,0].set_xticklabels([name[:8] for name in top_rush['Player']], rotation=45, ha='right')
                    axes[0,0].grid(True, alpha=0.3, axis='y')
                
                # Top 10 rushing TDs
                if 'TD' in df.columns:
                    df['TD'] = pd.to_numeric(df['TD'], errors='coerce')
                    top_td = df.nlargest(10, 'TD')
                    
                    bars = axes[0,1].bar(range(len(top_td)), top_td['TD'], color='darkred', alpha=0.8)
                    axes[0,1].set_title('Top 10 Rushing TDs', fontsize=12)
                    axes[0,1].set_ylabel('Touchdowns')
                    axes[0,1].set_xticks(range(len(top_td)))
                    axes[0,1].set_xticklabels([name[:8] for name in top_td['Player']], rotation=45, ha='right')
                    axes[0,1].grid(True, alpha=0.3, axis='y')
                
                # Yards per attempt
                if 'Y/A' in df.columns:
                    df['Y/A'] = pd.to_numeric(df['Y/A'], errors='coerce')
                    top_ypa = df.nlargest(10, 'Y/A')
                    
                    bars = axes[1,0].bar(range(len(top_ypa)), top_ypa['Y/A'], color='brown', alpha=0.8)
                    axes[1,0].set_title('Top 10 Yards per Attempt', fontsize=12)
                    axes[1,0].set_ylabel('Y/A')
                    axes[1,0].set_xticks(range(len(top_ypa)))
                    axes[1,0].set_xticklabels([name[:8] for name in top_ypa['Player']], rotation=45, ha='right')
                    axes[1,0].grid(True, alpha=0.3, axis='y')
                
                # Attempts
                if 'Att' in df.columns:
                    df['Att'] = pd.to_numeric(df['Att'], errors='coerce')
                    top_att = df.nlargest(10, 'Att')
                    
                    bars = axes[1,1].bar(range(len(top_att)), top_att['Att'], color='maroon', alpha=0.8)
                    axes[1,1].set_title('Top 10 Rush Attempts', fontsize=12)
                    axes[1,1].set_ylabel('Attempts')
                    axes[1,1].set_xticks(range(len(top_att)))
                    axes[1,1].set_xticklabels([name[:8] for name in top_att['Player']], rotation=45, ha='right')
                    axes[1,1].grid(True, alpha=0.3, axis='y')
                    
            elif stat_type == 'receiving':
                # Top 10 receiving yards
                if 'Yds' in df.columns:
                    df['Yds'] = pd.to_numeric(df['Yds'], errors='coerce')
                    top_rec = df.nlargest(10, 'Yds')
                    
                    bars = axes[0,0].bar(range(len(top_rec)), top_rec['Yds'], color='purple', alpha=0.8)
                    axes[0,0].set_title('Top 10 Receiving Yards', fontsize=12)
                    axes[0,0].set_ylabel('Yards')
                    axes[0,0].set_xticks(range(len(top_rec)))
                    axes[0,0].set_xticklabels([name[:8] for name in top_rec['Player']], rotation=45, ha='right')
                    axes[0,0].grid(True, alpha=0.3, axis='y')
                
                # Top 10 receptions
                if 'Rec' in df.columns:
                    df['Rec'] = pd.to_numeric(df['Rec'], errors='coerce')
                    top_catches = df.nlargest(10, 'Rec')
                    
                    bars = axes[0,1].bar(range(len(top_catches)), top_catches['Rec'], color='cyan', alpha=0.8)
                    axes[0,1].set_title('Top 10 Receptions', fontsize=12)
                    axes[0,1].set_ylabel('Catches')
                    axes[0,1].set_xticks(range(len(top_catches)))
                    axes[0,1].set_xticklabels([name[:8] for name in top_catches['Player']], rotation=45, ha='right')
                    axes[0,1].grid(True, alpha=0.3, axis='y')
                
                # Top 10 receiving TDs
                if 'TD' in df.columns:
                    df['TD'] = pd.to_numeric(df['TD'], errors='coerce')
                    top_td = df.nlargest(10, 'TD')
                    
                    bars = axes[1,0].bar(range(len(top_td)), top_td['TD'], color='magenta', alpha=0.8)
                    axes[1,0].set_title('Top 10 Receiving TDs', fontsize=12)
                    axes[1,0].set_ylabel('Touchdowns')
                    axes[1,0].set_xticks(range(len(top_td)))
                    axes[1,0].set_xticklabels([name[:8] for name in top_td['Player']], rotation=45, ha='right')
                    axes[1,0].grid(True, alpha=0.3, axis='y')
                
                # Yards per reception
                if 'Y/R' in df.columns:
                    df['Y/R'] = pd.to_numeric(df['Y/R'], errors='coerce')
                    top_ypr = df.nlargest(10, 'Y/R')
                    
                    bars = axes[1,1].bar(range(len(top_ypr)), top_ypr['Y/R'], color='lime', alpha=0.8)
                    axes[1,1].set_title('Top 10 Yards per Reception', fontsize=12)
                    axes[1,1].set_ylabel('Y/R')
                    axes[1,1].set_xticks(range(len(top_ypr)))
                    axes[1,1].set_xticklabels([name[:8] for name in top_ypr['Player']], rotation=45, ha='right')
                    axes[1,1].grid(True, alpha=0.3, axis='y')
                    
            elif stat_type == 'defense':
                # Top 10 tackles
                if 'Tkl' in df.columns:
                    df['Tkl'] = pd.to_numeric(df['Tkl'], errors='coerce')
                    top_tkl = df.nlargest(10, 'Tkl')
                    
                    bars = axes[0,0].bar(range(len(top_tkl)), top_tkl['Tkl'], color='darkblue', alpha=0.8)
                    axes[0,0].set_title('Top 10 Tackles', fontsize=12)
                    axes[0,0].set_ylabel('Tackles')
                    axes[0,0].set_xticks(range(len(top_tkl)))
                    axes[0,0].set_xticklabels([name[:8] for name in top_tkl['Player']], rotation=45, ha='right')
                    axes[0,0].grid(True, alpha=0.3, axis='y')
                
                # Top 10 sacks
                if 'Sk' in df.columns:
                    df['Sk'] = pd.to_numeric(df['Sk'], errors='coerce')
                    top_sacks = df.nlargest(10, 'Sk')
                    
                    bars = axes[0,1].bar(range(len(top_sacks)), top_sacks['Sk'], color='darkgreen', alpha=0.8)
                    axes[0,1].set_title('Top 10 Sacks', fontsize=12)
                    axes[0,1].set_ylabel('Sacks')
                    axes[0,1].set_xticks(range(len(top_sacks)))
                    axes[0,1].set_xticklabels([name[:8] for name in top_sacks['Player']], rotation=45, ha='right')
                    axes[0,1].grid(True, alpha=0.3, axis='y')
                
                # Top 10 interceptions
                if 'Int' in df.columns:
                    df['Int'] = pd.to_numeric(df['Int'], errors='coerce')
                    top_int = df.nlargest(10, 'Int')
                    
                    bars = axes[1,0].bar(range(len(top_int)), top_int['Int'], color='navy', alpha=0.8)
                    axes[1,0].set_title('Top 10 Interceptions', fontsize=12)
                    axes[1,0].set_ylabel('Interceptions')
                    axes[1,0].set_xticks(range(len(top_int)))
                    axes[1,0].set_xticklabels([name[:8] for name in top_int['Player']], rotation=45, ha='right')
                    axes[1,0].grid(True, alpha=0.3, axis='y')
                
                # Top 10 pass deflections
                if 'PD' in df.columns:
                    df['PD'] = pd.to_numeric(df['PD'], errors='coerce')
                    top_pd = df.nlargest(10, 'PD')
                    
                    bars = axes[1,1].bar(range(len(top_pd)), top_pd['PD'], color='teal', alpha=0.8)
                    axes[1,1].set_title('Top 10 Pass Deflections', fontsize=12)
                    axes[1,1].set_ylabel('Pass Deflections')
                    axes[1,1].set_xticks(range(len(top_pd)))
                    axes[1,1].set_xticklabels([name[:8] for name in top_pd['Player']], rotation=45, ha='right')
                    axes[1,1].grid(True, alpha=0.3, axis='y')
                    
        except Exception as e:
            print(f"❌ Error creating charts for {stat_type}: {e}")
            # Create a simple fallback chart
            axes[0,0].text(0.5, 0.5, f"Error creating {stat_type} charts\nData columns: {list(df.columns)[:5]}", 
                          ha='center', va='center', transform=axes[0,0].transAxes, color='white')
            
        # Save the chart
        plt.tight_layout()
        chart_path = self.docs_dir / f"{stat_type}_stats.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()
        
        print(f"✅ {stat_type.title()} charts saved to {chart_path}")
        
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
        print("🏈 NFL PLAYER STATISTICS PROCESSOR")
        print("=" * 60)
        print(f"Processing {self.current_season} NFL season data...")
        
        stat_types = ['passing', 'rushing', 'receiving', 'defense']
        
        for stat_type in stat_types:
            print(f"\n📊 Processing {stat_type} stats...")
            try:
                df = self.fetch_player_stats(stat_type)
                if not df.empty:
                    print(f"✅ Found data for {len(df)} players")
                    self.create_player_charts(df, stat_type)
                    self.save_data(df, stat_type)
                else:
                    print(f"❌ No {stat_type} data found")
                    
                time.sleep(1)  # Be respectful to the server
                    
            except Exception as e:
                print(f"❌ Error processing {stat_type} stats: {e}")
                continue
        
        print("\n" + "=" * 60)
        print("🏆 PLAYER STATISTICS PROCESSING COMPLETE!")
        print("=" * 60)

if __name__ == "__main__":
    # Ensure directories exist
    processor = NFLPlayerStats()
    
    processor.docs_dir.mkdir(parents=True, exist_ok=True)
    processor.archive_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Created directories:")
    print(f"  Docs: {processor.docs_dir}")
    print(f"  Archive: {processor.archive_dir}")
    
    processor.process_all_stats()