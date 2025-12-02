#!/usr/bin/env python3
"""
NFL Awards Predictor - CORRECTED VERSION
Enhanced NFL Awards Predictor with proper syntax
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

class NFLAwardsPredictor:
    def __init__(self):
        self.base_url = "https://www.pro-football-reference.com"
        self.current_season = self.get_current_nfl_season()
        self.docs_dir = Path(__file__).parent.parent.parent / "docs"
        self.archive_dir = Path(__file__).parent.parent.parent / "archive"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        print(f"🏈 NFL Awards Predictor - {self.current_season} Season")
        
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
            print(f"❌ Error fetching {stat_type} data: {e}")
            return pd.DataFrame()
    
    def calculate_mvp_scores(self):
        """Calculate MVP scores with enhanced model"""
        print("📊 Calculating MVP predictions...")
        
        passing_df = self.fetch_player_data('passing')
        if passing_df.empty:
            print("❌ No passing data available for MVP calculation")
            return pd.DataFrame()
        
        # Enhanced MVP calculation based on 2024 analysis
        numeric_cols = ['Yds', 'TD', 'Int', 'Rate', 'W', 'L']
        for col in numeric_cols:
            if col in passing_df.columns:
                passing_df[col] = pd.to_numeric(passing_df[col], errors='coerce').fillna(0)
        
        mvp_scores = []
        for idx, row in passing_df.iterrows():
            score = 0
            
            # Team Success (25% weight) - most important
            if 'W' in row and pd.notna(row['W']):
                score += row['W'] * 4.0  # 25% weight
            
            # Total TDs (30% weight) - includes passing + estimated rushing TDs
            if 'TD' in row and pd.notna(row['TD']):
                total_tds = row['TD']
                # Estimate rushing TDs for mobile QBs (simple heuristic)
                if row['TD'] > 20:  # High volume passer likely has rushing TDs
                    total_tds += 5  # Estimate
                score += total_tds * 2.4  # 30% weight
            
            # QB Efficiency (20% weight)
            if 'Rate' in row and pd.notna(row['Rate']):
                score += (row['Rate'] / 100) * 16  # 20% weight
            
            # Passing Yards (15% weight) - reduced from before
            if 'Yds' in row and pd.notna(row['Yds']):
                score += (row['Yds'] / 4000) * 12  # 15% weight
            
            # Turnover Protection (10% weight)
            if 'Int' in row and pd.notna(row['Int']):
                score -= row['Int'] * 0.8  # 10% penalty
            
            mvp_scores.append(max(score, 0))  # Don't allow negative scores
        
        passing_df['MVP_Score'] = mvp_scores
        
        # Get top candidates
        available_cols = ['Player', 'MVP_Score']
        for col in ['Tm', 'W', 'L', 'TD', 'Yds', 'Rate']:
            if col in passing_df.columns:
                available_cols.append(col)
        
        mvp_candidates = passing_df.nlargest(10, 'MVP_Score')[available_cols]
        
        if not mvp_candidates.empty:
            print(f"✅ Generated MVP predictions for {len(mvp_candidates)} candidates")
        
        return mvp_candidates
    
    def create_awards_chart(self, mvp_df):
        """Create comprehensive awards chart"""
        if mvp_df.empty:
            print("❌ No data for awards chart")
            return
        
        plt.style.use('dark_background')
        fig, ax = plt.subplots(1, 1, figsize=(14, 8))
        
        try:
            # MVP bar chart
            top_mvp = mvp_df.head(10)
            
            colors = plt.cm.RdYlGn(np.linspace(0.3, 1.0, len(top_mvp)))
            bars = ax.bar(range(len(top_mvp)), top_mvp['MVP_Score'], 
                         color=colors, alpha=0.8, edgecolor='white', linewidth=1)
            
            ax.set_title('🏆 NFL MVP Predictions - Enhanced Model', fontsize=16, color='white', pad=20)
            ax.set_ylabel('MVP Score', fontsize=12)
            ax.set_xlabel('Players', fontsize=12)
            ax.set_xticks(range(len(top_mvp)))
            ax.set_xticklabels([name[:10] for name in top_mvp['Player']], 
                              rotation=45, ha='right', fontsize=10)
            ax.grid(True, alpha=0.3, axis='y')
            
            # Add value labels on bars
            for i, bar in enumerate(bars):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{height:.1f}', ha='center', va='bottom', fontsize=9, 
                       color='white', fontweight='bold')
            
            # Add model info
            model_text = "Enhanced Model Weights:\n• Team Success: 25%\n• Total TDs: 30%\n• QB Efficiency: 20%\n• Passing Yards: 15%\n• Turnover Protection: 10%"
            ax.text(0.02, 0.98, model_text, transform=ax.transAxes, fontsize=9,
                   verticalalignment='top', bbox=dict(boxstyle='round', facecolor='black', alpha=0.8),
                   color='lightblue')
            
            plt.tight_layout()
            
            # Save chart
            chart_path = self.docs_dir / "awards_predictions.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='black')
            plt.close()
            
            print(f"✅ Awards chart saved to {chart_path}")
            
        except Exception as e:
            print(f"❌ Error creating chart: {e}")
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
        print("🏆 NFL AWARDS PREDICTION PROCESSOR")
        print("=" * 60)
        print(f"Processing {self.current_season} NFL season awards...")
        print("Enhanced MVP model based on 2024 Josh Allen analysis")
        
        # Calculate MVP
        mvp_df = self.calculate_mvp_scores()
        
        # Create chart
        print("\n📊 Creating awards chart...")
        self.create_awards_chart(mvp_df)
        
        # Save data
        print("\n💾 Saving awards data...")
        self.save_awards_data(mvp_df)
        
        print("\n" + "=" * 60)
        print("🏆 AWARDS PROCESSING COMPLETE!")
        print("=" * 60)
        
        if not mvp_df.empty:
            top_mvp = mvp_df.iloc[0]
            print(f"🥇 Top MVP candidate: {top_mvp['Player']} with {top_mvp['MVP_Score']:.1f} points")
            if 'Tm' in top_mvp:
                print(f"   Team: {top_mvp['Tm']}")
            if 'W' in top_mvp and 'L' in top_mvp:
                print(f"   Record: {top_mvp['W']:.0f}-{top_mvp['L']:.0f}")

if __name__ == "__main__":
    predictor = NFLAwardsPredictor()
    
    predictor.docs_dir.mkdir(parents=True, exist_ok=True)
    predictor.archive_dir.mkdir(parents=True, exist_ok=True)
    
    predictor.process_awards()