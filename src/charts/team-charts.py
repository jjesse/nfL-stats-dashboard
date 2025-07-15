#!/usr/bin/env python3
"""
NFL Team Charts Generator
Creates comprehensive team performance visualizations including:
- Team standings and records
- Offensive vs Defensive performance
- Division comparisons
- Conference analytics
- Advanced team metrics
"""

import requests
import pandas as pd
import requests
import pandas as pd
import matplotlib.pyplot as plt

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

import seaborn as sns
import numpy as np
from datetime import datetime
import time
from pathlib import Path
import sys
import warnings

class NFLTeamCharts:
    def __init__(self):
        self.base_url = "https://www.pro-football-reference.com"
        self.current_season = self.get_current_nfl_season()
        self.docs_dir = Path(__file__).parent.parent.parent / "docs"
        self.archive_dir = Path(__file__).parent.parent.parent / "archive"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # NFL team mappings
        self.afc_teams = ['BUF', 'MIA', 'NWE', 'NYJ', 'BAL', 'CIN', 'CLE', 'PIT', 
                         'HOU', 'IND', 'JAX', 'TEN', 'DEN', 'KAN', 'LVR', 'LAC']
        
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
        
        print(f"🏈 Initialized NFL Team Charts Generator for {self.current_season} season")
        
    def get_current_nfl_season(self):
        """Determine the current/most recent NFL season"""
        now = datetime.now()
        if now.month <= 7:
            return now.year - 1
        else:
            return now.year
    
    def fetch_team_standings(self):
        """Fetch comprehensive team standings data"""
        try:
            url = f"{self.base_url}/years/{self.current_season}/"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            tables = pd.read_html(response.content)
            standings_data = []
            
            print(f"📊 Found {len(tables)} tables on main season page")
            
            for i, table in enumerate(tables):
                # Look for tables with team standings info
                if 'W' in table.columns and 'L' in table.columns and 'Tm' in table.columns:
                    if table.columns.nlevels > 1:
                        table.columns = table.columns.droplevel(0)
                    
                    # Clean up the data
                    clean_table = table[table['Tm'].notna()]
                    clean_table = clean_table[clean_table['Tm'] != 'Tm']
                    
                    if not clean_table.empty:
                        print(f"  ✓ Table {i+1}: {len(clean_table)} teams - {list(clean_table.columns)[:8]}")
                        standings_data.append(clean_table)
            
            if standings_data:
                # Use the largest table (most complete data)
                combined_df = max(standings_data, key=len)
                print(f"✓ Using standings table with {len(combined_df)} teams")
                return combined_df
            
            return pd.DataFrame()
            
        except Exception as e:
            print(f"❌ Error fetching standings: {e}")
            return pd.DataFrame()
    
    def fetch_team_offense_defense(self):
        """Fetch detailed offensive and defensive statistics"""
        team_stats = {}
        
        try:
            # Team offensive/defensive stats page
            url = f"{self.base_url}/years/{self.current_season}/opp.htm"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                tables = pd.read_html(response.content)
                print(f"📈 Found {len(tables)} tables on team stats page")
                
                for i, table in enumerate(tables[:3]):  # Look at first 3 tables
                    if table.columns.nlevels > 1:
                        table.columns = table.columns.droplevel(0)
                    
                    # Clean and identify table type
                    if 'Tm' in table.columns and not table.empty:
                        clean_table = table[table['Tm'].notna()]
                        clean_table = clean_table[clean_table['Tm'] != 'Tm']
                        
                        if not clean_table.empty:
                            print(f"  ✓ Stats Table {i+1}: {len(clean_table)} teams - {list(clean_table.columns)[:8]}")
                            if i == 0:
                                team_stats['offense'] = clean_table
                            elif i == 1:
                                team_stats['defense'] = clean_table
                            else:
                                team_stats[f'additional_{i}'] = clean_table
                
            time.sleep(1)  # Be respectful to the server
            
        except Exception as e:
            print(f"❌ Error fetching team offense/defense stats: {e}")
            
        return team_stats
    
    def add_team_metadata(self, df):
        """Add conference and division information to team data"""
        if 'Tm' not in df.columns:
            return df
            
        df = df.copy()
        
        # Add conference
        df['Conference'] = df['Tm'].apply(
            lambda x: 'AFC' if x in self.afc_teams else 'NFC'
        )
        
        # Add division
        division_map = {}
        for div, teams in self.divisions.items():
            for team in teams:
                division_map[team] = div
        
        df['Division'] = df['Tm'].map(division_map).fillna('Unknown')
        
        return df
    
    def create_comprehensive_team_charts(self, standings_df, detailed_stats=None):
        """Create comprehensive team visualization dashboard"""
        if standings_df.empty:
            print("❌ No standings data available for charts")
            return
            
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(24, 18))
        gs = fig.add_gridspec(4, 3, hspace=0.4, wspace=0.3)
        
        # Add team metadata
        standings_df = self.add_team_metadata(standings_df)
        
        try:
            # Convert numeric columns
            numeric_cols = ['W', 'L', 'PF', 'PA']
            for col in numeric_cols:
                if col in standings_df.columns:
                    standings_df[col] = pd.to_numeric(standings_df[col], errors='coerce')
            
            # Calculate derived metrics
            if 'W' in standings_df.columns and 'L' in standings_df.columns:
                standings_df['Win_Pct'] = standings_df['W'] / (standings_df['W'] + standings_df['L'])
                standings_df['Games'] = standings_df['W'] + standings_df['L']
            
            if 'PF' in standings_df.columns and 'PA' in standings_df.columns:
                standings_df['Point_Diff'] = standings_df['PF'] - standings_df['PA']
                standings_df['PPG'] = standings_df['PF'] / standings_df['Games']
                standings_df['PAPG'] = standings_df['PA'] / standings_df['Games']
            
            print(f"Debug: Standings columns after processing: {list(standings_df.columns)}")
            print(f"Debug: Standings shape: {standings_df.shape}")
            
            # 1. AFC vs NFC Standings
            try:
                ax1 = fig.add_subplot(gs[0, 0])
                if 'Conference' in standings_df.columns and 'Win_Pct' in standings_df.columns:
                    afc_teams = standings_df[standings_df['Conference'] == 'AFC'].nlargest(8, 'Win_Pct')
                    nfc_teams = standings_df[standings_df['Conference'] == 'NFC'].nlargest(8, 'Win_Pct')
                    
                    y_pos_afc = np.arange(len(afc_teams))
                    y_pos_nfc = np.arange(len(nfc_teams)) + len(afc_teams) + 1
                    
                    bars1 = ax1.barh(y_pos_afc, afc_teams['Win_Pct'], color='#FF6B35', alpha=0.8, label='AFC')
                    bars2 = ax1.barh(y_pos_nfc, nfc_teams['Win_Pct'], color='#004E89', alpha=0.8, label='NFC')
                    
                    # Add team labels
                    all_teams = list(afc_teams['Tm']) + [''] + list(nfc_teams['Tm'])
                    ax1.set_yticks(list(y_pos_afc) + [len(afc_teams)] + list(y_pos_nfc))
                    ax1.set_yticklabels(all_teams, fontsize=10)
                    
                    ax1.set_title('🏆 Conference Standings (Top 8 Each)', fontsize=14, color='white', pad=20)
                    ax1.set_xlabel('Win Percentage')
                    ax1.legend()
                    ax1.grid(True, alpha=0.3, axis='x')
                    print("✓ Chart 1: Conference standings created")
                else:
                    ax1.text(0.5, 0.5, 'Conference data not available', ha='center', va='center', 
                            transform=ax1.transAxes, fontsize=12, color='white')
                    ax1.set_title('🏆 Conference Standings', fontsize=14, color='white')
            except Exception as e:
                print(f"⚠️ Error creating conference standings chart: {e}")
                ax1.text(0.5, 0.5, f'Chart error: {str(e)[:50]}...', ha='center', va='center', 
                        transform=ax1.transAxes, fontsize=10, color='red')
            
            # 2. Points For vs Points Against Scatter
            try:
                ax2 = fig.add_subplot(gs[0, 1])
                if 'PF' in standings_df.columns and 'PA' in standings_df.columns and 'Win_Pct' in standings_df.columns:
                    scatter = ax2.scatter(standings_df['PF'], standings_df['PA'], 
                                        s=150, c=standings_df['Win_Pct'], 
                                        cmap='RdYlGn', alpha=0.8, edgecolors='white', linewidth=1)
                    
                    # Add diagonal line for equal points
                    max_points = max(standings_df['PF'].max(), standings_df['PA'].max())
                    min_points = min(standings_df['PF'].min(), standings_df['PA'].min())
                    ax2.plot([min_points, max_points], [min_points, max_points], 
                            'r--', alpha=0.6, linewidth=2, label='Break Even')
                    
                    ax2.set_xlabel('Points For (Offense)')
                    ax2.set_ylabel('Points Against (Defense)')
                    ax2.set_title('📊 Offensive vs Defensive Performance', fontsize=14, color='white', pad=20)
                    ax2.legend()
                    ax2.grid(True, alpha=0.3)
                    
                    # Add colorbar
                    cbar = plt.colorbar(scatter, ax=ax2)
                    cbar.set_label('Win %', rotation=270, labelpad=20)
                    print("✓ Chart 2: Points scatter created")
                else:
                    ax2.text(0.5, 0.5, 'Points data not available', ha='center', va='center', 
                            transform=ax2.transAxes, fontsize=12, color='white')
                    ax2.set_title('📊 Offensive vs Defensive Performance', fontsize=14, color='white')
            except Exception as e:
                print(f"⚠️ Error creating points scatter chart: {e}")
                ax2.text(0.5, 0.5, f'Chart error: {str(e)[:50]}...', ha='center', va='center', 
                        transform=ax2.transAxes, fontsize=10, color='red')
            
            # 3. Division Leaders
            try:
                ax3 = fig.add_subplot(gs[0, 2])
                if 'Division' in standings_df.columns and 'Win_Pct' in standings_df.columns:
                    division_leaders = standings_df.loc[standings_df.groupby('Division')['Win_Pct'].idxmax()]
                    division_leaders = division_leaders.sort_values('Win_Pct', ascending=True)
                    
                    colors = ['#FF6B35' if conf == 'AFC' else '#004E89' 
                             for conf in division_leaders['Conference']]
                    
                    bars = ax3.barh(range(len(division_leaders)), division_leaders['Win_Pct'], 
                                   color=colors, alpha=0.8)
                    
                    ax3.set_yticks(range(len(division_leaders)))
                    ax3.set_yticklabels([f"{row['Tm']} ({row['Division'].split()[-1]})" 
                                       for _, row in division_leaders.iterrows()], fontsize=10)
                    ax3.set_title('👑 Division Leaders', fontsize=14, color='white', pad=20)
                    ax3.set_xlabel('Win Percentage')
                    ax3.grid(True, alpha=0.3, axis='x')
                    print("✓ Chart 3: Division leaders created")
                else:
                    ax3.text(0.5, 0.5, 'Division data not available', ha='center', va='center', 
                            transform=ax3.transAxes, fontsize=12, color='white')
                    ax3.set_title('👑 Division Leaders', fontsize=14, color='white')
            except Exception as e:
                print(f"⚠️ Error creating division leaders chart: {e}")
                ax3.text(0.5, 0.5, f'Chart error: {str(e)[:50]}...', ha='center', va='center', 
                        transform=ax3.transAxes, fontsize=10, color='red')
            
            # 4. Point Differential by Conference
            try:
                ax4 = fig.add_subplot(gs[1, :])
                if 'Point_Diff' in standings_df.columns and 'Conference' in standings_df.columns:
                    afc_diff = standings_df[standings_df['Conference'] == 'AFC'].sort_values('Point_Diff', ascending=False)
                    nfc_diff = standings_df[standings_df['Conference'] == 'NFC'].sort_values('Point_Diff', ascending=False)
                    
                    x_afc = np.arange(len(afc_diff))
                    x_nfc = np.arange(len(nfc_diff)) + len(afc_diff) + 2
                    
                    colors_afc = ['#2ECC71' if x > 0 else '#E74C3C' for x in afc_diff['Point_Diff']]
                    colors_nfc = ['#2ECC71' if x > 0 else '#E74C3C' for x in nfc_diff['Point_Diff']]
                    
                    bars1 = ax4.bar(x_afc, afc_diff['Point_Diff'], color=colors_afc, alpha=0.8, label='AFC')
                    bars2 = ax4.bar(x_nfc, nfc_diff['Point_Diff'], color=colors_nfc, alpha=0.8, label='NFC')
                    
                    # Add team labels
                    all_teams = list(afc_diff['Tm']) + ['', ''] + list(nfc_diff['Tm'])
                    ax4.set_xticks(list(x_afc) + [len(afc_diff), len(afc_diff)+1] + list(x_nfc))
                    ax4.set_xticklabels(all_teams, rotation=45, ha='right', fontsize=10)
                    
                    ax4.axhline(y=0, color='white', linestyle='-', alpha=0.5, linewidth=1)
                    ax4.set_title('⚖️ Point Differential by Conference', fontsize=16, color='white', pad=20)
                    ax4.set_ylabel('Point Differential')
                    ax4.legend()
                    ax4.grid(True, alpha=0.3, axis='y')
                    print("✓ Chart 4: Point differential created")
                else:
                    ax4.text(0.5, 0.5, 'Point differential data not available', ha='center', va='center', 
                            transform=ax4.transAxes, fontsize=12, color='white')
                    ax4.set_title('⚖️ Point Differential by Conference', fontsize=16, color='white')
            except Exception as e:
                print(f"⚠️ Error creating point differential chart: {e}")
                ax4.text(0.5, 0.5, f'Chart error: {str(e)[:50]}...', ha='center', va='center', 
                        transform=ax4.transAxes, fontsize=10, color='red')
            
            # 5. Team Efficiency Metrics (if detailed stats available)
            ax5 = fig.add_subplot(gs[2, 0])
            if detailed_stats and 'offense' in detailed_stats:
                offense_df = detailed_stats['offense'].copy()
                print(f"Debug: Offense columns: {list(offense_df.columns)}")
                
                # Handle duplicate column names by making them unique
                if len(offense_df.columns) != len(set(offense_df.columns)):
                    print("Debug: Found duplicate columns, making them unique...")
                    # Make columns unique by adding suffixes
                    new_columns = []
                    col_count = {}
                    for col in offense_df.columns:
                        if col in col_count:
                            col_count[col] += 1
                            new_columns.append(f"{col}_{col_count[col]}")
                        else:
                            col_count[col] = 0
                            new_columns.append(col)
                    offense_df.columns = new_columns
                    print(f"Debug: Updated columns: {list(offense_df.columns)}")
                
                # Look for yards column with different possible names
                yards_col = None
                possible_yards_cols = ['Yds', 'Yds_1', 'Yds_2', 'Yds/G', 'Total Yds', 'Off Yds', 'Yards']
                
                for col in possible_yards_cols:
                    if col in offense_df.columns:
                        yards_col = col
                        print(f"Debug: Using yards column: {yards_col}")
                        break
                
                if yards_col and 'Tm' in offense_df.columns:
                    try:
                        # Safely get the yards column data
                        yards_data = offense_df[yards_col]
                        
                        # If we got a DataFrame (multiple columns with same name), take the first one
                        if isinstance(yards_data, pd.DataFrame):
                            print(f"Debug: Found DataFrame for {yards_col}, taking first column")
                            yards_data = yards_data.iloc[:, 0]
                        
                        # Convert to numeric
                        numeric_yards = pd.to_numeric(yards_data, errors='coerce')
                        
                        # Create new column with unique name
                        offense_df['yards_numeric'] = numeric_yards
                        
                        # Remove any NaN values
                        valid_offense = offense_df.dropna(subset=['yards_numeric'])
                        
                        if not valid_offense.empty:
                            top_offense = valid_offense.nlargest(min(16, len(valid_offense)), 'yards_numeric')
                            
                            colors = ['#FF6B35' if team in self.afc_teams else '#004E89' 
                                     for team in top_offense['Tm']]
                            
                            bars = ax5.bar(range(len(top_offense)), top_offense['yards_numeric'], 
                                          color=colors, alpha=0.8)
                            ax5.set_title(f'🏃 {yards_col} by Team', fontsize=12, color='white')
                            ax5.set_ylabel(yards_col)
                            ax5.set_xticks(range(len(top_offense)))
                            ax5.set_xticklabels(top_offense['Tm'], rotation=45, ha='right', fontsize=9)
                            ax5.grid(True, alpha=0.3, axis='y')
                            print("✓ Chart 5: Offensive yards created")
                        else:
                            ax5.text(0.5, 0.5, 'No valid offensive data after processing', ha='center', va='center', 
                                    transform=ax5.transAxes, fontsize=12, color='white')
                            ax5.set_title('🏃 Offensive Stats', fontsize=12, color='white')
                    except Exception as e:
                        print(f"⚠️ Error processing yards column: {e}")
                        import traceback
                        traceback.print_exc()
                        ax5.text(0.5, 0.5, f'Data processing error\n{str(e)[:30]}...', ha='center', va='center', 
                                transform=ax5.transAxes, fontsize=10, color='white')
                        ax5.set_title('🏃 Offensive Stats', fontsize=12, color='white')
                else:
                    ax5.text(0.5, 0.5, f'Yards column not found\nAvailable: {list(offense_df.columns)[:5]}...', 
                            ha='center', va='center', transform=ax5.transAxes, fontsize=10, color='white')
                    ax5.set_title('🏃 Offensive Stats', fontsize=12, color='white')
            else:
                ax5.text(0.5, 0.5, 'No offensive data available', ha='center', va='center', 
                        transform=ax5.transAxes, fontsize=12, color='white')
                ax5.set_title('🏃 Offensive Stats', fontsize=12, color='white')
            
            # Remove axis for empty charts
            if not (detailed_stats and 'offense' in detailed_stats):
                ax5.set_xticks([])
                ax5.set_yticks([])
            
            # 6. Conference Summary Stats
            ax6 = fig.add_subplot(gs[2, 1:])
            if 'Conference' in standings_df.columns:
                conf_stats = standings_df.groupby('Conference').agg({
                    'W': 'sum',
                    'L': 'sum',
                    'PF': 'mean',
                    'PA': 'mean',
                    'Point_Diff': 'mean',
                    'Win_Pct': 'mean'
                }).round(2)
                
                x = np.arange(len(conf_stats))
                width = 0.35
                
                bars1 = ax6.bar(x - width/2, conf_stats['PF'], width, 
                               label='Avg Points For', color='#2ECC71', alpha=0.8)
                bars2 = ax6.bar(x + width/2, conf_stats['PA'], width, 
                               label='Avg Points Against', color='#E74C3C', alpha=0.8)
                
                ax6.set_title('🏟️ Conference Comparison - Scoring', fontsize=14, color='white', pad=20)
                ax6.set_ylabel('Average Points')
                ax6.set_xticks(x)
                ax6.set_xticklabels(conf_stats.index, fontsize=12)
                ax6.legend()
                ax6.grid(True, alpha=0.3, axis='y')
                
                # Add value labels on bars
                for bar in bars1:
                    height = bar.get_height()
                    ax6.text(bar.get_x() + bar.get_width()/2., height + 1,
                            f'{height:.1f}', ha='center', va='bottom', fontsize=10)
                
                for bar in bars2:
                    height = bar.get_height()
                    ax6.text(bar.get_x() + bar.get_width()/2., height + 1,
                            f'{height:.1f}', ha='center', va='bottom', fontsize=10)
            
            # 7. Model Information
            ax7 = fig.add_subplot(gs[3, :])
            info_text = f"""
🏈 NFL TEAM ANALYTICS DASHBOARD - {self.current_season} SEASON

📊 DATA SOURCES: Pro Football Reference - Team standings, offensive/defensive statistics, conference breakdowns
⚖️ KEY METRICS: Win percentage, point differential, offensive vs defensive efficiency, division standings  
🏆 ANALYSIS: AFC vs NFC performance comparison, division leader tracking, scoring trends by conference
📈 VISUALIZATION: Real-time team performance metrics with conference-based color coding (AFC: Orange, NFC: Blue)

Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            ax7.text(0.05, 0.5, info_text.strip(), fontsize=11, color='lightblue',
                    transform=ax7.transAxes, verticalalignment='center')
            ax7.set_xlim(0, 1)
            ax7.set_ylim(0, 1)
            ax7.axis('off')
            
            # Overall title
            plt.suptitle(f'🏈 NFL Team Performance Dashboard - {self.current_season} Season', 
                        fontsize=20, color='white', y=0.98)
            
            # Save the chart
            chart_path = self.docs_dir / "team_advanced_analytics.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='black', 
                       edgecolor='none', pad_inches=0.2)
            plt.close()
            
            print(f"✅ Team analytics charts saved to {chart_path}")
            
        except Exception as e:
            print(f"❌ Error creating team charts: {e}")
            import traceback
            traceback.print_exc()
            plt.close()
    
    def save_team_data(self, standings_df, detailed_stats=None):
        """Save team data to files"""
        if standings_df.empty:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save standings data
        standings_file = self.docs_dir / "team_standings.csv"
        standings_df.to_csv(standings_file, index=False)
        
        archive_file = self.archive_dir / f"team_standings_{timestamp}.csv"
        standings_df.to_csv(archive_file, index=False)
        
        # Save detailed stats if available
        if detailed_stats:
            for stat_type, df in detailed_stats.items():
                if not df.empty:
                    detail_file = self.docs_dir / f"team_{stat_type}.csv"
                    df.to_csv(detail_file, index=False)
        
        # Update timestamp
        timestamp_file = self.docs_dir / "last_updated_team_charts.txt"
        with open(timestamp_file, 'w') as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        print(f"✅ Team data saved to CSV files")
    
    def process_team_charts(self):
        """Main processing function"""
        print("🏈 NFL TEAM CHARTS PROCESSOR")
        print("=" * 50)
        print(f"Processing {self.current_season} NFL season team analytics...")
        
        # Fetch team standings
        print("\n1. Fetching team standings...")
        standings_df = self.fetch_team_standings()
        
        if standings_df.empty:
            print("❌ No standings data found - cannot create charts")
            return
        
        print(f"✅ Retrieved standings for {len(standings_df)} teams")
        print(f"   Columns: {list(standings_df.columns)}")
        
        # Fetch detailed stats
        print("\n2. Fetching detailed team statistics...")
        detailed_stats = self.fetch_team_offense_defense()
        
        if detailed_stats:
            print(f"✅ Retrieved {len(detailed_stats)} detailed stat categories")
            for stat_type, df in detailed_stats.items():
                print(f"   {stat_type}: {len(df)} teams")
        
        # Create charts
        print("\n3. Creating comprehensive team charts...")
        self.create_comprehensive_team_charts(standings_df, detailed_stats)
        
        # Save data
        print("\n4. Saving team data...")
        self.save_team_data(standings_df, detailed_stats)
        
        print("\n" + "=" * 50)
        print("🏆 TEAM CHARTS PROCESSING COMPLETE!")
        print("=" * 50)

if __name__ == "__main__":
    # Ensure directories exist
    charts = NFLTeamCharts()
    
    charts.docs_dir.mkdir(parents=True, exist_ok=True)
    charts.archive_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Created directories:")
    print(f"  Docs: {charts.docs_dir}")
    print(f"  Archive: {charts.archive_dir}")
    
    charts.process_team_charts()