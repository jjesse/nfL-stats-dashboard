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
        print(f"Initialized NFL Stats processor for {self.current_season}-{self.current_season + 1} season")
        
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
        
    def fetch_advanced_team_stats(self):
        """Fetch advanced team statistics like red zone efficiency, 3rd down conversions"""
        try:
            print("Fetching advanced team statistics...")
            # Try to get team stats page
            url = f"{self.base_url}/years/{self.current_season}/opp.htm"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            tables = pd.read_html(response.content)
            advanced_stats = {}
            
            # Look for different stat tables
            for i, table in enumerate(tables):
                if table.columns.nlevels > 1:
                    table.columns = table.columns.droplevel(0)
                
                # Red Zone stats, 3rd down stats, etc.
                if any(col for col in table.columns if 'Rd' in str(col) or '3D' in str(col)):
                    advanced_stats[f'advanced_{i}'] = table
                    
            return advanced_stats
            
        except Exception as e:
            print(f"Error fetching advanced stats: {e}")
            return {}

    def fetch_team_efficiency_stats(self):
        """Fetch team efficiency statistics - red zone, third down, etc."""
        efficiency_stats = {}
        
        try:
            print("Fetching team efficiency statistics...")
            
            # Red Zone efficiency
            red_zone_url = f"{self.base_url}/years/{self.current_season}/redzone.htm"
            response = requests.get(red_zone_url, headers=self.headers)
            if response.status_code == 200:
                red_zone_tables = pd.read_html(response.content)
                if red_zone_tables:
                    red_zone_df = red_zone_tables[0]
                    if red_zone_df.columns.nlevels > 1:
                        red_zone_df.columns = red_zone_df.columns.droplevel(0)
                    efficiency_stats['red_zone'] = red_zone_df
                    print(f"✓ Red zone data: {len(red_zone_df)} teams")
            
            time.sleep(1)
            
            # Third down conversions (if available)
            third_down_url = f"{self.base_url}/years/{self.current_season}/conv.htm"
            response = requests.get(third_down_url, headers=self.headers)
            if response.status_code == 200:
                third_down_tables = pd.read_html(response.content)
                if third_down_tables:
                    third_down_df = third_down_tables[0]
                    if third_down_df.columns.nlevels > 1:
                        third_down_df.columns = third_down_df.columns.droplevel(0)
                    efficiency_stats['third_down'] = third_down_df
                    print(f"✓ Third down data: {len(third_down_df)} teams")
                    
        except Exception as e:
            print(f"Error fetching efficiency stats: {e}")
            
        return efficiency_stats
    
    def fetch_team_turnover_stats(self):
        """Fetch turnover and penalty statistics"""
        try:
            print("Fetching turnover and penalty stats...")
            turnover_url = f"{self.base_url}/years/{self.current_season}/opp.htm"
            response = requests.get(turnover_url, headers=self.headers)
            response.raise_for_status()
            
            tables = pd.read_html(response.content)
            turnover_stats = {}
            
            for i, table in enumerate(tables):
                if table.columns.nlevels > 1:
                    table.columns = table.columns.droplevel(0)
                
                # Look for turnover-related columns
                if any(col for col in table.columns if 'TO' in str(col) or 'Int' in str(col) or 'Fmb' in str(col)):
                    turnover_stats[f'turnovers_{i}'] = table
                    print(f"✓ Found turnover data table {i}: {len(table)} teams")
                    
            return turnover_stats
            
        except Exception as e:
            print(f"Error fetching turnover stats: {e}")
            return {}

    def fetch_special_teams_stats(self):
        """Fetch special teams statistics"""
        try:
            print("Fetching special teams stats...")
            special_teams_stats = {}
            
            # Kicking stats
            kicking_url = f"{self.base_url}/years/{self.current_season}/kicking.htm"
            response = requests.get(kicking_url, headers=self.headers)
            if response.status_code == 200:
                kicking_tables = pd.read_html(response.content)
                if kicking_tables:
                    kicking_df = kicking_tables[0]
                    if kicking_df.columns.nlevels > 1:
                        kicking_df.columns = kicking_df.columns.droplevel(0)
                    special_teams_stats['kicking'] = kicking_df
                    print(f"✓ Kicking data: {len(kicking_df)} teams")
            
            time.sleep(1)
            
            # Punt return stats
            punt_url = f"{self.base_url}/years/{self.current_season}/returns.htm"
            response = requests.get(punt_url, headers=self.headers)
            if response.status_code == 200:
                punt_tables = pd.read_html(response.content)
                if punt_tables:
                    punt_df = punt_tables[0]
                    if punt_df.columns.nlevels > 1:
                        punt_df.columns = punt_df.columns.droplevel(0)
                    special_teams_stats['returns'] = punt_df
                    print(f"✓ Return data: {len(punt_df)} teams")
                    
            return special_teams_stats
            
        except Exception as e:
            print(f"Error fetching special teams stats: {e}")
            return {}

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
            # This would show AFC vs NFC stats if we can determine conference
            wins_by_conf = []
            conf_labels = []
            
            # Try to determine conference from team names or other indicators
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
            
            # 5 & 6. Additional charts if we have detailed stats
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

    def create_advanced_analytics_charts(self, all_stats):
        """Create advanced analytics visualizations"""
        if not all_stats.get('standings') or all_stats['standings'].empty:
            print("No data available for advanced analytics charts")
            return
            
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(24, 18))
        gs = fig.add_gridspec(4, 4, hspace=0.4, wspace=0.3)
        
        standings_df = all_stats['standings']
        
        try:
            # 1. Pythagorean Win Expectation
            ax1 = fig.add_subplot(gs[0, 0])
            if 'PF' in standings_df.columns and 'PA' in standings_df.columns:
                standings_df['PF'] = pd.to_numeric(standings_df['PF'], errors='coerce')
                standings_df['PA'] = pd.to_numeric(standings_df['PA'], errors='coerce')
                standings_df['W'] = pd.to_numeric(standings_df['W'], errors='coerce')
                standings_df['L'] = pd.to_numeric(standings_df['L'], errors='coerce')
                
                # Calculate Pythagorean expectation
                standings_df['Pyth_Wins'] = standings_df['PF']**2 / (standings_df['PF']**2 + standings_df['PA']**2)
                standings_df['Actual_Win_Pct'] = standings_df['W'] / (standings_df['W'] + standings_df['L'])
                
                scatter = ax1.scatter(standings_df['Pyth_Wins'], standings_df['Actual_Win_Pct'], 
                                    alpha=0.7, s=100, c='cyan', edgecolors='white')
                ax1.plot([0, 1], [0, 1], 'r--', alpha=0.5, label='Perfect Correlation')
                ax1.set_xlabel('Pythagorean Win %')
                ax1.set_ylabel('Actual Win %')
                ax1.set_title('Pythagorean Expectation vs Reality', fontsize=10, color='white')
                ax1.grid(True, alpha=0.3)
                ax1.legend()
            
            # 2. Strength of Schedule Analysis
            ax2 = fig.add_subplot(gs[0, 1])
            if 'SOS' in standings_df.columns:
                standings_df['SOS'] = pd.to_numeric(standings_df['SOS'], errors='coerce')
                sorted_sos = standings_df.nlargest(16, 'SOS')
                team_names = [str(row.get('Tm', f'Team {i}'))[:3] for i, row in sorted_sos.iterrows()]
                
                colors = ['#ff4444' if x > 0 else '#44ff44' for x in sorted_sos['SOS']]
                ax2.barh(range(len(sorted_sos)), sorted_sos['SOS'], color=colors, alpha=0.8)
                ax2.set_title('Strength of Schedule', fontsize=10, color='white')
                ax2.set_xlabel('SOS (Tougher →)')
                ax2.set_yticks(range(len(sorted_sos)))
                ax2.set_yticklabels(team_names, fontsize=8)
                ax2.grid(True, alpha=0.3)
                ax2.axvline(x=0, color='white', linestyle='-', alpha=0.5)
            
            # 3. Margin of Victory Distribution
            ax3 = fig.add_subplot(gs[0, 2])
            if 'PF' in standings_df.columns and 'PA' in standings_df.columns:
                standings_df['Margin'] = standings_df['PF'] - standings_df['PA']
                ax3.hist(standings_df['Margin'], bins=15, color='orange', alpha=0.7, edgecolor='white')
                ax3.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Even')
                ax3.set_title('Point Margin Distribution', fontsize=10, color='white')
                ax3.set_xlabel('Point Differential')
                ax3.set_ylabel('Number of Teams')
                ax3.grid(True, alpha=0.3)
                ax3.legend()
            
            # 4. Offensive vs Defensive Efficiency Heatmap
            ax4 = fig.add_subplot(gs[0, 3])
            if all_stats.get('offense') and all_stats.get('defense'):
                offense_df = all_stats['offense']
                defense_df = all_stats['defense']
                
                # Create efficiency matrix if we have the right columns
                if 'Yds' in offense_df.columns and 'Yds' in defense_df.columns:
                    offense_df['Off_Yds'] = pd.to_numeric(offense_df['Yds'], errors='coerce')
                    defense_df['Def_Yds'] = pd.to_numeric(defense_df['Yds'], errors='coerce')
                    
                    # Combine offensive and defensive yards for heatmap
                    combined = pd.merge(offense_df[['Tm', 'Off_Yds']], 
                                      defense_df[['Tm', 'Def_Yds']], on='Tm', how='inner')
                    
                    if not combined.empty:
                        scatter = ax4.scatter(combined['Off_Yds'], combined['Def_Yds'], 
                                            alpha=0.7, s=100, c='purple', edgecolors='white')
                        ax4.set_xlabel('Offensive Yards/Game')
                        ax4.set_ylabel('Defensive Yards Allowed/Game')
                        ax4.set_title('Off vs Def Efficiency', fontsize=10, color='white')
                        ax4.grid(True, alpha=0.3)
            
            # 5-8. Efficiency stats if available
            row = 1
            col = 0
            
            if all_stats.get('efficiency'):
                efficiency_stats = all_stats['efficiency']
                
                for stat_name, df in efficiency_stats.items():
                    if row >= 4:  # Don't overflow the grid
                        break
                        
                    ax = fig.add_subplot(gs[row, col])
                    
                    # Red Zone Efficiency
                    if 'red_zone' in stat_name and 'TD%' in df.columns:
                        df['TD%'] = pd.to_numeric(df['TD%'], errors='coerce')
                        top_teams = df.nlargest(10, 'TD%')
                        team_names = [str(row.get('Tm', f'Team {i}'))[:3] for i, row in top_teams.iterrows()]
                        
                        ax.bar(range(len(top_teams)), top_teams['TD%'], color='red', alpha=0.8)
                        ax.set_title('Red Zone TD%', fontsize=10, color='white')
                        ax.set_ylabel('TD %')
                        ax.set_xticks(range(len(top_teams)))
                        ax.set_xticklabels(team_names, rotation=45, ha='right', fontsize=8)
                        ax.grid(True, alpha=0.3)
                    
                    col += 1
                    if col >= 4:
                        col = 0
                        row += 1
            
            # Save the advanced analytics chart
            plt.suptitle(f'NFL Advanced Team Analytics - {self.current_season}', 
                        fontsize=24, color='white', y=0.98)
            
            chart_path = self.docs_dir / "team_advanced_analytics.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='black', 
                       edgecolor='none', pad_inches=0.2)
            plt.close()
            
            print(f"✓ Advanced analytics charts saved to {chart_path}")
            
        except Exception as e:
            print(f"Error creating advanced analytics charts: {e}")
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
        print("🏈 NFL ADVANCED TEAM STATISTICS PROCESSOR")
        print("=" * 60)
        
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
        
        # Fetch efficiency stats
        print("\n3. Fetching efficiency statistics...")
        efficiency_stats = self.fetch_team_efficiency_stats()
        if efficiency_stats:
            all_stats['efficiency'] = efficiency_stats
            for stat_name, df in efficiency_stats.items():
                if not df.empty:
                    print(f"✓ Found {stat_name}: {len(df)} teams")
                    self.save_data(df, f"efficiency_{stat_name}")
        
        # Fetch turnover stats
        print("\n4. Fetching turnover statistics...")
        turnover_stats = self.fetch_team_turnover_stats()
        if turnover_stats:
            all_stats['turnovers'] = turnover_stats
            for stat_name, df in turnover_stats.items():
                if not df.empty:
                    print(f"✓ Found {stat_name}: {len(df)} teams")
                    self.save_data(df, stat_name)
        
        # Fetch special teams stats
        print("\n5. Fetching special teams statistics...")
        special_teams_stats = self.fetch_special_teams_stats()
        if special_teams_stats:
            all_stats['special_teams'] = special_teams_stats
            for stat_name, df in special_teams_stats.items():
                if not df.empty:
                    print(f"✓ Found {stat_name}: {len(df)} teams")
                    self.save_data(df, f"special_teams_{stat_name}")
        
        # Create comprehensive visualizations
        print("\n6. Creating comprehensive charts...")
        if not standings_df.empty:
            self.create_comprehensive_team_charts(standings_df, detailed_stats)
            print("✓ Basic team charts created successfully")
            
            # Create advanced analytics
            print("\n7. Creating advanced analytics charts...")
            self.create_advanced_analytics_charts(all_stats)
            print("✓ Advanced analytics charts created successfully")
        else:
            print("✗ Cannot create charts without standings data")
        
        print("\n" + "=" * 60)
        print("🏆 ADVANCED TEAM STATISTICS PROCESSING COMPLETE!")
        print("=" * 60)
        print(f"📊 Data sources processed: {len(all_stats)}")
        print(f"📈 Charts generated: team_stats.png, team_advanced_analytics.png")
        print("=" * 60)

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs("docs", exist_ok=True)
    os.makedirs("archive", exist_ok=True)
    
    processor = NFLTeamStats()
    processor.process_all_team_stats()