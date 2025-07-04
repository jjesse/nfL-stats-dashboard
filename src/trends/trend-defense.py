nfl_stats/
├── docs/                           # GitHub Pages site
│   ├── index.html                 # Homepage with navigation
│   ├── player_stats.html          # Player stats dashboard
│   ├── team_stats.html            # Team stats dashboard
│   ├── standings.html              # Team standings
│   ├── award_predictions.html      # Award predictions
│   ├── *.png                      # Generated charts & visualizations
│   ├── *.html                     # Generated data tables
│   └── last_updated_*.txt         # Timestamp files for each data source
├── archive/                       # Historical data for trends
│   ├── player_*.csv              # Daily player archives
│   └── team_*.csv                # Weekly team archives
├── .github/workflows/            # Automation pipeline
│   ├── update-player-stats.yml    # Daily player stats updates
│   ├── update-team-stats.yml      # Weekly team stats updates
│   ├── update-standings.yml       # Daily standings updates
│   └── update-awards.yml          # Daily award predictions
├── player_chart.py                # Player data processor
├── team_chart.py                  # Team data processor
├── standings_chart.py             # Standings processor
├── award_prediction_calculator.py  # Award prediction engine
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation