# 🏈 NFL Stats Dashboard

A comprehensive, automated NFL statistics dashboard that provides real-time player and team analytics with beautiful visualizations.

## ✨ Features

### 📊 **Player Statistics**
- **Passing Stats**: Yards, TDs, completion %, QB rating
- **Rushing Stats**: Yards, TDs, attempts, yards per carry
- **Receiving Stats**: Catches, yards, TDs, yards per reception
- **Defensive Stats**: Tackles, sacks, interceptions, pass deflections

### 🏆 **Team Analytics**
- Win/loss records and standings
- Points for/against analysis
- Advanced team metrics
- Conference comparisons
- Pythagorean win expectation

### 🎨 **Visualizations**
- Dark-themed professional charts
- Top 10 leaderboards for all categories
- High-resolution PNG exports (300 DPI)
- Responsive web dashboard

### 🤖 **Automation**
- GitHub Actions for data updates every 6 hours
- Historical data archiving
- Automatic chart regeneration
- Error handling and logging

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Ubuntu/Linux system (recommended)
- Internet connection for data fetching

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/nfL-stats-dashboard.git
   cd nfL-stats-dashboard
   ```

2. **Set up the environment:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Activate virtual environment:**
   ```bash
   source nfl_dashboard_env/bin/activate
   ```

4. **Set up directories:**
   ```bash
   python setup_directories.py
   ```

5. **Generate initial data:**
   ```bash
   python src/data-processors/player-stats.py
   python src/data-processors/team-stats.py
   ```

6. **View the dashboard:**
   Open `docs/index.html` in your browser or set up GitHub Pages.

## 📱 Dashboard

The dashboard includes five main sections:

- **Overview**: Key statistics at a glance
- **Players**: Detailed player statistics and charts
- **Teams**: Team performance and analytics
- **Standings**: League standings and rankings
- **Awards**: Award predictions (coming soon)

## 🔄 Current Status

### ✅ **Completed Features**
- ✅ Player statistics processor (passing, rushing, receiving, defense)
- ✅ Professional chart generation with dark theme
- ✅ CSV data export and archiving
- ✅ HTML dashboard with responsive design
- ✅ GitHub Actions automation workflow
- ✅ Error handling and logging
- ✅ Season detection (automatically uses 2024 season for July 2025)

### 🚧 **In Progress**
- 🚧 Team statistics processor (partially complete)
- 🚧 Advanced team analytics
- 🚧 GitHub Pages deployment

### 📋 **Planned Features**
- 📋 Award predictions (MVP, OROY, DROY)
- 📋 Playoff probability calculations
- 📋 Player comparison tools
- 📋 Historical trend analysis

## 🛠️ Technical Details

### Data Sources
- **Pro Football Reference**: Primary data source for all NFL statistics
- **Season Detection**: Automatically detects current/most recent completed season
- **Rate Limiting**: Respectful scraping with delays between requests

### Architecture
```
nfL-stats-dashboard/
├── docs/                    # GitHub Pages website
│   ├── index.html          # Main dashboard
│   ├── *.png              # Generated charts
│   ├── *.csv              # Data exports
│   └── last_updated_*.txt # Timestamps
├── archive/                # Historical data
├── src/
│   └── data-processors/   # Python scripts
├── .github/workflows/     # Automation
└── requirements.txt       # Dependencies
```

### Charts Generated
- `passing_stats.png` - Quarterback performance metrics
- `rushing_stats.png` - Running back statistics
- `receiving_stats.png` - Wide receiver and tight end stats
- `defense_stats.png` - Defensive player metrics
- `team_stats.png` - Team performance overview
- `team_advanced_analytics.png` - Advanced team metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📊 Data Updates

The dashboard automatically updates every 6 hours during the NFL season via GitHub Actions. Data includes:

- Player statistics from all games
- Team standings and records
- Advanced analytics calculations
- Historical data archiving

## 🐛 Known Issues

- Web scraping may occasionally fail due to website changes
- Large historical datasets may impact performance
- Some advanced statistics require manual verification

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Pro Football Reference](https://www.pro-football-reference.com/) for providing comprehensive NFL statistics
- [Matplotlib](https://matplotlib.org/) for visualization capabilities
- [Pandas](https://pandas.pydata.org/) for data processing
- GitHub Actions for automation infrastructure

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-username/nfL-stats-dashboard/issues) page
2. Review the troubleshooting section below
3. Create a new issue with detailed information

### Troubleshooting

**Common Issues:**

1. **Directory Errors**: Run `python setup_directories.py` to fix
2. **Missing Dependencies**: Run `pip install -r requirements.txt`
3. **Data Fetching Errors**: Check internet connection and Pro Football Reference availability
4. **Chart Generation Issues**: Ensure matplotlib backend is properly configured

---

**Last Updated**: July 2025  
**Version**: 1.0.0  
**Status**: Active Development