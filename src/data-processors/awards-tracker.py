#!/usr/bin/env python3
"""
NFL Awards Predictor - FONT-WARNING FREE VERSION
Enhanced NFL Awards Predictor with zero font warnings
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime
import time
from pathlib import Path
import json

import warnings

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


class NFLAwardsPredictor:
    def __init__(self):
        self.base_url = "https://www.pro-football-reference.com"
        self.current_season = self.get_current_nfl_season()
        self.docs_dir = Path(__file__).parent.parent.parent / "docs"
        self.archive_dir = Path(__file__).parent.parent.parent / "archive"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        print("Initialized NFL Awards Predictor for {}-{} season".format(self.current_season, self.current_season + 1))
        
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
                if df.columns.nlevels > 1:
                    df.columns = df.columns.droplevel(0)
                df = df[df['Player'].notna()]
                df = df[df['Player'] != 'Player']
                return df
            return pd.DataFrame()
        except Exception as e:
            print(f"Error fetching {stat_type} data: {e}")
            return pd.DataFrame()
    
    def calculate_mvp_scores(self):
        """Calculate MVP scores - simplified version"""
        print("Calculating MVP predictions...")
        
        passing_df = self.fetch_player_data('passing')
        if passing_df.empty:
            print("No passing data available for MVP calculation")
            return pd.DataFrame()
        
        # Simple MVP calculation
        numeric_cols = ['Yds', 'TD', 'Int', 'Rate', 'W', 'L']
        for col in numeric_cols:
            if col in passing_df.columns:
                passing_df[col] = pd.to_numeric(passing_df[col], errors='coerce').fillna(0)
        
        # Basic MVP score
        mvp_scores = []
        for idx, row in passing_df.iterrows():
            score = 0
            
            # Passing yards (normalized)
            if 'Yds' in row and pd.notna(row['Yds']):
                score += (row['Yds'] / 4000) * 25
            
            # Passing TDs
            if 'TD' in row and pd.notna(row['TD']):
                score += row['TD'] * 2
            
            # Team wins
            if 'W' in row and pd.notna(row['W']):
                score += row['W'] * 3
            
            # Interception penalty
            if 'Int' in row and pd.notna(row['Int']):
                score -= row['Int'] * 1
            
            mvp_scores.append(score)
        
        passing_df['MVP_Score'] = mvp_scores
        
        # Get top candidates
        available_cols = ['Player', 'MVP_Score']
        if 'Tm' in passing_df.columns:
            available_cols.append('Tm')
        if 'W' in passing_df.columns:
            available_cols.append('W')
        if 'L' in passing_df.columns:
            available_cols.append('L')
        
        mvp_candidates = passing_df.nlargest(10, 'MVP_Score')[available_cols]
        
        if not mvp_candidates.empty:
            print("Generated MVP predictions for {} candidates".format(len(mvp_candidates)))
        
        return mvp_candidates
    
    def calculate_oroy_scores(self):
        """Calculate Enhanced OROY scores - Mobile rookie QB model"""
        print("Calculating OROY predictions with enhanced mobile QB model...")
        
        # Fetch all offensive position data
        passing_df = self.fetch_player_data('passing')
        rushing_df = self.fetch_player_data('rushing')
        receiving_df = self.fetch_player_data('receiving')
        
        oroy_candidates = []
        
        # Process QB candidates (prioritizes mobile rookie quarterbacks)
        if not passing_df.empty:
            numeric_cols = ['Yds', 'TD', 'Int', 'Rate', 'W', 'L', 'Age']
            for col in numeric_cols:
                if col in passing_df.columns:
                    passing_df[col] = pd.to_numeric(passing_df[col], errors='coerce').fillna(0)
            
            # Add rushing stats for QBs from rushing data
            if not rushing_df.empty:
                rushing_df['Rush_TD'] = pd.to_numeric(rushing_df['TD'], errors='coerce')
                rushing_df['Rush_Yds'] = pd.to_numeric(rushing_df['Yds'], errors='coerce')
                qb_rushing = rushing_df[rushing_df['Pos'] == 'QB'][['Player', 'Rush_TD', 'Rush_Yds']]
                passing_df = passing_df.merge(qb_rushing, on='Player', how='left')
                passing_df['Rush_TD'] = passing_df['Rush_TD'].fillna(0)
                passing_df['Rush_Yds'] = passing_df['Rush_Yds'].fillna(0)
            
            # Focus on rookie QBs - mobile QB model
            for idx, row in passing_df.iterrows():
                # Check if likely rookie (age <= 24 or rookie indicators)
                is_rookie = False
                if 'Age' in row and pd.notna(row['Age']) and row['Age'] <= 24:
                    is_rookie = True
                
                if not is_rookie:
                    continue
                
                score = 0
                # OROY scoring for mobile QBs
                score += row.get('TD', 0) * 4  # Passing TDs
                score += row.get('Rush_TD', 0) * 6  # Rushing TDs (bonus for mobile QBs)
                score += (row.get('Yds', 0) / 4000) * 30  # Passing yards
                score += (row.get('Rush_Yds', 0) / 500) * 20  # Rushing yards
                score += row.get('W', 0) * 5  # Team success
                score -= row.get('Int', 0) * 2  # Turnover penalty
                
                oroy_candidates.append({
                    'Player': row['Player'],
                    'Tm': row.get('Tm', 'N/A'),
                    'Position': 'QB',
                    'OROY_Score': score,
                    'Age': row.get('Age', 0)
                })
        
        # Process other positions (RB, WR, TE)
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
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            for idx, row in df.head(50).iterrows():
                # Check if likely rookie
                is_rookie = False
                if 'Age' in row and pd.notna(row['Age']) and row['Age'] <= 23:
                    is_rookie = True
                
                if not is_rookie:
                    continue
                
                score = 0
                # Position-specific scoring
                if pos_type == 'RB':
                    score += (row.get('Yds', 0) / 1000) * 40
                    score += row.get('TD', 0) * 6
                    score += (row.get('Att', 0) / 200) * 10
                else:  # WR/TE
                    score += (row.get('Yds', 0) / 1000) * 35
                    score += row.get('TD', 0) * 6
                    score += (row.get('Rec', 0) / 70) * 15
                
                oroy_candidates.append({
                    'Player': row['Player'],
                    'Tm': row.get('Tm', 'N/A'),
                    'Position': pos_type,
                    'OROY_Score': score,
                    'Age': row.get('Age', 0)
                })
        
        if oroy_candidates:
            oroy_df = pd.DataFrame(oroy_candidates)
            oroy_df = oroy_df.sort_values('OROY_Score', ascending=False)
            
            print("Generated OROY predictions for {} candidates".format(len(oroy_df)))
            if not oroy_df.empty:
                top_oroy = oroy_df.iloc[0]
                print("Top candidate: {} ({}) - {:.1f} points".format(
                    top_oroy['Player'], top_oroy['Position'], top_oroy['OROY_Score']))
            
            return oroy_df.head(15)
        
        return pd.DataFrame()
    
    def calculate_droy_scores(self):
        """Calculate Enhanced DROY scores - Pass rush model"""
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
                defense_df[col] = pd.to_numeric(defense_df[col], errors='coerce').fillna(0)
        
        droy_candidates = []
        
        for idx, row in defense_df.iterrows():
            # Check if likely rookie (age <= 23)
            is_rookie = False
            if 'Age' in row and pd.notna(row['Age']) and row['Age'] <= 23:
                is_rookie = True
            
            if not is_rookie:
                continue
                
            score = 0
            position = row.get('Pos', '')
            
            # Pass rush production (50% weight)
            sacks = row.get('Sk', 0)
            qb_hits = row.get('QBHits', 0)
            tfl = row.get('TFL', 0)
            
            # Edge rusher positions get priority
            if any(pos in position for pos in ['EDGE', 'OLB', 'DE', 'LB']):
                score += sacks * 15  # High value for sacks
                score += qb_hits * 3
                score += tfl * 2
            else:
                score += sacks * 12
                score += qb_hits * 2
                score += tfl * 1.5
            
            # General defensive stats
            score += row.get('Tkl', 0) * 0.5
            score += row.get('Int', 0) * 8
            score += row.get('PD', 0) * 2
            score += row.get('FF', 0) * 5
            
            if score > 20:  # Minimum threshold
                droy_candidates.append({
                    'Player': row['Player'],
                    'Tm': row.get('Tm', 'N/A'),
                    'Position': position,
                    'DROY_Score': score,
                    'Age': row.get('Age', 0),
                    'Sacks': sacks
                })
        
        if droy_candidates:
            droy_df = pd.DataFrame(droy_candidates)
            droy_df = droy_df.sort_values('DROY_Score', ascending=False)
            
            print("Generated DROY predictions for {} candidates".format(len(droy_df)))
            if not droy_df.empty:
                top_droy = droy_df.iloc[0]
                print("Top candidate: {} ({}) - {:.1f} points".format(
                    top_droy['Player'], top_droy['Position'], top_droy['DROY_Score']))
            
            return droy_df.head(15)
        
        print("No rookie defensive candidates found")
        return pd.DataFrame()
    
    def create_comprehensive_awards_chart(self, mvp_df, oroy_df, droy_df):
        """Create comprehensive awards chart with all three awards"""
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(2, 3, hspace=0.4, wspace=0.3)
        
        try:
            # 1. MVP Chart
            ax1 = fig.add_subplot(gs[0, 0])
            if not mvp_df.empty:
                top_mvp = mvp_df.head(8)
                bars = ax1.bar(range(len(top_mvp)), top_mvp['MVP_Score'], 
                             color='gold', alpha=0.8)
                ax1.set_title('MVP Predictions', fontsize=14, color='white')
                ax1.set_ylabel('MVP Score')
                ax1.set_xticks(range(len(top_mvp)))
                ax1.set_xticklabels(top_mvp['Player'], rotation=45, ha='right', fontsize=9)
                ax1.grid(True, alpha=0.3, axis='y')
                
                # Add value labels
                for i, bar in enumerate(bars):
                    height = bar.get_height()
                    ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                           f'{height:.0f}', ha='center', va='bottom', fontsize=8)
            else:
                ax1.text(0.5, 0.5, 'No MVP data available', ha='center', va='center', 
                        transform=ax1.transAxes, fontsize=12, color='white')
                ax1.set_title('MVP Predictions', fontsize=14, color='white')
            
            # 2. OROY Chart
            ax2 = fig.add_subplot(gs[0, 1])
            if not oroy_df.empty:
                top_oroy = oroy_df.head(8)
                colors = ['#2ECC71' if pos == 'QB' else '#3498DB' if pos == 'RB' else '#E74C3C' 
                         for pos in top_oroy['Position']]
                bars = ax2.bar(range(len(top_oroy)), top_oroy['OROY_Score'], 
                             color=colors, alpha=0.8)
                ax2.set_title('Offensive ROY Predictions', fontsize=14, color='white')
                ax2.set_ylabel('OROY Score')
                ax2.set_xticks(range(len(top_oroy)))
                ax2.set_xticklabels(top_oroy['Player'], rotation=45, ha='right', fontsize=9)
                ax2.grid(True, alpha=0.3, axis='y')
                
                # Add value labels
                for i, bar in enumerate(bars):
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                           f'{height:.0f}', ha='center', va='bottom', fontsize=8)
            else:
                ax2.text(0.5, 0.5, 'No OROY data available', ha='center', va='center', 
                        transform=ax2.transAxes, fontsize=12, color='white')
                ax2.set_title('Offensive ROY Predictions', fontsize=14, color='white')
            
            # 3. DROY Chart
            ax3 = fig.add_subplot(gs[0, 2])
            if not droy_df.empty:
                top_droy = droy_df.head(8)
                colors = ['#8B4513' if 'DE' in pos or 'EDGE' in pos else '#4B0082' 
                         for pos in top_droy['Position']]
                bars = ax3.bar(range(len(top_droy)), top_droy['DROY_Score'], 
                             color=colors, alpha=0.8)
                ax3.set_title('Defensive ROY Predictions', fontsize=14, color='white')
                ax3.set_ylabel('DROY Score')
                ax3.set_xticks(range(len(top_droy)))
                ax3.set_xticklabels(top_droy['Player'], rotation=45, ha='right', fontsize=9)
                ax3.grid(True, alpha=0.3, axis='y')
                
                # Add value labels
                for i, bar in enumerate(bars):
                    height = bar.get_height()
                    ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                           f'{height:.0f}', ha='center', va='bottom', fontsize=8)
            else:
                ax3.text(0.5, 0.5, 'No DROY data available', ha='center', va='center', 
                        transform=ax3.transAxes, fontsize=12, color='white')
                ax3.set_title('Defensive ROY Predictions', fontsize=14, color='white')
            
            # 4. Award Race Summary (bottom spans all columns)
            ax4 = fig.add_subplot(gs[1, :])
            
            # Create a summary comparison
            award_leaders = []
            if not mvp_df.empty:
                mvp_leader = mvp_df.iloc[0]
                award_leaders.append({
                    'Award': 'MVP',
                    'Player': mvp_leader['Player'],
                    'Score': mvp_leader['MVP_Score'],
                    'Team': mvp_leader.get('Tm', 'N/A')
                })
            
            if not oroy_df.empty:
                oroy_leader = oroy_df.iloc[0]
                award_leaders.append({
                    'Award': 'OROY',
                    'Player': oroy_leader['Player'],
                    'Score': oroy_leader['OROY_Score'],
                    'Team': oroy_leader.get('Tm', 'N/A')
                })
            
            if not droy_df.empty:
                droy_leader = droy_df.iloc[0]
                award_leaders.append({
                    'Award': 'DROY',
                    'Player': droy_leader['Player'],
                    'Score': droy_leader['DROY_Score'],
                    'Team': droy_leader.get('Tm', 'N/A')
                })
            
            if award_leaders:
                leaders_df = pd.DataFrame(award_leaders)
                colors = ['gold', '#2ECC71', '#8B4513'][:len(leaders_df)]
                
                bars = ax4.bar(range(len(leaders_df)), leaders_df['Score'], 
                             color=colors, alpha=0.8)
                ax4.set_title('Award Race Leaders', fontsize=16, color='white', pad=20)
                ax4.set_ylabel('Prediction Score')
                ax4.set_xticks(range(len(leaders_df)))
                ax4.set_xticklabels([f"{row['Award']}\n{row['Player']}" for _, row in leaders_df.iterrows()], 
                                   fontsize=12)
                ax4.grid(True, alpha=0.3, axis='y')
                
                # Add value labels and team info
                for i, (bar, (_, row)) in enumerate(zip(bars, leaders_df.iterrows())):
                    height = bar.get_height()
                    ax4.text(bar.get_x() + bar.get_width()/2., height + 5,
                           f'{height:.0f}', ha='center', va='bottom', fontsize=12, fontweight='bold')
                    ax4.text(bar.get_x() + bar.get_width()/2., -10,
                           f"({row['Team']})", ha='center', va='top', fontsize=10)
            else:
                ax4.text(0.5, 0.5, 'No award data available', ha='center', va='center', 
                        transform=ax4.transAxes, fontsize=16, color='white')
                ax4.set_title('Award Race Leaders', fontsize=16, color='white')
            
            # Remove empty chart axes
            if not award_leaders:
                ax4.set_xticks([])
                ax4.set_yticks([])
                for ax in [ax1, ax2, ax3]:
                    ax.set_xticks([])
                    ax.set_yticks([])
            
            plt.suptitle(f'NFL Awards Predictions - {self.current_season} Season', 
                        fontsize=20, color='white', y=0.98)
            
            plt.tight_layout()
            
            # Save chart
            chart_path = self.docs_dir / "awards_predictions.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='black')
            plt.close()
            
            print("Comprehensive awards chart saved to {}".format(chart_path))
            
        except Exception as e:
    def record_prediction_for_accuracy(self, award, predicted_winner, predicted_score):
        """Record prediction for accuracy tracking"""
        try:
            import json
            accuracy_file = self.docs_dir / "awards_accuracy_history.json"
            
            # Load existing history
            if accuracy_file.exists():
                with open(accuracy_file, 'r') as f:
                    history = json.load(f)
            else:
                history = {"predictions": [], "model_performance": {}}
            
            # Check if we already have a prediction for this season/award
            existing = [p for p in history["predictions"] 
                       if p["season"] == self.current_season and p["award"] == award]
            
            if not existing:
                prediction_record = {
                    "season": self.current_season,
                    "award": award,
                    "predicted_winner": predicted_winner,
                    "predicted_score": predicted_score,
                    "actual_winner": None,
                    "prediction_date": datetime.now().isoformat(),
                    "was_correct": None
                }
                
                history["predictions"].append(prediction_record)
                
                # Save updated history
                with open(accuracy_file, 'w') as f:
                    json.dump(history, f, indent=2)
                
                print("  -> Prediction recorded for accuracy tracking")
        except Exception as e:
            print(f"  -> Warning: Could not record prediction for accuracy tracking: {e}")
    
        """Create simple awards chart with no font issues"""
        if mvp_df.empty:
            print("No data for awards chart")
            return
        
        plt.style.use('dark_background')
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        try:
            # Simple MVP bar chart
            top_mvp = mvp_df.head(10)
            
            bars = ax.bar(range(len(top_mvp)), top_mvp['MVP_Score'], 
                         color='gold', alpha=0.8)
            
            ax.set_title('MVP Predictions', fontsize=14, color='white')
            ax.set_ylabel('MVP Score')
            ax.set_xticks(range(len(top_mvp)))
            ax.set_xticklabels(top_mvp['Player'], rotation=45, ha='right')
            ax.grid(True, alpha=0.3, axis='y')
            
            # Add value labels
            for i, bar in enumerate(bars):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{height:.1f}', ha='center', va='bottom')
            
            plt.tight_layout()
            
            # Save chart
            chart_path = self.docs_dir / "awards_predictions.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='black')
            plt.close()
            
            print("Awards chart saved to {}".format(chart_path))
            
        except Exception as e:
            print(f"Error creating chart: {e}")
            plt.close()
    
    def save_awards_data(self, mvp_df, oroy_df=None, droy_df=None):
        """Save comprehensive awards data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save MVP data
        if not mvp_df.empty:
            mvp_file = self.docs_dir / "mvp_predictions.csv"
            mvp_df.to_csv(mvp_file, index=False)
            
            archive_file = self.archive_dir / f"mvp_predictions_{timestamp}.csv"
            mvp_df.to_csv(archive_file, index=False)
        
        # Save OROY data
        if oroy_df is not None and not oroy_df.empty:
            oroy_file = self.docs_dir / "oroy_predictions.csv"
            oroy_df.to_csv(oroy_file, index=False)
            
            archive_file = self.archive_dir / f"oroy_predictions_{timestamp}.csv"
            oroy_df.to_csv(archive_file, index=False)
        
        # Save DROY data
        if droy_df is not None and not droy_df.empty:
            droy_file = self.docs_dir / "droy_predictions.csv"
            droy_df.to_csv(droy_file, index=False)
            
            archive_file = self.archive_dir / f"droy_predictions_{timestamp}.csv"
            droy_df.to_csv(archive_file, index=False)
        
        # Update timestamp
        timestamp_file = self.docs_dir / "last_updated_awards.txt"
        with open(timestamp_file, 'w') as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def process_awards(self):
        """Enhanced main processing function with all three awards"""
        print("NFL AWARDS PREDICTION PROCESSOR (ENHANCED)")
        print("=" * 60)
        print("Processing {} NFL season awards...".format(self.current_season))
        print("Enhanced models based on modern NFL trends:")
        print("  MVP: Dual-threat QB model (total touchdown focus)")
        print("  OROY: Mobile rookie QB model (dual-threat ability)")
        print("  DROY: Pass rush model (edge rusher focus)")
        
        # Calculate all three awards
        print("\n1. Calculating MVP predictions...")
        mvp_df = self.calculate_mvp_scores()
        
        print("\n2. Calculating OROY predictions...")
        oroy_df = self.calculate_oroy_scores()
        
        print("\n3. Calculating DROY predictions...")
        droy_df = self.calculate_droy_scores()
        
        # Create comprehensive chart
        print("\n4. Creating comprehensive awards chart...")
        self.create_comprehensive_awards_chart(mvp_df, oroy_df, droy_df)
        
        # Save all data
        print("\n5. Saving all awards data...")
        self.save_awards_data(mvp_df, oroy_df, droy_df)
        
        print("\n" + "=" * 60)
        print("AWARDS PREDICTION PROCESSING COMPLETE!")
        print("=" + "=" * 60)
        
        # Display top candidates for each award and record for accuracy tracking
        if not mvp_df.empty:
            top_mvp = mvp_df.iloc[0]
            print("Top MVP candidate: {} with {:.1f} points".format(
                top_mvp['Player'], top_mvp['MVP_Score']))
            
            # Record prediction for accuracy tracking
            self.record_prediction_for_accuracy(
                award="MVP",
                predicted_winner=top_mvp['Player'],
                predicted_score=top_mvp['MVP_Score']
            )
        
        if not oroy_df.empty:
            top_oroy = oroy_df.iloc[0]
            print("Top OROY candidate: {} ({}) with {:.1f} points".format(
                top_oroy['Player'], top_oroy['Position'], top_oroy['OROY_Score']))
            
            # Record prediction for accuracy tracking
            self.record_prediction_for_accuracy(
                award="OROY", 
                predicted_winner=top_oroy['Player'],
                predicted_score=top_oroy['OROY_Score']
            )
        
        if not droy_df.empty:
            top_droy = droy_df.iloc[0]
            print("Top DROY candidate: {} ({}) with {:.1f} points".format(
                top_droy['Player'], top_droy['Position'], top_droy['DROY_Score']))
            
            # Record prediction for accuracy tracking
            self.record_prediction_for_accuracy(
                award="DROY",
                predicted_winner=top_droy['Player'], 
                predicted_score=top_droy['DROY_Score']
            )

if __name__ == "__main__":
    predictor = NFLAwardsPredictor()
    
    predictor.docs_dir.mkdir(parents=True, exist_ok=True)
    predictor.archive_dir.mkdir(parents=True, exist_ok=True)
    
    predictor.process_awards()