# 🏈 NFL Stats Dashboard

A comprehensive, automated NFL statistics dashboard that provides real-time player stats, team performance metrics, standings, and award predictions. Built with Python and deployed via GitHub Pages.

## 🚀 Features

- **Player Statistics**: Passing, rushing, receiving, and defensive stats
- **Team Analysis**: Win/loss records, points scored/allowed, and performance metrics
- **Live Standings**: Current division standings and playoff picture
- **Award Predictions**: MVP, Offensive/Defensive Player of the Year calculations
- **Historical Trends**: Track player and team performance over time
- **Automated Updates**: Regular data refreshes via GitHub Actions
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Mode**: Easy on the eyes for extended viewing

## 📊 Dashboard Sections

### Player Stats
- **Passing Leaders**: Yards, TDs, completion percentage
- **Rushing Leaders**: Yards, TDs, yards per carry
- **Receiving Leaders**: Receptions, yards, TDs
- **Defensive Leaders**: Tackles, sacks, interceptions

### Team Analytics
- **Performance Metrics**: Points for/against, win percentage
- **Efficiency Stats**: Yards per play, turnover differential
- **Head-to-Head Comparisons**: Team vs team analysis

### Standings & Playoffs
- **Division Standings**: Current records and rankings
- **Playoff Picture**: Wild card and division race tracking
- **Strength of Schedule**: Remaining games difficulty

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
- Pro Football Reference (primary)
- ESPN (backup)
- NFL.com (official stats)

### Update Frequency
- **Player Stats**: Every 6 hours during season
- **Team Stats**: Daily
- **Standings**: Every 4 hours
- **Awards**: Daily

### Customization
Edit the configuration in each processor file:
- `src/data-processors/player-stats.py`
- `src/data-processors/team-stats.py`
- `src/data-processors/standings.py`
- `src/data-processors/awards-tracker.py`

## 📈 Data Processing Pipeline

```
Data Sources → Python Processors → CSV/JSON → Charts → HTML Dashboard
     ↓              ↓                 ↓          ↓         ↓
  NFL APIs    →  Data Cleaning  →  Storage  →  Matplotlib → GitHub Pages
```

## 🤖 Automation

The dashboard uses GitHub Actions for automated updates:

- **Schedule**: Runs every 6 hours during NFL season
- **Manual Trigger**: Can be triggered manually via GitHub interface
- **Error Handling**: Continues with partial data if some sources fail
- **Notifications**: Logs all update attempts and results

## 📱 Responsive Design

The dashboard adapts to different screen sizes:
- **Desktop**: Full grid layout with multiple charts
- **Tablet**: Stacked layout with optimized charts
- **Mobile**: Single column with touch-friendly navigation

## 🎨 Styling

- **Color Scheme**: Dark mode optimized for extended viewing
- **Typography**: Clean, readable fonts with proper contrast
- **Charts**: High-contrast colors for accessibility
- **Layout**: Grid-based responsive design

## 🔍 Troubleshooting

### Common Issues

1. **Data not updating**
   - Check GitHub Actions logs
   - Verify API endpoints are accessible
   - Ensure file permissions are correct

2. **Charts not displaying**
   - Verify matplotlib is installed
   - Check file paths in HTML
   - Ensure PNG files are generated

3. **Missing data**
   - Check internet connection
   - Verify data source availability
   - Review error logs in processor files

### Debug Mode
Run processors with debug output:
```bash
python src/data-processors/player-stats.py --debug
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
- Review the automated workflow logs

---

**Last Updated**: Automatically updated via GitHub Actions
**Data Sources**: Pro Football Reference, ESPN, NFL.com
**Update Frequency**: Every 6 hours during NFL season