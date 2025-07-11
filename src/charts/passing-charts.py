nfl_stats/
├── docs/                           # GitHub Pages site
│   ├── index.html                 # Homepage with navigation
│   ├── offensive_stats.html       # Offensive stats dashboard
│   ├── defensive_stats.html       # Defensive stats dashboard
│   ├── standings.html              # Team standings
│   ├── award_predictions.html      # MVP & other award predictions
│   ├── *.png                      # Generated charts & visualizations
│   ├── *.html                     # Generated data tables
│   └── last_updated_*.txt         # Timestamp files for each data source
├── archive/                       # Historical data for trends
│   ├── offensive_*.csv            # Daily offensive archives
│   └── defensive_*.csv            # Weekly defensive archives
├── .github/workflows/            # Automation pipeline
│   ├── update-offensive.yml       # Daily offensive updates
│   ├── update-defensive.yml       # Weekly defensive updates
│   ├── update-standings.yml       # Daily standings updates
│   └── update-awards.yml          # Daily award predictions
├── offensive_chart.py             # Offensive data processor
├── defensive_chart.py             # Defensive data processor
├── standings_chart.py             # Standings processor
├── mvp_calculator.py              # Award prediction engine
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation