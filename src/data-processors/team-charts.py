#!/usr/bin/env python3
"""
NFL Team Charts Generator
Creates comprehensive team performance visualizations including:
- AFC vs NFC conference analysis
- Offensive vs Defensive efficiency
- Division strength comparisons
- Advanced team metrics
- Championship contender analysis
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

class NFLTeamCharts:
    def __init__(self):
        self.base_url = "https://www.pro-football-reference.com"
        self.current_season = self.get_current_nfl_season()
        self.docs_dir = Path(__file__).parent.parent.parent / "docs"
        self.archive_dir = Path(__file__).parent.parent.parent / "archive"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # NFL divisions and conferences
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
        
        print(f"🏈 NFL Team Charts Generator - {self.current_season} Season")
        
    def get_current_nfl_season(self):
        """Get current/most recent NFL season"""
        now = datetime.now()
        return now.year - 1 if now.month <= 7 else now.year
    
    def fetch_team_standings(self):
        """Fetch comprehensive team standings data"""
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
                        print(f"✅ Found standings table with {len(clean_table)} teams")
                        return clean_table
            
            print("❌ No suitable standings table found")
            return pd.DataFrame()
            
        except Exception as e:
            print(f"❌ Error fetching standings: {e}")
            return pd.DataFrame()
    
    def add_team_metadata(self, df):
        """Add conference and division information"""
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
    
    def create_advanced_team_charts(self, standings_df):
        """Create comprehensive advanced team analytics"""
        if standings_df.empty:
            print("❌ No standings data available for charts")
            return
            
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(20, 16))
        gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
        
        # Add team metadata
        standings_df = self.add_team_metadata(standings_df)
        
        # Convert numeric columns
        for col in ['W', 'L', 'PF', 'PA']:
            if col in standings_df.columns:
                standings_df[col] = pd.to_numeric(standings_df[col], errors='coerce')
        
        # Calculate derived metrics
        if 'W' in standings_df.columns and 'L' in standings_df.columns:
            standings_df['Games'] = standings_df['W'] + standings_df['L']
            standings_df['Win_Pct'] = standings_df['W'] / standings_df['Games']
        
        if 'PF' in standings_df.columns and 'PA' in standings_df.columns:
            standings_df['Point_Diff'] = standings_df['PF'] - standings_df['PA']
            standings_df['PPG'] = standings_df['PF'] / standings_df['Games']
            standings_df['PAPG'] = standings_df['PA'] / standings_df['Games']
        
        try:
            # 1. AFC vs NFC Win Percentage Comparison
            ax1 = fig.add_subplot(gs[0, 0])
            if 'Conference' in standings_df.columns:
                conf_data = standings_df.groupby('Conference')['Win_Pct'].agg(['mean', 'std']).reset_index()
                
                colors = ['#FF6B35', '#004E89']  # AFC Orange, NFC Blue
                bars = ax1.bar(conf_data['Conference'], conf_data['mean'], 
                              color=colors, alpha=0.8, yerr=conf_data['std'], capsize=5)
                
                ax1.set_title('AFC vs NFC Average Win %', fontsize=12)
                ax1.set_ylabel('Average Win Percentage')
                ax1.grid(True, alpha=0.3, axis='y')
                
                # Add values on bars
                for i, (bar, val) in enumerate(zip(bars, conf_data['mean'])):
                    ax1.text(bar.get_x() + bar.get_width()/2., val + 0.01, 
                           f'{val:.3f}', ha='center', va='bottom', fontweight='bold')
            
            # 2. Offensive vs Defensive Balance Scatter
            ax2 = fig.add_subplot(gs[0, 1])
            if 'PPG' in standings_df.columns and 'PAPG' in standings_df.columns:
                # Color by conference
                colors = ['#FF6B35' if conf == 'AFC' else '#004E89' 
                         for conf in standings_df['Conference']]
                
                scatter = ax2.scatter(standings_df['PPG'], standings_df['PAPG'], 
                                    c=colors, alpha=0.7, s=100, edgecolors='white', linewidth=1)
                
                # Add diagonal line for balance
                max_points = max(standings_df['PPG'].max(), standings_df['PAPG'].max())
                min_points = min(standings_df['PPG'].min(), standings_df['PAPG'].min())
                ax2.plot([min_points, max_points], [min_points, max_points], 
                        'r--', alpha=0.5, linewidth=2, label='Balanced O/D')
                
                ax2.set_xlabel('Points Per Game (Offense)')
                ax2.set_ylabel('Points Allowed Per Game (Defense)')
                ax2.set_title('Offensive vs Defensive Balance', fontsize=12)
                ax2.legend()
                ax2.grid(True, alpha=0.3)
            
            # 3. Division Strength Analysis
            ax3 = fig.add_subplot(gs[0, 2])
            if 'Division' in standings_df.columns:
                div_strength = standings_df.groupby('Division')['Win_Pct'].mean().sort_values(ascending=True)
                
                # Color by conference
                div_colors = ['#FF6B35' if div.startswith('AFC') else '#004E89' 
                             for div in div_strength.index]
                
                bars = ax3.barh(range(len(div_strength)), div_strength.values, 
                               color=div_colors, alpha=0.8)
                
                ax3.set_yticks(range(len(div_strength)))
                ax3.set_yticklabels([div.split()[-1] for div in div_strength.index])
                ax3.set_title('Division Strength (Avg Win %)', fontsize=12)
                ax3.set_xlabel('Average Win %')
                ax3.grid(True, alpha=0.3, axis='x')
            
            # 4. Top Contenders by Point Differential
            ax4 = fig.add_subplot(gs[1, 0])
            if 'Point_Diff' in standings_df.columns:
                top_contenders = standings_df.nlargest(10, 'Point_Diff')
                
                colors = ['#FF6B35' if conf == 'AFC' else '#004E89' 
                         for conf in top_contenders['Conference']]
                
                bars = ax4.bar(range(len(top_contenders)), top_contenders['Point_Diff'], 
                              color=colors, alpha=0.8)
                
                ax4.set_title('Top Championship Contenders', fontsize=12)
                ax4.set_ylabel('Point Differential')
                ax4.set_xticks(range(len(top_contenders)))
                ax4.set_xticklabels(top_contenders['Tm'], rotation=45, ha='right')
                ax4.grid(True, alpha=0.3, axis='y')
            
            # 5. Offensive Powerhouses
            ax5 = fig.add_subplot(gs[1, 1])
            if 'PPG' in standings_df.columns:
                top_offense = standings_df.nlargest(10, 'PPG')
                
                colors = plt.cm.Reds(np.linspace(0.4, 1, len(top_offense)))
                bars = ax5.bar(range(len(top_offense)), top_offense['PPG'], 
                              color=colors, alpha=0.8)
                
                ax5.set_title('Top Offensive Teams', fontsize=12)
                ax5.set_ylabel('Points Per Game')
                ax5.set_xticks(range(len(top_offense)))
                ax5.set_xticklabels(top_offense['Tm'], rotation=45, ha='right')
                ax5.grid(True, alpha=0.3, axis='y')
            
            # 6. Elite Defenses
            ax6 = fig.add_subplot(gs[1, 2])
            if 'PAPG' in standings_df.columns:
                best_defense = standings_df.nsmallest(10, 'PAPG')
                
                colors = plt.cm.Blues(np.linspace(0.4, 1, len(best_defense)))
                bars = ax6.bar(range(len(best_defense)), best_defense['PAPG'], 
                              color=colors, alpha=0.8)
                
                ax6.set_title('Elite Defenses', fontsize=12)
                ax6.set_ylabel('Points Allowed Per Game')
                ax6.set_xticks(range(len(best_defense)))
                ax6.set_xticklabels(best_defense['Tm'], rotation=45, ha='right')
                ax6.grid(True, alpha=0.3, axis='y')
            
            # 7. Conference Championship Race
            ax7 = fig.add_subplot(gs[2, :2])
            if 'Conference' in standings_df.columns and 'Win_Pct' in standings_df.columns:
                # Get top 6 teams from each conference
                afc_teams = standings_df[standings_df['Conference'] == 'AFC'].nlargest(6, 'Win_Pct')
                nfc_teams = standings_df[standings_df['Conference'] == 'NFC'].nlargest(6, 'Win_Pct')
                
                # Create side-by-side comparison
                x_afc = np.arange(len(afc_teams))
                x_nfc = np.arange(len(nfc_teams)) + len(afc_teams) + 1
                
                bars1 = ax7.bar(x_afc, afc_teams['Win_Pct'], color='#FF6B35', alpha=0.8, label='AFC')
                bars2 = ax7.bar(x_nfc, nfc_teams['Win_Pct'], color='#004E89', alpha=0.8, label='NFC')
                
                ax7.set_title('Conference Championship Race (Top 6 Each)', fontsize=14)
                ax7.set_ylabel('Win Percentage')
                ax7.set_xticks(list(x_afc) + list(x_nfc))
                ax7.set_xticklabels(list(afc_teams['Tm']) + list(nfc_teams['Tm']), rotation=45, ha='right')
                ax7.legend()
                ax7.grid(True, alpha=0.3, axis='y')
            
            # 8. Analytics Summary
            ax8 = fig.add_subplot(gs[2, 2])
            ax8.axis('off')
            
            # Calculate some interesting stats
            if not standings_df.empty:
                best_record = standings_df.loc[standings_df['Win_Pct'].idxmax()]
                worst_record = standings_df.loc[standings_df['Win_Pct'].idxmin()]
                highest_scoring = standings_df.loc[standings_df['PPG'].idxmax()]
                best_defense = standings_df.loc[standings_df['PAPG'].idxmin()]
                
                summary_text = f"""
ADVANCED TEAM ANALYTICS SUMMARY

🏆 Best Record: {best_record['Tm']} ({best_record['W']:.0f}-{best_record['L']:.0f})

📊 Highest Scoring: {highest_scoring['Tm']} ({highest_scoring['PPG']:.1f} PPG)

🛡️ Best Defense: {best_defense['Tm']} ({best_defense['PAPG']:.1f} PAPG)

⚖️ Most Balanced: Look for teams near the diagonal line

🏈 Conference Battle: AFC vs NFC strength comparison

📈 Championship Contenders: Top point differential teams

Analysis includes:
• Offensive vs Defensive efficiency
• Division strength rankings  
• Conference comparisons
• Championship probability factors

Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                
                ax8.text(0.05, 0.95, summary_text.strip(), fontsize=10, color='lightblue',
                        transform=ax8.transAxes, verticalalignment='top')
            
            plt.suptitle(f'🏈 NFL Advanced Team Analytics Dashboard - {self.current_season}', 
                        fontsize=18, color='white', y=0.98)
            
            # Save chart
            chart_path = self.docs_dir / "team_advanced_analytics.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='black')
            plt.close()
            
            print(f"✅ Advanced team analytics saved to {chart_path}")
            
        except Exception as e:
            print(f"❌ Error creating advanced charts: {e}")
            plt.close()
    
    def save_team_data(self, standings_df):
        """Save team data to files"""
        if standings_df.empty:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save advanced analytics data
        analytics_file = self.docs_dir / "team_advanced_data.csv"
        standings_df.to_csv(analytics_file, index=False)
        
        # Archive
        archive_file = self.archive_dir / f"team_advanced_data_{timestamp}.csv"
        standings_df.to_csv(archive_file, index=False)
        
        # Update timestamp
        timestamp_file = self.docs_dir / "last_updated_team_charts.txt"
        with open(timestamp_file, 'w') as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        print(f"✅ Advanced team data saved")
    
    def process_team_charts(self):
        """Main processing function for advanced team charts"""
        print("🏈 NFL ADVANCED TEAM ANALYTICS PROCESSOR")
        print("=" * 60)
        print("Generating advanced team performance analytics:")
        print("• AFC vs NFC conference analysis")
        print("• Offensive vs defensive balance")
        print("• Division strength rankings")
        print("• Championship contender analysis")
        print("• Elite offense and defense identification")
        
        # Fetch standings
        print("\n1. Fetching team standings data...")
        standings_df = self.fetch_team_standings()
        
        if standings_df.empty:
            print("❌ No standings data found")
            return
        
        print(f"✅ Retrieved data for {len(standings_df)} teams")
        print(f"   Columns: {list(standings_df.columns)[:10]}")
        
        # Create advanced charts
        print("\n2. Creating advanced team analytics...")
        self.create_advanced_team_charts(standings_df)
        
        # Save data
        print("\n3. Saving advanced team data...")
        self.save_team_data(standings_df)
        
        print("\n" + "=" * 60)
        print("🏆 ADVANCED TEAM ANALYTICS COMPLETE!")
        print("Charts created: team_advanced_analytics.png")
        print("Data saved: team_advanced_data.csv")
        print("=" * 60)

if __name__ == "__main__":
    # Ensure directories exist
    charts = NFLTeamCharts()
    
    charts.docs_dir.mkdir(parents=True, exist_ok=True)
    charts.archive_dir.mkdir(parents=True, exist_ok=True)
    
    charts.process_team_charts()