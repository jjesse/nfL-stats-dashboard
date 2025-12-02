# Copilot Instructions for NFL Stats Dashboard

## Project Overview

This is an NFL Stats Dashboard project that provides real-time player stats, team analytics, season schedules, and award predictions with professional-grade visualizations. The dashboard is built with Python for data processing and HTML/JavaScript for the web interface.

## Technology Stack

- **Python 3.8+**: Core language for data processing and analysis
- **pandas**: Data manipulation and analysis
- **matplotlib/seaborn/plotly**: Data visualization and chart generation
- **BeautifulSoup4**: Web scraping for NFL statistics
- **HTML/CSS/JavaScript**: Web dashboard interface
- **GitHub Actions**: Automated data updates and CI/CD
- **GitHub Pages**: Web hosting (served from `docs/` folder)

## Project Structure

```
nfL-stats-dashboard/
├── src/
│   ├── data-processors/    # Data collection and processing scripts
│   ├── charts/             # Chart generation utilities
│   ├── analysis/           # Data analysis modules
│   └── utils/              # Utility functions and helpers
├── docs/                   # Web dashboard files (GitHub Pages source)
│   ├── *.html              # Dashboard pages
│   ├── js/                 # JavaScript files
│   └── *.png, *.csv        # Generated charts and data
├── tests/                  # Test files
├── .github/
│   ├── workflows/          # GitHub Actions workflows
│   └── ISSUE_TEMPLATE/     # Issue templates
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── CONTRIBUTING.md         # Contribution guidelines
```

## Development Environment Setup

1. Use Python 3.8 or higher
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install flake8 pytest  # Development dependencies
   ```

## Code Style Guidelines

### Python
- Follow PEP 8 guidelines
- Maximum line length: 120 characters
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Use type hints where appropriate

### Linting
Run flake8 before committing:
```bash
flake8 --max-line-length=120 --ignore=E501,W503 src/
```

### JavaScript
- Use consistent indentation (2 spaces)
- Add comments for complex logic

## Testing

### Running Tests
```bash
python -m pytest tests/ -v --tb=short
```

### Test Requirements
- Place test files in `tests/` directory
- Follow naming convention `test_*.py`
- Use pytest for writing tests
- Create required directories (`docs`, `archive`) before running tests

## Data Processing

### Key Scripts
- `src/data-processors/run_all_processors.py`: Master processor that runs all data processors
- `src/data-processors/player-stats.py`: Player statistics processor
- `src/data-processors/team-stats-basic.py`: Team statistics processor
- `src/data-processors/schedule-processor.py`: Schedule and results processor
- `src/data-processors/awards-tracker.py`: Award predictions processor

### Guidelines
- Always include graceful error handling with try/except blocks
- Add appropriate logging for debugging
- Be mindful of API rate limits when scraping external sources
- Generate high-quality visualizations (300 DPI) with dark theme styling

## Web Dashboard

### Local Development
```bash
cd docs
python -m http.server 8000
# Access at http://localhost:8000
```

### Generated Files
- Charts are saved to `docs/` as PNG files
- Data is exported as CSV files to `docs/`

## GitHub Actions Workflows

- `ci.yml`: Linting and testing on PRs
- `update-all.yml`: Automated data updates
- `update-nfl-data-with-accuracy.yml`: Data updates with accuracy tracking
- `update-standings.yml`: Standings updates
- `update-stats.yml`: Statistics updates

## Common Tasks

### Adding a New Data Processor
1. Create new Python file in `src/data-processors/`
2. Follow existing processor patterns for error handling and logging
3. Add corresponding tests in `tests/`
4. Update `run_all_processors.py` to include the new processor

### Adding a New Dashboard Page
1. Create HTML file in `docs/`
2. Follow existing page structure and styling
3. Link from the main navigation in `index.html`

### Updating Dependencies
1. Add new dependencies to `requirements.txt`
2. Document any version constraints
3. Test installation in a clean environment

## Commit Message Format
- `feat: Add new feature description`
- `fix: Fix bug description`
- `docs: Update documentation`
- `refactor: Code refactoring description`
- `test: Add or update tests`

## Important Notes

- The `docs/` folder is the source for GitHub Pages deployment
- Generated charts and data files should be committed to `docs/`
- External data sources include Pro Football Reference, ESPN, and NFL.com
- Be mindful of web scraping ethics and rate limits
