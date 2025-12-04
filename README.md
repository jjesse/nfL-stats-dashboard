# 🏈 NFL Stats Dashboard

A comprehensive, interactive NFL statistics dashboard that provides real-time player stats, team analytics, season schedules, and award predictions with professional-grade visualizations.

## ✨ Features

### 📊 **Interactive Dashboard**
- **Tabbed Interface**: Overview, Schedule, Players, Teams, Standings, Awards
- **Interactive Charts**: Hover tooltips, zoom controls, and fullscreen viewing
- **Mobile Responsive**: Optimized for all devices
- **Real-time Data**: Automated updates with GitHub Actions

### 🏈 **Comprehensive NFL Data**
- **Player Statistics**: Passing, rushing, receiving, and defensive stats
- **Team Analytics**: Win/loss records, standings, and performance metrics
- **Season Schedule**: Complete game results with weekly breakdowns
- **Award Predictions**: MVP, OROY, DROY with accuracy tracking

### 🎯 **Specialized Pages**
- **📅 Schedule Tab**: Complete season schedule with game results and weekly filters
- **🏃 Rushing Stats**: Comprehensive rushing leaders and analytics
- **🎯 Receiving Stats**: Top receivers with detailed performance metrics
- **🛡️ Defense Stats**: Defensive leaders across all major categories
- **📊 Passing Stats**: Quarterback performance and efficiency metrics
- **📋 Standings**: Team standings with playoff indicators and division races

### 🔧 **Technical Features**
- **Automated Data Processing**: Multi-source data collection and validation
- **High-Quality Visualizations**: 300 DPI charts with dark theme styling
- **Error Handling**: Graceful fallbacks and comprehensive logging
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/nfL-stats-dashboard.git
cd nfL-stats-dashboard

# Install dependencies
pip install -r requirements.txt

# Generate data and charts
python src/data-processors/run_all_processors.py

# Start local web server
cd docs
python -m http.server 8000

# Open browser to http://localhost:8000
```

## 📁 Project Structure

```
nfL-stats-dashboard/
├── 📄 README.md                 # Project documentation
├── 📋 TODO.md                   # Development roadmap
├── 📦 requirements.txt          # Python dependencies
├── 🗂️ src/
│   ├── 📊 data-processors/      # Data collection and processing
│   │   ├── 🏃 player-stats.py   # Player statistics processor
│   │   ├── 🏈 team-stats-basic.py # Team statistics processor
│   │   ├── 📅 schedule-processor.py # Schedule and results processor
│   │   ├── 🏆 awards-tracker.py # Award predictions processor
│   │   ├── 📈 team-weekly-trends.py # Team momentum analysis
│   │   └── ⚙️ run_all_processors.py # Master processor script
│   ├── 📊 charts/               # Chart generation utilities
│   └── 🛠️ utils/               # Utility functions and helpers
├── 📱 docs/                     # Web dashboard files
│   ├── 🏠 index.html            # Main dashboard
│   ├── 🏃 rushing.html          # Rushing statistics page
│   ├── 🎯 receiving.html        # Receiving statistics page
│   ├── 🛡️ defense.html          # Defense statistics page
│   ├── 📊 passing.html          # Passing statistics page
│   ├── 📋 standings.html        # Team standings page
│   ├── ⚡ js/interactive-charts.js # Interactive chart enhancements
│   └── 📊 *.png, *.csv          # Generated charts and data
└── 🔄 .github/workflows/       # GitHub Actions automation
```

## 🎮 Usage

### Data Generation
```bash
# Generate all NFL data and charts
python src/data-processors/run_all_processors.py

# Generate specific data types
python src/data-processors/player-stats.py      # Player statistics
python src/data-processors/team-stats-basic.py  # Team standings
python src/data-processors/schedule-processor.py # Schedule results
python src/data-processors/awards-tracker.py    # Award predictions
```

### Web Dashboard
```bash
# Start local development server
cd docs
python -m http.server 8000

# Access dashboard at http://localhost:8000
```

### Interactive Features
- **Hover over charts** for detailed player stats and insights
- **Use zoom controls** (🔍+ / 🔍- / ↻ / ⛶) for detailed analysis
- **Click charts** to progressively zoom in/out
- **Filter schedules** by team, week, or game status
- **Navigate tabs** for different data categories

## 📊 Data Sources

- **Pro Football Reference**: Primary source for NFL statistics
- **ESPN**: Supplementary data and validation
- **NFL.com**: Official team and schedule information

## 🔄 Automation

The dashboard includes GitHub Actions workflows for:
- **Automated data updates** every 6 hours during NFL season
- **Award prediction accuracy tracking** with historical validation
- **Error monitoring** and notification system
- **GitHub Pages deployment** for web hosting

## 🏆 Award Predictions

Our enhanced MVP model includes:
- **Performance metrics**: Passing yards, touchdowns, completion percentage
- **Team success factors**: Win percentage, playoff positioning
- **Advanced analytics**: QBR, efficiency ratings, clutch performance
- **Historical accuracy**: Tracked predictions vs actual results

## 🌐 Deployment

### GitHub Pages (Recommended)
1. Enable GitHub Pages in repository settings
2. Set source to `docs` folder
3. GitHub Actions will automatically update data

### Local Development
```bash
cd docs
python -m http.server 8000
```

## 🔧 Troubleshooting

### Schedule Tab Not Working

If you see "Could not load schedule data" error:

1. **Run the schedule processor**:
   ```bash
   python src/data-processors/schedule-processor.py
   ```

2. **Verify the CSV format**: The `docs/schedule_results.csv` file should contain these columns:
   - Week, Date, Time, Away_Team, Away_Score, Home_Team, Home_Score, Winner, Status

3. **Check the timestamp**: Verify `docs/last_updated_schedule.txt` exists

4. **Use the master processor** to generate all data:
   ```bash
   python src/data-processors/run_all_processors.py
   ```

### Charts Not Displaying

If charts show error messages:

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Generate data**: `python src/data-processors/run_all_processors.py`
3. **Check file permissions**: Ensure `docs/` directory is writable
4. **Clear browser cache**: Hard refresh the page (Ctrl+Shift+R)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Pro Football Reference** for comprehensive NFL statistics
- **NFL.com** for official team and schedule data
- **ESPN** for supplementary analytics and validation
- **GitHub** for hosting and automation infrastructure

## 📞 Support

For issues, questions, or feature requests:
- 🐛 [Report bugs](https://github.com/yourusername/nfL-stats-dashboard/issues)
- 💡 [Request features](https://github.com/yourusername/nfL-stats-dashboard/issues)
- 📧 [Contact maintainer](mailto:your.email@example.com)

---

**🏈 Built with passion for NFL analytics and data visualization**