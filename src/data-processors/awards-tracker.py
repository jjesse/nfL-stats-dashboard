#!/usr/bin/env python3
"""
Enhanced NFL Awards Predictor - Updated for 2024 Results
Fixed models based on actual 2024 winners:
- MVP: Josh Allen (dual-threat QB)
- OROY: Jayden Daniels (dual-threat rookie QB) 
- DROY: Jared Verse (rookie edge rusher)
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from pathlib import Path
import numpy as np
import time

class NFLAwardsPredictor:
    def __init__(self):
        self.base_url = "https://www.pro-football-reference.com"
        self.current_season = self.get_current_nfl_season()
        self.docs_dir = Path(__file__).parent.parent.parent / "docs"
        self.archive_dir = Path(__file__).parent.parent.parent / "archive"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print(f"Initialized Enhanced NFL Awards Predictor for {self.current_season}-{self.current_season + 1} season")
        
    def get_current_nfl_season(self):
        """Determine the current/most recent NFL season"""
        now = datetime.now()
        if now.month <= 7:
            return now.year - 1
        else:
            return now.year
    
    def fetch_player_data(self, stat_type):
        """Fetch player data for award calculations"""
        try:
            url = f"{self.base_url}/years/{self.current_season}/{stat_type}.htm"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
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
            print(f"Error fetching {stat_type} data: {e}")
            return pd.DataFrame()
    
    def calculate_mvp_scores(self):
        """Calculate MVP scores with enhanced Josh Allen model"""
        print("Calculating MVP predictions with enhanced model...")
        
        # Fetch passing stats for MVP calculation
        passing_df = self.fetch_player_data('passing')
        if passing_df.empty:
            print("No passing data available for MVP calculation")
            return pd.DataFrame()
        
        # Get rushing stats to add rushing TDs for QBs
        rushing_df = self.fetch_player_data('rushing')
        
        # Convert relevant columns to numeric
        numeric_cols = ['Yds', 'TD', 'Int', 'Rate', 'Cmp%', 'Y/A', 'G', 'W', 'L']
        for col in numeric_cols:
            if col in passing_df.columns:
                passing_df[col] = pd.to_numeric(passing_df[col], errors='coerce')
        
        # Add rushing TDs for QBs from rushing data
        if not rushing_df.empty:
            rushing_df['Rush_TD'] = pd.to_numeric(rushing_df['TD'], errors='coerce')
            rushing_df['Rush_Yds'] = pd.to_numeric(rushing_df['Yds'], errors='coerce')
            qb_rushing = rushing_df[rushing_df['Pos'] == 'QB'][['Player', 'Rush_TD', 'Rush_Yds']]
            passing_df = passing_df.merge(qb_rushing, on='Player', how='left')
            passing_df['Rush_TD'] = passing_df['Rush_TD'].fillna(0)
            passing_df['Rush_Yds'] = passing_df['Rush_Yds'].fillna(0)
        else:
            passing_df['Rush_TD'] = 0
            passing_df['Rush_Yds'] = 0
        
        # Enhanced MVP scoring formula (based on Josh Allen 2024 win)
        mvp_scores = []
        
        for idx, row in passing_df.iterrows():
            score = 0
            
            # 1. TOTAL TOUCHDOWNS (35% weight) - Josh Allen had 43 total TDs vs Lamar's 28
            total_tds = 0
            if 'TD' in row and pd.notna(row['TD']):
                total_tds += row['TD']
            if 'Rush_TD' in row and pd.notna(row['Rush_TD']):
                total_tds += row['Rush_TD']
            
            if total_tds >= 40:
                score += 35  # Elite total production
            elif total_tds >= 35:
                score += 30
            elif total_tds >= 30:
                score += 25
            elif total_tds >= 25:
                score += 20
            else:
                score += max(0, total_tds - 15) * 1.5
            
            # 2. TEAM SUCCESS (25% weight) - Reduced from 40%
            if 'W' in row and 'L' in row and pd.notna(row['W']) and pd.notna(row['L']):
                wins = row['W']
                win_pct = wins / (wins + row['L']) if (wins + row['L']) > 0 else 0
                
                if wins >= 13:  # Elite team
                    score += 25
                elif wins >= 11:  # Good team
                    score += 20
                elif wins >= 9:  # Decent team
                    score += 15
                elif wins >= 7:  # Average team
                    score += 10
            
            # 3. QB EFFICIENCY (20% weight)
            if 'Rate' in row and pd.notna(row['Rate']):
                qb_rating = row['Rate']
                if qb_rating >= 110:
                    score += 20
                elif qb_rating >= 100:
                    score += 15
                elif qb_rating >= 95:
                    score += 10
                elif qb_rating >= 90:
                    score += 5
            
            # 4. TURNOVER PROTECTION (10% weight)
            if 'Int' in row and pd.notna(row['Int']):
                ints = row['Int']
                if ints <= 5:
                    score += 10
                elif ints <= 8:
                    score += 8
                elif ints <= 12:
                    score += 5
            
            # 5. DUAL-THREAT BONUS (10% weight) - Key differentiator for Josh Allen
            if 'Rush_TD' in row and pd.notna(row['Rush_TD']):
                rush_tds = row['Rush_TD']
                if rush_tds >= 12:  # Elite rushing QB
                    score += 10
                elif rush_tds >= 8:   # Very good
                    score += 8
                elif rush_tds >= 5:   # Good
                    score += 5
                elif rush_tds >= 3:   # Decent
                    score += 3
            
            mvp_scores.append(score)
        
        passing_df['MVP_Score'] = mvp_scores
        
        # Get top MVP candidates
        available_cols = ['Player', 'MVP_Score']
        for col in ['Tm', 'Team', 'W', 'L', 'Yds', 'TD', 'Rush_TD', 'Int', 'Rate']:
            if col in passing_df.columns:
                available_cols.append(col)
        
        mvp_candidates = passing_df.nlargest(15, 'MVP_Score')[available_cols]
        
        if not mvp_candidates.empty:
            print(f"✓ Generated MVP predictions for {len(mvp_candidates)} candidates")
            print(f"  Top candidate: {mvp_candidates.iloc[0]['Player']} - {mvp_candidates.iloc[0]['MVP_Score']} points")
        
        return mvp_candidates
    
    def calculate_oroy_scores(self):
        """Calculate Enhanced OROY scores - Updated for Jayden Daniels model"""
        print("Calculating OROY predictions with enhanced mobile QB model...")
        
        # Fetch all offensive position data
        passing_df = self.fetch_player_data('passing')
        rushing_df = self.fetch_player_data('rushing')
        receiving_df = self.fetch_player_data('receiving')
        
        oroy_candidates = []
        
        # Process QB candidates (key for 2024: Jayden Daniels won!)
        if not passing_df.empty:
            numeric_cols = ['Yds', 'TD', 'Int', 'Rate', 'W', 'L', 'Age']
            for col in numeric_cols:
                if col in passing_df.columns:
                    passing_df[col] = pd.to_numeric(passing_df[col], errors='coerce')
            
            # Add rushing stats for QBs from rushing data
            if not rushing_df.empty:
                rushing_df['Rush_TD'] = pd.to_numeric(rushing_df['TD'], errors='coerce')
                rushing_df['Rush_Yds'] = pd.to_numeric(rushing_df['Yds'], errors='coerce')
                qb_rushing = rushing_df[rushing_df['Pos'] == 'QB'][['Player', 'Rush_TD', 'Rush_Yds']]
                passing_df = passing_df.merge(qb_rushing, on='Player', how='left')
                passing_df['Rush_TD'] = passing_df['Rush_TD'].fillna(0)
                passing_df['Rush_Yds'] = passing_df['Rush_Yds'].fillna(0)
            
            # Focus on rookie QBs - Jayden Daniels model
            for idx, row in passing_df.iterrows():
                # Check if likely rookie (age <= 24 or has ORoY award)
                is_rookie = False
                if 'Age' in row and pd.notna(row['Age']) and row['Age'] <= 24:
                    is_rookie = True
                if 'Awards' in row and pd.notna(row['Awards']) and 'ORoY' in str(row['Awards']):
                    is_rookie = True
                
                if is_rookie:
                    score = 0
                    
                    # 1. Dual-threat ability (40% weight) - Jayden's key advantage
                    total_tds = 0
                    if 'TD' in row and pd.notna(row['TD']):
                        total_tds += row['TD']
                    if 'Rush_TD' in row and pd.notna(row['Rush_TD']):
                        total_tds += row['Rush_TD']
                    
                    rushing_yards = row.get('Rush_Yds', 0) if pd.notna(row.get('Rush_Yds', 0)) else 0
                    
                    # Dual-threat bonus (key for Jayden)
                    if rushing_yards >= 800:  # Elite rushing QB
                        score += 40
                    elif rushing_yards >= 500:  # Good rushing QB
                        score += 30
                    elif rushing_yards >= 200:  # Mobile QB
                        score += 20
                    
                    # Total TD production
                    if total_tds >= 30:
                        score += 15
                    elif total_tds >= 25:
                        score += 10
                    elif total_tds >= 20:
                        score += 5
                    
                    # 2. Team Success (25% weight)
                    if 'W' in row and pd.notna(row['W']):
                        wins = row['W']
                        if wins >= 12:  # Playoff team
                            score += 25
                        elif wins >= 10:  # Good season
                            score += 20
                        elif wins >= 8:  # Decent for rookie
                            score += 15
                        elif wins >= 6:  # Average rookie
                            score += 10
                    
                    # 3. Passing efficiency (20% weight)
                    if 'Rate' in row and pd.notna(row['Rate']):
                        qb_rating = row['Rate']
                        if qb_rating >= 100:
                            score += 20
                        elif qb_rating >= 90:
                            score += 15
                        elif qb_rating >= 85:
                            score += 10
                    
                    # 4. Volume stats (15% weight)
                    if 'Yds' in row and pd.notna(row['Yds']):
                        pass_yards = row['Yds']
                        if pass_yards >= 3500:
                            score += 15
                        elif pass_yards >= 3000:
                            score += 10
                        elif pass_yards >= 2500:
                            score += 5
                    
                    if score > 0:
                        candidate = {
                            'Player': row['Player'],
                            'Position': 'QB',
                            'Team': row.get('Team', row.get('Tm', 'N/A')),
                            'Primary_Stat': f"{rushing_yards} Rush Yds, {total_tds} Total TDs",
                            'OROY_Score': score
                        }
                        oroy_candidates.append(candidate)
        
        # Process other positions (but with reduced weighting since QB won)
        for df_name, df, pos_type in [('rushing', rushing_df, 'RB'), ('receiving', receiving_df, 'WR/TE')]:
            if df.empty:
                continue
                
            numeric_cols = ['Yds', 'TD', 'Age']
            if pos_type == 'RB':
                numeric_cols.extend(['Att', 'Y/A'])
            else:
                numeric_cols.extend(['Rec', 'Y/R'])
            
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            for idx, row in df.head(50).iterrows():
                if 'Player' in row and pd.notna(row['Player']):
                    age = row.get('Age', 30)
                    awards = str(row.get('Awards', ''))
                    is_rookie = ('ORoY' in awards or age <= 23)
                    
                    if is_rookie and age <= 25:
                        score = 0
                        
                        if pos_type == 'RB':
                            if 'Yds' in row and pd.notna(row['Yds']):
                                score += row['Yds'] / 25
                            if 'TD' in row and pd.notna(row['TD']):
                                score += row['TD'] * 6
                        else:  # WR/TE
                            if 'Rec' in row and pd.notna(row['Rec']):
                                score += row['Rec'] * 0.6
                            if 'Yds' in row and pd.notna(row['Yds']):
                                score += row['Yds'] / 18
                            if 'TD' in row and pd.notna(row['TD']):
                                score += row['TD'] * 5
                        
                        oroy_candidates.append({
                            'Player': row['Player'],
                            'Position': pos_type,
                            'Team': row.get('Team', row.get('Tm', 'N/A')),
                            'Primary_Stat': f"{row.get('Yds', 0)} {df_name.title()} Yds",
                            'OROY_Score': score
                        })
        
        if oroy_candidates:
            oroy_df = pd.DataFrame(oroy_candidates)
            oroy_df = oroy_df.sort_values('OROY_Score', ascending=False)
            
            print(f"✓ Generated OROY predictions for {len(oroy_df)} candidates")
            if not oroy_df.empty:
                print(f"  Top candidate: {oroy_df.iloc[0]['Player']} ({oroy_df.iloc[0]['Position']}) - {oroy_df.iloc[0]['OROY_Score']} points")
            
            return oroy_df.head(15)
        
        return pd.DataFrame()
    
    def calculate_droy_scores(self):
        """Calculate Enhanced DROY scores - Updated for Jared Verse model"""
        print("Calculating DROY predictions with enhanced pass rush model...")
        
        # Fetch defensive stats
        defense_df = self.fetch_player_data('defense')
        if defense_df.empty:
            print("No defensive data available for DROY calculation")
            return pd.DataFrame()
        
        # Convert relevant columns to numeric
        numeric_cols = ['Tkl', 'Sk', 'Int', 'PD', 'FF', 'Age', 'Comb', 'Solo', 'TFL', 'QBHits']
        for col in numeric_cols:
            if col in defense_df.columns:
                defense_df[col] = pd.to_numeric(defense_df[col], errors='coerce')
        
        droy_candidates = []
        
        for idx, row in defense_df.iterrows():
            # Check if likely rookie (Jared Verse model - age <= 23 or has DRoY award)
            is_rookie = False
            if 'Age' in row and pd.notna(row['Age']) and row['Age'] <= 23:
                is_rookie = True
            if 'Awards' in row and pd.notna(row['Awards']) and 'DRoY' in str(row['Awards']):
                is_rookie = True
            
            if not is_rookie:
                continue
                
            score = 0
            position = row.get('Pos', '')
            
            # 1. PASS RUSH PRODUCTION (50% weight) - Key for Jared Verse win
            sacks = row.get('Sk', 0) if pd.notna(row.get('Sk', 0)) else 0
            qb_hits = row.get('QBHits', 0) if pd.notna(row.get('QBHits', 0)) else 0
            tfl = row.get('TFL', 0) if pd.notna(row.get('TFL', 0)) else 0
            
            # Edge rusher positions get priority (where Jared Verse played)
            if any(pos in position for pos in ['EDGE', 'OLB', 'DE', 'LB']):
                position_bonus = 10  # Favor edge rushers
            else:
                position_bonus = 0
            
            # Sack production (most important)
            if sacks >= 10:  # Elite rookie pass rusher
                score += 35
            elif sacks >= 8:  # Very good
                score += 30
            elif sacks >= 6:  # Good
                score += 25
            elif sacks >= 4:  # Decent
                score += 20
            elif sacks >= 2:  # Some production
                score += 15
            
            # QB Hits and TFL (pressure stats)
            if qb_hits >= 15:
                score += 10
            elif qb_hits >= 10:
                score += 8
            elif qb_hits >= 5:
                score += 5
            
            if tfl >= 10:
                score += 5
            elif tfl >= 5:
                score += 3
            
            # 2. OVERALL TACKLE PRODUCTION (25% weight)
            tackles = row.get('Tkl', 0) if pd.notna(row.get('Tkl', 0)) else 0
            combined = row.get('Comb', 0) if pd.notna(row.get('Comb', 0)) else 0
            
            # Use combined tackles if available, otherwise regular tackles
            total_tackles = combined if combined > 0 else tackles
            
            if total_tackles >= 80:
                score += 15
            elif total_tackles >= 60:
                score += 12
            elif total_tackles >= 40:
                score += 10
            elif total_tackles >= 20:
                score += 8
            
            # 3. PLAYMAKING (15% weight)
            interceptions = row.get('Int', 0) if pd.notna(row.get('Int', 0)) else 0
            pds = row.get('PD', 0) if pd.notna(row.get('PD', 0)) else 0
            forced_fumbles = row.get('FF', 0) if pd.notna(row.get('FF', 0)) else 0
            
            if interceptions >= 3:
                score += 8
            elif interceptions >= 1:
                score += 5
            
            if pds >= 10:
                score += 5
            elif pds >= 5:
                score += 3
            
            if forced_fumbles >= 2:
                score += 4
            elif forced_fumbles >= 1:
                score += 2
            
            # 4. POSITION BONUS (10% weight)
            score += position_bonus
            
            if score > 0:
                candidate = {
                    'Player': row['Player'],
                    'DROY_Score': score,
                    'Position': position,
                    'Team': row.get('Team', row.get('Tm', 'N/A')),
                    'Sk': sacks,
                    'Int': interceptions,
                    'PD': pds,
                    'FF': forced_fumbles,
                    'Tkl': total_tackles,
                    'QBHits': qb_hits,
                    'TFL': tfl
                }
                droy_candidates.append(candidate)
        
        if droy_candidates:
            droy_df = pd.DataFrame(droy_candidates)
            droy_df = droy_df.sort_values('DROY_Score', ascending=False)
            
            print(f"✓ Generated DROY predictions for {len(droy_df)} rookie candidates")
            if not droy_df.empty:
                print(f"  Top candidate: {droy_df.iloc[0]['Player']} ({droy_df.iloc[0]['Position']}) - {droy_df.iloc[0]['DROY_Score']} points")
            
            return droy_df.head(15)
        
        print("No rookie defensive candidates found")
        return pd.DataFrame()
    
    def create_awards_charts(self, mvp_df, oroy_df, droy_df):
        """Create visualization charts for award predictions"""
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(20, 15))
        gs = fig.add_gridspec(3, 2, hspace=0.4, wspace=0.3)
        
        try:
            # MVP Chart
            ax1 = fig.add_subplot(gs[0, :])
            if not mvp_df.empty:
                top_mvp = mvp_df.head(10)
                colors = plt.cm.Blues(range(len(top_mvp)))
                bars = ax1.bar(range(len(top_mvp)), top_mvp['MVP_Score'], color=colors)
                ax1.set_title('🏆 MVP Predictions - Dual-Threat QB Model v2.0', fontsize=16, color='white', pad=20)
                ax1.set_xticks(range(len(top_mvp)))
                ax1.set_xticklabels([f"{row['Player']}\n{row.get('Tm', 'N/A')}" for _, row in top_mvp.iterrows()], 
                                  rotation=45, ha='right', fontsize=10)
                ax1.set_ylabel('MVP Score', fontsize=12)
                
                # Add score labels on bars
                for i, bar in enumerate(bars):
                    height = bar.get_height()
                    ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                           f'{int(height)}', ha='center', va='bottom', fontsize=9)
            
            # OROY Chart
            ax2 = fig.add_subplot(gs[1, 0])
            if not oroy_df.empty:
                top_oroy = oroy_df.head(8)
                colors = plt.cm.Greens(range(len(top_oroy)))
                bars = ax2.bar(range(len(top_oroy)), top_oroy['OROY_Score'], color=colors)
                ax2.set_title('🌟 OROY Predictions - Mobile QB Model', fontsize=14, color='white', pad=15)
                ax2.set_xticks(range(len(top_oroy)))
                ax2.set_xticklabels([f"{row['Player']}\n{row.get('Position', 'N/A')}" for _, row in top_oroy.iterrows()], 
                                  rotation=45, ha='right', fontsize=9)
                ax2.set_ylabel('OROY Score', fontsize=10)
                
                # Add score labels
                for i, bar in enumerate(bars):
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                           f'{int(height)}', ha='center', va='bottom', fontsize=8)
            
            # DROY Chart
            ax3 = fig.add_subplot(gs[1, 1])
            if not droy_df.empty:
                top_droy = droy_df.head(8)
                colors = plt.cm.Reds(range(len(top_droy)))
                bars = ax3.bar(range(len(top_droy)), top_droy['DROY_Score'], color=colors)
                ax3.set_title('🛡️ DROY Predictions - Pass Rush Model', fontsize=14, color='white', pad=15)
                ax3.set_xticks(range(len(top_droy)))
                ax3.set_xticklabels([f"{row['Player']}\n{row.get('Position', 'N/A')}" for _, row in top_droy.iterrows()], 
                                  rotation=45, ha='right', fontsize=9)
                ax3.set_ylabel('DROY Score', fontsize=10)
                
                # Add score labels
                for i, bar in enumerate(bars):
                    height = bar.get_height()
                    ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                           f'{int(height)}', ha='center', va='bottom', fontsize=8)
            
            # Model explanation
            ax4 = fig.add_subplot(gs[2, :])
            ax4.text(0.1, 0.8, "📊 ENHANCED 2024 AWARD MODELS", fontsize=16, weight='bold', color='cyan')
            ax4.text(0.1, 0.6, "🏆 MVP: Dual-Threat QB Model - Total TDs (35%), Team Success (25%), Efficiency (20%), Turnovers (10%), Dual-Threat (10%)", 
                    fontsize=12, color='lightblue')
            ax4.text(0.1, 0.4, "🌟 OROY: Mobile Rookie Model - Dual-Threat (40%), Team Success (25%), Efficiency (20%), Volume (15%)", 
                    fontsize=12, color='lightgreen')
            ax4.text(0.1, 0.2, "🛡️ DROY: Pass Rush Model - Pass Rush (50%), Tackles (25%), Playmaking (15%), Position (10%)", 
                    fontsize=12, color='lightcoral')
            ax4.set_xlim(0, 1)
            ax4.set_ylim(0, 1)
            ax4.axis('off')
            
            plt.suptitle(f'NFL Awards Predictions - {self.current_season} Season (Enhanced Models)', 
                        fontsize=18, color='white', y=0.98)
            
            chart_path = self.docs_dir / "awards_predictions.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='black')
            plt.close()
            
            print(f"✓ Awards prediction charts saved to {chart_path}")
            
        except Exception as e:
            print(f"Error creating awards charts: {e}")
            plt.close()
    
    def save_awards_data(self, mvp_df, oroy_df, droy_df):
        """Save awards prediction data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save individual award predictions
        if not mvp_df.empty:
            mvp_file = self.docs_dir / "mvp_predictions.csv"
            mvp_df.to_csv(mvp_file, index=False)
            archive_file = self.archive_dir / f"mvp_predictions_{timestamp}.csv"
            mvp_df.to_csv(archive_file, index=False)
        
        if not oroy_df.empty:
            oroy_file = self.docs_dir / "oroy_predictions.csv"
            oroy_df.to_csv(oroy_file, index=False)
            archive_file = self.archive_dir / f"oroy_predictions_{timestamp}.csv"
            oroy_df.to_csv(archive_file, index=False)
        
        if not droy_df.empty:
            droy_file = self.docs_dir / "droy_predictions.csv"
            droy_df.to_csv(droy_file, index=False)
            archive_file = self.archive_dir / f"droy_predictions_{timestamp}.csv"
            droy_df.to_csv(archive_file, index=False)
        
        # Update timestamp
        timestamp_file = self.docs_dir / "last_updated_awards.txt"
        with open(timestamp_file, 'w') as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def process_all_awards(self):
        """Process all award predictions"""
        print("=" * 60)
        print("🏆 NFL AWARDS PREDICTION PROCESSOR (ENHANCED)")
        print("=" * 60)
        print(f"Processing {self.current_season} NFL season awards...")
        print("Updated models based on 2024 actual winners:")
        print("  MVP: Josh Allen (dual-threat QB)")
        print("  OROY: Jayden Daniels (dual-threat rookie QB)")
        print("  DROY: Jared Verse (rookie edge rusher)")
        
        # Calculate award predictions
        mvp_df = self.calculate_mvp_scores()
        oroy_df = self.calculate_oroy_scores()
        droy_df = self.calculate_droy_scores()
        
        # Create charts
        print("\nCreating awards prediction charts...")
        self.create_awards_charts(mvp_df, oroy_df, droy_df)
        
        # Save data
        print("Saving awards prediction data...")
        self.save_awards_data(mvp_df, oroy_df, droy_df)
        
        print("\n" + "=" * 60)
        print("🏆 AWARDS PREDICTION PROCESSING COMPLETE!")
        print("=" * 60)
        
        # Print summary
        if not mvp_df.empty:
            print(f"🏆 TOP MVP CANDIDATES:")
            for i, (_, row) in enumerate(mvp_df.head(3).iterrows()):
                total_tds = row.get('TD', 0) + row.get('Rush_TD', 0)
                print(f"  {i+1}. {row['Player']} ({row.get('Tm', 'N/A')}) - {row['MVP_Score']} pts ({total_tds} total TDs)")
        
        if not oroy_df.empty:
            print(f"🌟 TOP OROY CANDIDATES:")
            for i, (_, row) in enumerate(oroy_df.head(3).iterrows()):
                print(f"  {i+1}. {row['Player']} ({row['Position']}) - {row['OROY_Score']} pts")
        
        if not droy_df.empty:
            print(f"🛡️ TOP DROY CANDIDATES:")
            for i, (_, row) in enumerate(droy_df.head(3).iterrows()):
                print(f"  {i+1}. {row['Player']} ({row['Position']}) - {row['DROY_Score']} pts ({row['Sk']} sacks)")
        
        print("=" * 60)

if __name__ == "__main__":
    # Ensure directories exist
    predictor = NFLAwardsPredictor()
    
    predictor.docs_dir.mkdir(parents=True, exist_ok=True)
    predictor.archive_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Created directories:")
    print(f"  Docs: {predictor.docs_dir}")
    print(f"  Archive: {predictor.archive_dir}")
    
    predictor.process_all_awards()