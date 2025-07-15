#!/usr/bin/env python3
"""
Basic NFL Team Statistics Processor
Focuses on core team stats that every NFL fan expects to see:
- Team standings by division
- Basic offensive/defensive stats
- Simple win/loss trends
- Points scored vs allowed
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

class BasicNFLTeamStats:
    def __init__(self):
        self.base_url = "https://www.pro-football-reference.com"
        self.current_season = self.get_current_nfl_season()
        self.docs_dir = Path(__file__).parent.parent.parent / "docs"
        self.archive_dir = Path(__file__).parent.parent.parent / "archive"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # NFL divisions for organization
        self.divisions = {
            'AFC East': ['BUF', 'MIA', 'NWE', 'NYJ'],
            'AFC North': ['BAL', 'CIN', 'CLE', 'PIT'],
            'AFC South': ['HOU', 'IND', 'JAX', 'TEN'],
            'AFC West': ['DEN', 'KAN', 'LVR', 'LAC'],
            'NFC East': ['DAL', 'NYG', 'PHI', 'WAS'],
            'NFC North': ['CHI', 'DET', 'GNB', 'MIN'],
            'NFC South': ['ATL', 'CAR', 'NOR', 'TAM'],
            'NFC West': ['ARI', 'LAR', 'SFO', 'SEA']
        }
        
        print(f"🏈 Basic NFL Team Stats Processor - {self.current_season} Season")
        
    def get_current_nfl_season(self):
        """Get current/most recent NFL season"""
        now = datetime.now()
        return now.year - 1 if now.month <= 7 else now.year
    
    def fetch_team_standings(self):
        """Fetch basic team standings - wins, losses, points"""
        try:
            url = f"{self.base_url}/years/{self.current_season}/"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            tables = pd.read_html(response.content)
            
            # Look for the main standings table
            for table in tables:
                if 'W' in table.columns and 'L' in table.columns and 'Tm' in table.columns:
                    # Clean up multi-level columns
                    if table.columns.nlevels > 1:
                        table.columns = table.columns.droplevel(0)
                    
                    # Remove header rows and NaN teams
                    clean_table = table[table['Tm'].notna()]
                    clean_table = clean_table[clean_table['Tm'] != 'Tm']
                    
                    if len(clean_table) >= 20:  # Should have most/all NFL teams
                        print(f"✓ Found standings table with {len(clean_table)} teams")
                        return clean_table
            
            print("❌ No suitable standings table found")
            return pd.DataFrame()
            
        except Exception as e:
            print(f"❌ Error fetching standings: {e}")
            return pd.DataFrame()
    
    def add_division_info(self, df):
        """Add division and conference information"""
        if 'Tm' not in df.columns:
            return df
            
        df = df.copy()
        
        # Create division map
        team_to_division = {}
        for division, teams in self.divisions.items():
            for team in teams:
                team_to_division[team] = division
        
        # Add division and conference
        df['Division'] = df['Tm'].map(team_to_division).fillna('Unknown')
        df['Conference'] = df['Division'].apply(
            lambda x: 'AFC' if x.startswith('AFC') else 'NFC' if x.startswith('NFC') else 'Unknown'
        )
        
        return df
    
    def create_basic_team_charts(self, standings_df):
        """Create fundamental team charts that every NFL fan expects"""
        if standings_df.empty:
            print("❌ No data available for charts")
            return
            
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 4, hspace=0.4, wspace=0.3)
        
        # Add division info
        standings_df = self.add_division_info(standings_df)
        
        # Convert numeric columns
        for col in ['W', 'L', 'PF', 'PA']:
            if col in standings_df.columns:
                standings_df[col] = pd.to_numeric(standings_df[col], errors='coerce')
        
        # Calculate basic metrics
        if 'W' in standings_df.columns and 'L' in standings_df.columns:
            standings_df['Games'] = standings_df['W'] + standings_df['L']
            standings_df['Win_Pct'] = standings_df['W'] / standings_df['Games']
        
        if 'PF' in standings_df.columns and 'PA' in standings_df.columns:
            standings_df['Point_Diff'] = standings_df['PF'] - standings_df['PA']
        
        # 1. AFC Standings by Division
        ax1 = fig.add_subplot(gs[0, :2])
        afc_teams = standings_df[standings_df['Conference'] == 'AFC'].copy()
        if not afc_teams.empty:
            afc_teams = afc_teams.sort_values(['Division', 'Win_Pct'], ascending=[True, False])
            
            colors = ['#FF6B35', '#FF8C69', '#FFA500', '#FFB347']  # Different orange shades for AFC divisions
            div_colors = []
            current_div = None
            color_idx = 0
            
            for _, row in afc_teams.iterrows():
                if row['Division'] != current_div:
                    current_div = row['Division']
                    color_idx = (color_idx + 1) % len(colors)
                div_colors.append(colors[color_idx])
            
            bars = ax1.barh(range(len(afc_teams)), afc_teams['Win_Pct'], color=div_colors, alpha=0.8)
            ax1.set_yticks(range(len(afc_teams)))
            ax1.set_yticklabels([f"{row['Tm']} ({row['W']}-{row['L']})" for _, row in afc_teams.iterrows()])
            ax1.set_title('🏈 AFC Standings by Division', fontsize=14, color='white')
            ax1.set_xlabel('Win Percentage')
            ax1.grid(True, alpha=0.3, axis='x')
        
        # 2. NFC Standings by Division  
        ax2 = fig.add_subplot(gs[0, 2:])
        nfc_teams = standings_df[standings_df['Conference'] == 'NFC'].copy()
        if not nfc_teams.empty:
            nfc_teams = nfc_teams.sort_values(['Division', 'Win_Pct'], ascending=[True, False])
            
            colors = ['#004E89', '#0066CC', '#4682B4', '#6495ED']  # Different blue shades for NFC divisions
            div_colors = []
            current_div = None
            color_idx = 0
            
            for _, row in nfc_teams.iterrows():
                if row['Division'] != current_div:
                    current_div = row['Division']
                    color_idx = (color_idx + 1) % len(colors)
                div_colors.append(colors[color_idx])
            
            bars = ax2.barh(range(len(nfc_teams)), nfc_teams['Win_Pct'], color=div_colors, alpha=0.8)
            ax2.set_yticks(range(len(nfc_teams)))
            ax2.set_yticklabels([f"{row['Tm']} ({row['W']}-{row['L']})" for _, row in nfc_teams.iterrows()])
            ax2.set_title('🏈 NFC Standings by Division', fontsize=14, color='white')
            ax2.set_xlabel('Win Percentage')
            ax2.grid(True, alpha=0.3, axis='x')
        
        # 3. Top Scoring Offenses
        ax3 = fig.add_subplot(gs[1, 0])
        if 'PF' in standings_df.columns:
            top_offense = standings_df.nlargest(10, 'PF')
            colors = ['#2ECC71' if team in ['BUF', 'MIA', 'NWE', 'NYJ', 'BAL', 'CIN', 'CLE', 'PIT', 
                                           'HOU', 'IND', 'JAX', 'TEN', 'DEN', 'KAN', 'LVR', 'LAC'] 
                     else '#3498DB' for team in top_offense['Tm']]
            
            bars = ax3.bar(range(len(top_offense)), top_offense['PF'], color=colors, alpha=0.8)
            ax3.set_title('🎯 Top Scoring Offenses', fontsize=12, color='white')
            ax3.set_ylabel('Points For')
            ax3.set_xticks(range(len(top_offense)))
            ax3.set_xticklabels(top_offense['Tm'], rotation=45, ha='right')
            ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Best Defenses (Fewest Points Allowed)
        ax4 = fig.add_subplot(gs[1, 1])
        if 'PA' in standings_df.columns:
            best_defense = standings_df.nsmallest(10, 'PA')
            colors = ['#E74C3C' if team in ['BUF', 'MIA', 'NWE', 'NYJ', 'BAL', 'CIN', 'CLE', 'PIT', 
                                           'HOU', 'IND', 'JAX', 'TEN', 'DEN', 'KAN', 'LVR', 'LAC'] 
                     else '#9B59B6' for team in best_defense['Tm']]
            
            bars = ax4.bar(range(len(best_defense)), best_defense['PA'], color=colors, alpha=0.8)
            ax4.set_title('🛡️ Best Defenses (Fewest PA)', fontsize=12, color='white')
            ax4.set_ylabel('Points Against')
            ax4.set_xticks(range(len(best_defense)))
            ax4.set_xticklabels(best_defense['Tm'], rotation=45, ha='right')
            ax4.grid(True, alpha=0.3, axis='y')
        
        # 5. Point Differential Leaders
        ax5 = fig.add_subplot(gs[1, 2])
        if 'Point_Diff' in standings_df.columns:
            top_diff = standings_df.nlargest(10, 'Point_Diff')
            colors = ['#2ECC71' if x > 0 else '#E74C3C' for x in top_diff['Point_Diff']]
            
            bars = ax5.bar(range(len(top_diff)), top_diff['Point_Diff'], color=colors, alpha=0.8)
            ax5.set_title('⚖️ Point Differential Leaders', fontsize=12, color='white')
            ax5.set_ylabel('Point Differential')
            ax5.set_xticks(range(len(top_diff)))
            ax5.set_xticklabels(top_diff['Tm'], rotation=45, ha='right')
            ax5.axhline(y=0, color='white', linestyle='-', alpha=0.5)
            ax5.grid(True, alpha=0.3, axis='y')
        
        # 6. Win Percentage by Conference
        ax6 = fig.add_subplot(gs[1, 3])
        if 'Conference' in standings_df.columns and 'Win_Pct' in standings_df.columns:
            conf_wins = standings_df.groupby('Conference')['Win_Pct'].mean()
            colors = ['#FF6B35', '#004E89']  # AFC Orange, NFC Blue
            
            bars = ax6.bar(range(len(conf_wins)), conf_wins.values, color=colors, alpha=0.8)
            ax6.set_title('🏆 Average Win % by Conference', fontsize=12, color='white')
            ax6.set_ylabel('Average Win %')
            ax6.set_xticks(range(len(conf_wins)))
            ax6.set_xticklabels(conf_wins.index)
            ax6.grid(True, alpha=0.3, axis='y')
            
            # Add values on bars
            for i, v in enumerate(conf_wins.values):
                ax6.text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # 7. Division Winners (Current Leaders)
        ax7 = fig.add_subplot(gs[2, :2])
        division_leaders = standings_df.loc[standings_df.groupby('Division')['Win_Pct'].idxmax()]
        division_leaders = division_leaders.sort_values('Win_Pct', ascending=True)
        
        colors = ['#FF6B35' if conf == 'AFC' else '#004E89' for conf in division_leaders['Conference']]
        
        bars = ax7.barh(range(len(division_leaders)), division_leaders['Win_Pct'], color=colors, alpha=0.8)
        ax7.set_yticks(range(len(division_leaders)))
        ax7.set_yticklabels([f"{row['Tm']} - {row['Division'].split()[-1]}" for _, row in division_leaders.iterrows()])
        ax7.set_title('👑 Current Division Leaders', fontsize=14, color='white')
        ax7.set_xlabel('Win Percentage')
        ax7.grid(True, alpha=0.3, axis='x')
        
        # 8. Offensive vs Defensive Balance
        ax8 = fig.add_subplot(gs[2, 2:])
        if 'PF' in standings_df.columns and 'PA' in standings_df.columns:
            # Scatter plot of offense vs defense
            colors = ['#FF6B35' if conf == 'AFC' else '#004E89' for conf in standings_df['Conference']]
            
            scatter = ax8.scatter(standings_df['PF'], standings_df['PA'], 
                                c=colors, alpha=0.7, s=100, edgecolors='white', linewidth=1)
            
            # Add diagonal line
            max_points = max(standings_df['PF'].max(), standings_df['PA'].max())
            min_points = min(standings_df['PF'].min(), standings_df['PA'].min())
            ax8.plot([min_points, max_points], [min_points, max_points], 
                    'r--', alpha=0.5, linewidth=2, label='Break Even')
            
            ax8.set_xlabel('Points For (Offense)')
            ax8.set_ylabel('Points Against (Defense)')
            ax8.set_title('📊 Offensive vs Defensive Balance', fontsize=14, color='white')
            ax8.legend()
            ax8.grid(True, alpha=0.3)
            
            # Add some team labels for interesting teams
            for _, row in standings_df.iterrows():
                if row['Point_Diff'] > 100 or row['Point_Diff'] < -100:  # Extreme teams
                    ax8.annotate(row['Tm'], (row['PF'], row['PA']), 
                               xytext=(5, 5), textcoords='offset points', 
                               fontsize=8, alpha=0.8)
        
        plt.suptitle(f'🏈 NFL Team Stats Overview - {self.current_season} Season', 
                    fontsize=18, color='white', y=0.98)
        
        # Save chart
        chart_path = self.docs_dir / "team_stats.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()
        
        print(f"✅ Basic team stats charts saved to {chart_path}")
    
    def save_team_data(self, standings_df):
        """Save team standings data"""
        if standings_df.empty:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save current standings
        standings_file = self.docs_dir / "team_standings.csv"
        standings_df.to_csv(standings_file, index=False)
        
        # Archive
        archive_file = self.archive_dir / f"team_standings_{timestamp}.csv"
        standings_df.to_csv(archive_file, index=False)
        
        # Update timestamp
        timestamp_file = self.docs_dir / "last_updated_team_standings.txt"
        with open(timestamp_file, 'w') as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        print(f"✅ Team data saved")
    
    def process_basic_team_stats(self):
        """Main processing function for basic team stats"""
        print("🏈 BASIC NFL TEAM STATS PROCESSOR")
        print("=" * 50)
        print("Generating core team statistics that every NFL fan expects:")
        print("• Team standings by division")
        print("• Top scoring offenses")
        print("• Best defenses")
        print("• Point differential")
        print("• Division leaders")
        
        # Fetch standings
        print("\n1. Fetching team standings...")
        standings_df = self.fetch_team_standings()
        
        if standings_df.empty:
            print("❌ No standings data found")
            return
        
        print(f"✅ Found data for {len(standings_df)} teams")
        print(f"   Columns: {list(standings_df.columns)[:10]}")
        
        # Create charts
        print("\n2. Creating basic team charts...")
        self.create_basic_team_charts(standings_df)
        
        # Save data
        print("\n3. Saving team data...")
        self.save_team_data(standings_df)
        
        print("\n" + "=" * 50)
        print("🏆 BASIC TEAM STATS PROCESSING COMPLETE!")
        print("Charts created: team_stats.png")
        print("Data saved: team_standings.csv")
        print("=" * 50)

if __name__ == "__main__":
    # Ensure directories exist
    processor = BasicNFLTeamStats()
    
    processor.docs_dir.mkdir(parents=True, exist_ok=True)
    processor.archive_dir.mkdir(parents=True, exist_ok=True)
    
    processor.process_basic_team_stats()