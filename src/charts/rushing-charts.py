nfl_stats/
├── docs/                           # GitHub Pages site
│   ├── index.html                 # Homepage with navigation
│   ├── player_stats.html          # Player stats dashboard
│   ├── team_stats.html            # Team stats dashboard
│   ├── standings.html              # Team standings
│   ├── award_predictions.html      # Award predictions
│   ├── *_predictions.csv          # Award prediction CSV exports
│   ├── *.png                      # Generated charts & visualizations
│   ├── *.html                     # Generated data tables
│   └── last_updated_*.txt         # Timestamp files for each data source
├── archive/                       # Historical data for trends
│   ├── player_stats_*.csv        # Daily player stats archives
│   └── team_stats_*.csv          # Weekly team stats archives
├── .github/workflows/            # Automation pipeline
│   ├── update-player-stats.yml    # Daily player stats updates
│   ├── update-team-stats.yml      # Weekly team stats updates
│   ├── update-standings.yml       # Daily standings updates
│   ├── update-awards.yml          # Daily award predictions
│   └── update-all.yml             # Master workflow (complete rebuild)
├── player_chart.py                # Player data processor
├── team_chart.py                  # Team data processor
├── standings_chart.py             # Standings processor
├── award_calculator.py            # Award prediction engine
├── trend_analysis.py              # Trend analyzer for stats
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation