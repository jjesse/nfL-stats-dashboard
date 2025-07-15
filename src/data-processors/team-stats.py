import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from pathlib import Path
import time

class NFLTeamStats:
    def __init__(self):
        self.base_url = "https://www.pro-football-reference.com"
        self.current_season = self.get_current_nfl_season()
        self.docs_dir = Path(__file__).parent.parent.parent / "docs"
        self.archive_dir = Path(__file__).parent.parent.parent / "archive"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print(f"Initialized NFL Team Stats processor for {self.current_season}-{self.current_season + 1} season")
        
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
        
    def fetch_team_standings(self):
        """Fetch current NFL standings (AFC/NFC)"""
        try:
            url = f"{self.base_url}/years/{self.current_season}/"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            tables = pd.read_html(response.content)
            standings_data = []
            
            for table in tables:
                # Look for tables that contain team standings info
                if 'W' in table.columns and 'L' in table.columns:
                    if table.columns.nlevels > 1:
                        table.columns = table.columns.droplevel(0)
                    
                    # Clean up the data
                    table = table[table['Tm'].notna()]  # Remove NaN teams
                    table = table[table['Tm'] != 'Tm']  # Remove header rows
                    standings_data.append(table)
            
            if standings_data:
                # Combine all standings tables
                combined_df = pd.concat(standings_data, ignore_index=True)
                return combined_df
            
            return pd.DataFrame()
            
        except Exception as e:
            print(f"Error fetching standings: {e}")
            return pd.DataFrame()
    
    def fetch_team_offense_defense_stats(self):
        """Fetch detailed offensive and defensive team statistics"""
        team_stats = {}
        
        try:
            # Offensive stats
            print("Fetching offensive team stats...")
            offense_url = f"{self.base_url}/years/{self.current_season}/opp.htm"
            response = requests.get(offense_url, headers=self.headers)
            if response.status_code == 200:
                offense_tables = pd.read_html(response.content)
                if offense_tables:
                    offense_df = offense_tables[0]
                    if offense_df.columns.nlevels > 1:
                        offense_df.columns = offense_df.columns.droplevel(0)
                    team_stats['offense'] = offense_df
            
            time.sleep(1)  # Be respectful to the server
            
            # Defensive stats  
            print("Fetching defensive team stats...")
            defense_url = f"{self.base_url}/years/{self.current_season}/opp.htm"
            response = requests.get(defense_url, headers=self.headers)
            if response.status_code == 200:
                defense_tables = pd.read_html(response.content)
                if defense_tables and len(defense_tables) > 1:
                    defense_df = defense_tables[1] if len(defense_tables) > 1 else defense_tables[0]
                    if defense_df.columns.nlevels > 1:
                        defense_df.columns = defense_df.columns.droplevel(0)
                    team_stats['defense'] = defense_df
                    
        except Exception as e:
            print(f"Error fetching offense/defense stats: {e}")
            
        return team_stats

    def create_comprehensive_team_charts(self, standings_df, detailed_stats=None):
        """Create comprehensive team visualization charts"""
        if standings_df.empty:
            print("No standings data available for charts")
            return
            
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(20, 15))
        
        # Create a more complex layout
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        try:
            # 1. Win Percentage by Division
            ax1 = fig.add_subplot(gs[0, 0])
            if 'W' in standings_df.columns and 'L' in standings_df.columns:
                standings_df['W'] = pd.to_numeric(standings_df['W'], errors='coerce')
                standings_df['L'] = pd.to_numeric(standings_df['L'], errors='coerce')
                standings_df['Win_Pct'] = standings_df['W'] / (standings_df['W'] + standings_df['L'])
                
                # Sort by win percentage
                sorted_teams = standings_df.nlargest(32, 'Win_Pct')
                team_names = [str(row.get('Tm', f'Team {i}'))[:3] for i, row in sorted_teams.iterrows()]
                
                bars = ax1.bar(range(len(sorted_teams)), sorted_teams['Win_Pct'], 
                              color=['#2ca02c' if x > 0.5 else '#d62728' for x in sorted_teams['Win_Pct']])
                ax1.set_title('Team Win Percentage', fontsize=12, color='white')
                ax1.set_ylabel('Win %')
                ax1.set_xticks(range(len(sorted_teams)))
                ax1.set_xticklabels(team_names, rotation=45, ha='right', fontsize=8)
                ax1.grid(True, alpha=0.3)
            
            # 2. Points For vs Points Against Scatter
            ax2 = fig.add_subplot(gs[0, 1])
            if 'PF' in standings_df.columns and 'PA' in standings_df.columns:
                standings_df['PF'] = pd.to_numeric(standings_df['PF'], errors='coerce')
                standings_df['PA'] = pd.to_numeric(standings_df['PA'], errors='coerce')
                
                scatter = ax2.scatter(standings_df['PF'], standings_df['PA'], 
                                    alpha=0.7, s=100, c=standings_df['Win_Pct'], 
                                    cmap='RdYlGn', edgecolors='white', linewidth=1)
                ax2.set_xlabel('Points For')
                ax2.set_ylabel('Points Against')
                ax2.set_title('Offensive vs Defensive Performance', fontsize=12, color='white')
                ax2.grid(True, alpha=0.3)
                
                # Add diagonal line for equal points
                max_points = max(standings_df['PF'].max(), standings_df['PA'].max())
                ax2.plot([0, max_points], [0, max_points], 'r--', alpha=0.5, label='Equal Points')
                ax2.legend()
                
                # Add colorbar
                plt.colorbar(scatter, ax=ax2, label='Win %')
            
            # 3. Point Differential
            ax3 = fig.add_subplot(gs[0, 2])
            if 'PF' in standings_df.columns and 'PA' in standings_df.columns:
                standings_df['Point_Diff'] = standings_df['PF'] - standings_df['PA']
                sorted_diff = standings_df.nlargest(32, 'Point_Diff')
                team_names = [str(row.get('Tm', f'Team {i}'))[:3] for i, row in sorted_diff.iterrows()]
                
                colors = ['#2ca02c' if x > 0 else '#d62728' for x in sorted_diff['Point_Diff']]
                ax3.bar(range(len(sorted_diff)), sorted_diff['Point_Diff'], color=colors, alpha=0.8)
                ax3.set_title('Point Differential', fontsize=12, color='white')
                ax3.set_ylabel('Point Differential')
                ax3.set_xticks(range(len(sorted_diff)))
                ax3.set_xticklabels(team_names, rotation=45, ha='right', fontsize=8)
                ax3.axhline(y=0, color='white', linestyle='-', alpha=0.5)
                ax3.grid(True, alpha=0.3)
            
            # 4. Conference Breakdown
            ax4 = fig.add_subplot(gs[1, :])
            # Try to determine conference from team names
            afc_teams = ['BUF', 'MIA', 'NWE', 'NYJ', 'BAL', 'CIN', 'CLE', 'PIT', 
                        'HOU', 'IND', 'JAX', 'TEN', 'DEN', 'KAN', 'LVR', 'LAC']
            
            if 'Tm' in standings_df.columns:
                standings_df['Conference'] = standings_df['Tm'].apply(
                    lambda x: 'AFC' if x in afc_teams else 'NFC'
                )
                
                conf_stats = standings_df.groupby('Conference').agg({
                    'W': 'sum',
                    'L': 'sum', 
                    'PF': 'mean',
                    'PA': 'mean'
                }).reset_index()
                
                x_pos = range(len(conf_stats))
                width = 0.35
                
                ax4.bar([x - width/2 for x in x_pos], conf_stats['PF'], width, 
                       label='Avg Points For', color='#1f77b4', alpha=0.8)
                ax4.bar([x + width/2 for x in x_pos], conf_stats['PA'], width, 
                       label='Avg Points Against', color='#ff7f0e', alpha=0.8)
                
                ax4.set_title('Conference Comparison - Avg Points', fontsize=14, color='white')
                ax4.set_ylabel('Average Points')
                ax4.set_xticks(x_pos)
                ax4.set_xticklabels(conf_stats['Conference'])
                ax4.legend()
                ax4.grid(True, alpha=0.3)
            
            # 5. Additional charts if we have detailed stats
            if detailed_stats and 'offense' in detailed_stats:
                offense_df = detailed_stats['offense']
                
                # Yards per game
                ax5 = fig.add_subplot(gs[2, 0])
                if 'Yds' in offense_df.columns:
                    offense_df['Yds'] = pd.to_numeric(offense_df['Yds'], errors='coerce')
                    top_offense = offense_df.nlargest(16, 'Yds')
                    team_names = [str(row.get('Tm', f'Team {i}'))[:3] for i, row in top_offense.iterrows()]
                    
                    ax5.bar(range(len(top_offense)), top_offense['Yds'], color='#9467bd', alpha=0.8)
                    ax5.set_title('Offensive Yards per Game', fontsize=12, color='white')
                    ax5.set_ylabel('Yards')
                    ax5.set_xticks(range(len(top_offense)))
                    ax5.set_xticklabels(team_names, rotation=45, ha='right', fontsize=8)
                    ax5.grid(True, alpha=0.3)
            
            # Save the comprehensive chart
            plt.suptitle(f'NFL Team Statistics Dashboard - {self.current_season}', 
                        fontsize=20, color='white', y=0.98)
            
            chart_path = self.docs_dir / "team_stats.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='black', 
                       edgecolor='none', pad_inches=0.2)
            plt.close()
            
            print(f"✓ Comprehensive team charts saved to {chart_path}")
            
        except Exception as e:
            print(f"Error creating comprehensive charts: {e}")
            plt.close()

    def save_data(self, df, data_type="standings"):
        """Save team data with enhanced organization"""
        if df.empty:
            return
            
        # Save current data
        current_file = self.docs_dir / f"team_{data_type}.csv"
        df.to_csv(current_file, index=False)
        
        # Save to archive
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = self.archive_dir / f"team_{data_type}_{timestamp}.csv"
        df.to_csv(archive_file, index=False)
        
        # Update timestamp
        timestamp_file = self.docs_dir / f"last_updated_team_{data_type}.txt"
        with open(timestamp_file, 'w') as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def process_all_team_stats(self):
        """Process all team statistics with enhanced data collection"""
        print("=" * 60)
        print("🏈 NFL TEAM STATISTICS PROCESSOR")
        print("=" * 60)
        print(f"Processing {self.current_season} NFL season data...")
        
        all_stats = {}
        
        # Fetch standings data
        print("\n1. Fetching team standings...")
        standings_df = self.fetch_team_standings()
        
        if not standings_df.empty:
            print(f"✓ Found data for {len(standings_df)} teams")
            print("Sample columns:", list(standings_df.columns)[:10])
            self.save_data(standings_df, "standings")
            all_stats['standings'] = standings_df
        else:
            print("✗ No standings data found")
            
        # Fetch detailed offensive/defensive stats
        print("\n2. Fetching detailed team statistics...")
        detailed_stats = self.fetch_team_offense_defense_stats()
        all_stats.update(detailed_stats)
        
        for stat_type, df in detailed_stats.items():
            if not df.empty:
                print(f"✓ Found {stat_type} data: {len(df)} teams")
                self.save_data(df, stat_type)
            else:
                print(f"✗ No {stat_type} data found")
        
        # Create comprehensive visualizations
        print("\n3. Creating comprehensive charts...")
        if not standings_df.empty:
            self.create_comprehensive_team_charts(standings_df, detailed_stats)
            print("✓ Team charts created successfully")
        else:
            print("✗ Cannot create charts without standings data")
        
        print("\n" + "=" * 60)
        print("🏆 TEAM STATISTICS PROCESSING COMPLETE!")
        print("=" * 60)
        print(f"📊 Data sources processed: {len(all_stats)}")
        print(f"📈 Charts generated: team_stats.png")
        print("=" * 60)

if __name__ == "__main__":
    # Ensure directories exist using Path objects for better cross-platform support
    processor = NFLTeamStats()
    
    # Create directories using the processor's path objects
    processor.docs_dir.mkdir(parents=True, exist_ok=True)
    processor.archive_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Created directories:")
    print(f"  Docs: {processor.docs_dir}")
    print(f"  Archive: {processor.archive_dir}")
    
    processor.process_all_team_stats()