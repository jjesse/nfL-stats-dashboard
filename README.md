# 🏈 NFL Stats Dashboard

A comprehensive, automated NFL statistics dashboard that provides real-time player stats, team performance metrics, and visualizations. Built with Python and deployed via GitHub Pages.

## 🚀 Features

- **Player Statistics**: Passing, rushing, receiving, and defensive stats with top 10 leaderboards
- **Team Analysis**: Win/loss records, points scored/allowed, point differential, and performance metrics
- **Automated Data Collection**: Web scraping from Pro Football Reference
- **Visual Charts**: Dark-themed matplotlib charts for all statistics
- **Data Archiving**: Historical data storage with timestamps
- **Automated Updates**: Regular data refreshes via GitHub Actions every 6 hours
- **Responsive Web Dashboard**: Clean, dark-mode interface with tabbed navigation

## 📊 Dashboard Sections

### Player Stats
- **Passing Leaders**: Yards, TDs, completion percentage, QB rating
- **Rushing Leaders**: Yards, TDs, yards per attempt, total attempts
- **Receiving Leaders**: Receptions, yards, TDs, yards per reception
- **Defensive Leaders**: Tackles, sacks, interceptions, pass deflections

### Team Analytics
- **Points Analysis**: Points for vs points against scatter plot with team labels
- **Win Percentage**: Ranked bar chart of all teams
- **Point Differential**: Positive/negative differential with color coding
- **Win/Loss Comparison**: Side-by-side wins vs losses for all teams

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Git
- GitHub account (for automated updates)

### Local Development
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/nfl-stats-dashboard.git
   cd nfl-stats-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create required directories**
   ```bash
   mkdir -p docs archive
   ```

4. **Run data processors**
   ```bash
   python src/data-processors/player-stats.py
   python src/data-processors/team-stats.py
   ```

5. **Open the dashboard**
   ```bash
   # Open docs/index.html in your browser
   open docs/index.html
   ```

## 🔧 Configuration

### Data Sources
The dashboard pulls data from:
- Pro Football Reference (primary source)
- Automated web scraping with proper user-agent headers
- Error handling for failed requests

### Update Frequency
- **All Stats**: Every 6 hours during season via GitHub Actions
- **Manual Trigger**: Available through GitHub Actions interface
- **Data Archiving**: Every update saves timestamped copies

### File Structure
```
nfl-stats-dashboard/
├── src/data-processors/
│   ├── player-stats.py          # Player statistics processor
│   └── team-stats.py            # Team statistics processor
├── docs/                        # GitHub Pages deployment
│   ├── index.html              # Main dashboard
│   ├── *_stats.png             # Generated charts
│   ├── *_stats.csv             # Data tables
│   └── last_updated_*.txt      # Timestamps
├── archive/                     # Historical data
├── .github/workflows/           # Automation
│   └── update-stats.yml        # Main update workflow
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 📈 Data Processing Pipeline

```
Pro Football Reference → Web Scraping → Data Cleaning → Chart Generation → File Output
                                    ↓
                               CSV Storage → GitHub Pages → Web Dashboard
                                    ↓
                            Archive with Timestamps
```

## 🤖 Automation

The dashboard uses GitHub Actions for automated updates:

- **Schedule**: Runs every 6 hours during NFL season
- **Manual Trigger**: Can be triggered manually via GitHub interface
- **Error Handling**: Continues with partial data if some sources fail
- **File Management**: Automatically creates directories and manages outputs

## 📱 Dashboard Features

### Current Implementation
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Mode**: Optimized for extended viewing
- **Tabbed Navigation**: Overview, Players, Teams, Standings, Awards
- **Dynamic Content**: JavaScript-powered tab switching
- **Error Handling**: Graceful fallbacks for missing images

### Chart Types
- **Bar Charts**: Top 10 leaderboards for all stat categories
- **Scatter Plots**: Points for vs points against analysis
- **Comparative Charts**: Win/loss side-by-side comparisons
- **Color-coded Visuals**: Positive/negative indicators

## 🎨 Technical Details

### Python Libraries Used
- **requests**: Web scraping with proper headers
- **pandas**: Data manipulation and CSV handling
- **matplotlib**: Chart generation with dark themes
- **seaborn**: Enhanced statistical visualizations
- **pathlib**: Modern file path handling

### Data Processing Features
- **Robust Error Handling**: Graceful failures with informative messages
- **Data Validation**: Numeric conversion with error handling
- **Column Flexibility**: Handles different table structures
- **User-Agent Spoofing**: Prevents blocking by target websites

## 🔍 Troubleshooting

### Common Issues

1. **Data not updating**
   - Check GitHub Actions logs in the Actions tab
   - Verify Pro Football Reference is accessible
   - Ensure file permissions are correct

2. **Charts not displaying**
   - Verify matplotlib is installed correctly
   - Check that PNG files are generated in docs/
   - Ensure proper file paths in HTML

3. **Missing data**
   - Check internet connection
   - Verify Pro Football Reference site structure hasn't changed
   - Review error logs in processor output

### Debug Mode
Run processors individually to see detailed output:
```bash
python src/data-processors/player-stats.py
python src/data-processors/team-stats.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Pro Football Reference for comprehensive NFL data
- GitHub Pages for free hosting
- The Python data science community for excellent libraries

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check the troubleshooting guide above
- Review the automated workflow logs in GitHub Actions

---

**Last Updated**: Automatically updated via GitHub Actions  
**Data Source**: Pro Football Reference  
**Update Frequency**: Every 6 hours during NFL season  
**Current Season**: 2024 NFL Season