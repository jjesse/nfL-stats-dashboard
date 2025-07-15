#!/usr/bin/env python3
"""
NFL Awards Accuracy Tracker
Tracks prediction accuracy against actual results to improve models
"""

import pandas as pd
import json
from datetime import datetime
from pathlib import Path
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


class NFLAwardsAccuracyTracker:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.docs_dir = self.base_dir / "docs"
        self.archive_dir = self.base_dir / "archive"
        self.accuracy_file = self.docs_dir / "awards_accuracy_history.json"
        
        # Historical actual winners for validation
        self.actual_winners = {
            2023: {
                'MVP': 'Lamar Jackson',
                'OROY': 'C.J. Stroud', 
                'DROY': 'Defensive ROY Placeholder'  # Update with actual
            },
            2022: {
                'MVP': 'Aaron Rodgers',
                'OROY': 'Justin Jefferson', 
                'DROY': 'Defensive ROY Placeholder'
            },
            2021: {
                'MVP': 'Aaron Rodgers',
                'OROY': 'Justin Herbert',
                'DROY': 'Defensive ROY Placeholder'
            },
            2020: {
                'MVP': 'Aaron Rodgers',
                'OROY': 'Justin Herbert',
                'DROY': 'Defensive ROY Placeholder'
            }
        }
        
        print("Initialized NFL Awards Accuracy Tracker")
    
    def load_accuracy_history(self):
        """Load historical accuracy data"""
        if self.accuracy_file.exists():
            with open(self.accuracy_file, 'r') as f:
                return json.load(f)
        return {"predictions": [], "model_performance": {}}
    
    def save_accuracy_history(self, data):
        """Save accuracy data"""
        with open(self.accuracy_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def record_prediction(self, season, award, predicted_winner, predicted_score, actual_winner=None):
        """Record a prediction for future accuracy tracking"""
        history = self.load_accuracy_history()
        
        prediction_record = {
            "season": season,
            "award": award,
            "predicted_winner": predicted_winner,
            "predicted_score": predicted_score,
            "actual_winner": actual_winner,
            "prediction_date": datetime.now().isoformat(),
            "was_correct": None if actual_winner is None else (predicted_winner == actual_winner)
        }
        
        history["predictions"].append(prediction_record)
        self.save_accuracy_history(history)
        
        print(f"Recorded prediction: {season} {award} - {predicted_winner} (Score: {predicted_score:.1f})")
        if actual_winner:
            status = "CORRECT" if predicted_winner == actual_winner else "INCORRECT"
            print(f"  Actual winner: {actual_winner} - Prediction {status}")
    
    def update_with_actual_results(self, season, award_results):
        """Update predictions with actual results when available"""
        history = self.load_accuracy_history()
        
        for prediction in history["predictions"]:
            if prediction["season"] == season and prediction["award"] in award_results:
                actual_winner = award_results[prediction["award"]]
                prediction["actual_winner"] = actual_winner
                prediction["was_correct"] = (prediction["predicted_winner"] == actual_winner)
        
        self.save_accuracy_history(history)
        print(f"Updated {season} predictions with actual results")
    
    def calculate_model_accuracy(self):
        """Calculate overall model accuracy"""
        history = self.load_accuracy_history()
        predictions = history["predictions"]
        
        if not predictions:
            print("No predictions recorded yet")
            return {}
        
        # Filter predictions with known results
        completed_predictions = [p for p in predictions if p.get("was_correct") is not None]
        
        if not completed_predictions:
            print("No completed predictions to analyze")
            return {}
        
        # Calculate accuracy by award type
        accuracy_by_award = {}
        for award in ["MVP", "OROY", "DROY"]:
            award_predictions = [p for p in completed_predictions if p["award"] == award]
            if award_predictions:
                correct = sum(1 for p in award_predictions if p["was_correct"])
                total = len(award_predictions)
                accuracy_by_award[award] = {
                    "correct": correct,
                    "total": total,
                    "accuracy": correct / total * 100
                }
        
        # Overall accuracy
        total_correct = sum(1 for p in completed_predictions if p["was_correct"])
        total_predictions = len(completed_predictions)
        overall_accuracy = total_correct / total_predictions * 100
        
        accuracy_summary = {
            "overall_accuracy": overall_accuracy,
            "total_predictions": total_predictions,
            "total_correct": total_correct,
            "by_award": accuracy_by_award,
            "last_updated": datetime.now().isoformat()
        }
        
        # Save to history
        history["model_performance"] = accuracy_summary
        self.save_accuracy_history(history)
        
        return accuracy_summary
    
    def analyze_prediction_patterns(self):
        """Analyze patterns in incorrect predictions"""
        history = self.load_accuracy_history()
        predictions = history["predictions"]
        
        completed_predictions = [p for p in predictions if p.get("was_correct") is not None]
        incorrect_predictions = [p for p in completed_predictions if not p["was_correct"]]
        
        analysis = {
            "common_mistakes": [],
            "model_biases": [],
            "recommendations": []
        }
        
        # Analyze MVP prediction patterns
        mvp_incorrect = [p for p in incorrect_predictions if p["award"] == "MVP"]
        if mvp_incorrect:
            analysis["common_mistakes"].append({
                "award": "MVP",
                "pattern": "May be overvaluing pure passing stats vs team success",
                "example": f"Predicted {mvp_incorrect[0]['predicted_winner']} over actual winner {mvp_incorrect[0]['actual_winner']}"
            })
            
            analysis["recommendations"].append({
                "award": "MVP", 
                "suggestion": "Increase team wins weight, consider clutch performance metrics"
            })
        
        return analysis
    
    def create_accuracy_dashboard(self):
        """Create visual accuracy tracking dashboard"""
        accuracy_data = self.calculate_model_accuracy()
        
        if not accuracy_data or "by_award" not in accuracy_data:
            print("Insufficient data for accuracy dashboard")
            return
        
        plt.style.use('dark_background')
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        try:
            # 1. Overall Accuracy Gauge
            overall_acc = accuracy_data["overall_accuracy"]
            ax1.pie([overall_acc, 100 - overall_acc], 
                   labels=[f'Correct\n{overall_acc:.1f}%', f'Incorrect\n{100-overall_acc:.1f}%'],
                   colors=['#2ECC71', '#E74C3C'], autopct='', startangle=90)
            ax1.set_title(f'Overall Model Accuracy\n{accuracy_data["total_correct"]}/{accuracy_data["total_predictions"]} Predictions', 
                         fontsize=14, color='white')
            
            # 2. Accuracy by Award Type
            awards = list(accuracy_data["by_award"].keys())
            accuracies = [accuracy_data["by_award"][award]["accuracy"] for award in awards]
            
            colors = ['gold', '#2ECC71', '#8B4513'][:len(awards)]
            bars = ax2.bar(awards, accuracies, color=colors, alpha=0.8)
            ax2.set_title('Accuracy by Award Type', fontsize=14, color='white')
            ax2.set_ylabel('Accuracy (%)')
            ax2.set_ylim(0, 100)
            ax2.grid(True, alpha=0.3, axis='y')
            
            # Add value labels
            for bar, acc in zip(bars, accuracies):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                        f'{acc:.1f}%', ha='center', va='bottom', fontsize=12)
            
            # 3. Prediction History Timeline
            history = self.load_accuracy_history()
            completed_preds = [p for p in history["predictions"] if p.get("was_correct") is not None]
            
            if completed_preds:
                seasons = [p["season"] for p in completed_preds]
                correct_mask = [p["was_correct"] for p in completed_preds]
                
                for i, (season, correct) in enumerate(zip(seasons, correct_mask)):
                    color = '#2ECC71' if correct else '#E74C3C'
                    marker = 'o' if correct else 'x'
                    ax3.scatter(season, i, color=color, marker=marker, s=100)
                
                ax3.set_title('Prediction History', fontsize=14, color='white')
                ax3.set_xlabel('Season')
                ax3.set_ylabel('Prediction Index')
                ax3.grid(True, alpha=0.3)
                
                # Add legend
                ax3.scatter([], [], color='#2ECC71', marker='o', label='Correct')
                ax3.scatter([], [], color='#E74C3C', marker='x', label='Incorrect')
                ax3.legend()
            else:
                ax3.text(0.5, 0.5, 'No completed predictions yet', ha='center', va='center',
                        transform=ax3.transAxes, fontsize=12, color='white')
                ax3.set_title('Prediction History', fontsize=14, color='white')
            
            # 4. Model Performance Summary
            ax4.axis('off')
            summary_text = f"""
MODEL PERFORMANCE SUMMARY

Total Predictions: {accuracy_data.get('total_predictions', 0)}
Correct Predictions: {accuracy_data.get('total_correct', 0)}
Overall Accuracy: {accuracy_data.get('overall_accuracy', 0):.1f}%

Award-Specific Performance:
"""
            
            for award, data in accuracy_data.get("by_award", {}).items():
                summary_text += f"  {award}: {data['correct']}/{data['total']} ({data['accuracy']:.1f}%)\n"
            
            summary_text += f"""
Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Next Steps:
- Collect more historical validation data
- Adjust model weights based on accuracy patterns  
- Track in-season prediction changes
"""
            
            ax4.text(0.05, 0.95, summary_text.strip(), fontsize=11, color='lightblue',
                    transform=ax4.transAxes, verticalalignment='top')
            
            plt.suptitle('NFL Awards Prediction Accuracy Dashboard', 
                        fontsize=18, color='white', y=0.98)
            
            plt.tight_layout()
            
            # Save chart
            chart_path = self.docs_dir / "awards_accuracy_dashboard.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='black')
            plt.close()
            
            print(f"Accuracy dashboard saved to {chart_path}")
            
        except Exception as e:
            print(f"Error creating accuracy dashboard: {e}")
            plt.close()
    
    def process_current_predictions(self):
        """Process current season predictions and check against known results"""
        # Load current predictions
        mvp_file = self.docs_dir / "mvp_predictions.csv"
        
        if mvp_file.exists():
            mvp_df = pd.read_csv(mvp_file)
            if not mvp_df.empty:
                top_mvp = mvp_df.iloc[0]
                
                # Record 2024 prediction
                self.record_prediction(
                    season=2024,
                    award="MVP",
                    predicted_winner=top_mvp['Player'],
                    predicted_score=top_mvp['MVP_Score'],
                    actual_winner="Josh Allen"  # Known 2024 result
                )
        
        # Update any historical predictions with known results
        for season, results in self.actual_winners.items():
            self.update_with_actual_results(season, results)
        
        # Calculate and display accuracy
        accuracy = self.calculate_model_accuracy()
        
        if accuracy:
            print("\n" + "="*50)
            print("MODEL ACCURACY ANALYSIS")
            print("="*50)
            print(f"Overall Accuracy: {accuracy['overall_accuracy']:.1f}%")
            print(f"Total Predictions: {accuracy['total_predictions']}")
            print(f"Correct Predictions: {accuracy['total_correct']}")
            
            for award, data in accuracy.get("by_award", {}).items():
                print(f"{award} Accuracy: {data['accuracy']:.1f}% ({data['correct']}/{data['total']})")
        
        # Create dashboard
        self.create_accuracy_dashboard()
        
        return accuracy

if __name__ == "__main__":
    tracker = NFLAwardsAccuracyTracker()
    
    # Ensure directories exist
    tracker.docs_dir.mkdir(parents=True, exist_ok=True)
    tracker.archive_dir.mkdir(parents=True, exist_ok=True)
    
    # Process predictions and track accuracy
    tracker.process_current_predictions()