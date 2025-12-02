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

# COMPREHENSIVE warning suppression
import warnings
warnings.filterwarnings("ignore")

# Safe matplotlib configuration
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
    
    def create_simple_chart(self, mvp_df):
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
    
    def save_awards_data(self, mvp_df):
        """Save awards data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if not mvp_df.empty:
            mvp_file = self.docs_dir / "mvp_predictions.csv"
            mvp_df.to_csv(mvp_file, index=False)
            
            archive_file = self.archive_dir / f"mvp_predictions_{timestamp}.csv"
            mvp_df.to_csv(archive_file, index=False)
        
        # Update timestamp
        timestamp_file = self.docs_dir / "last_updated_awards.txt"
        with open(timestamp_file, 'w') as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def process_awards(self):
        """Main processing function"""
        print("NFL AWARDS PREDICTION PROCESSOR")
        print("=" * 50)
        print("Processing {} NFL season awards...".format(self.current_season))
        
        # Calculate MVP
        mvp_df = self.calculate_mvp_scores()
        
        # Create chart
        print("\nCreating awards chart...")
        self.create_simple_chart(mvp_df)
        
        # Save data
        print("Saving awards data...")
        self.save_awards_data(mvp_df)
        
        print("\n" + "=" * 50)
        print("AWARDS PROCESSING COMPLETE!")
        print("=" * 50)
        
        if not mvp_df.empty:
            top_mvp = mvp_df.iloc[0]
            print("Top MVP candidate: {} with {:.1f} points".format(
                top_mvp['Player'], top_mvp['MVP_Score']))

if __name__ == "__main__":
    predictor = NFLAwardsPredictor()
    
    predictor.docs_dir.mkdir(parents=True, exist_ok=True)
    predictor.archive_dir.mkdir(parents=True, exist_ok=True)
    
    predictor.process_awards()