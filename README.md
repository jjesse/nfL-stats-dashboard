# NFL Stats Dashboard

[![Update NFL Stats Data](https://github.com/jjesse/nfl-stats-dashboard/actions/workflows/update-data.yml/badge.svg)](https://github.com/jjesse/nfl-stats-dashboard/actions/workflows/update-data.yml)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://jjesse.github.io/nfl-stats-dashboard/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](VERSION.md)

A modern, responsive web dashboard for viewing NFL statistics, schedules, and player performance data. Built with vanilla HTML, CSS, and JavaScript, designed to be hosted on GitHub Pages with automated data updates via GitHub Actions.

**🎉 Version 1.0.0 Released!** - Phase 5 complete with 4 new statistics pages, enhanced interactivity, and playoff picture feature.

## 🏈 Project Overview

The NFL Stats Dashboard provides an easy-to-navigate interface for accessing comprehensive NFL data including:

- **Schedule**: View upcoming games with team records and venue information (Weeks 14-18)
- **Betting Odds**: Toggle to display spreads, moneylines, and totals for upcoming games (requires setup)
- **Standings**: NFL standings organized by division and conference
- **Team Statistics**: Compare team performance across the league
- **Player Leaders**: Track top performers in multiple categories:
  - Quarterbacks (passing stats)
  - Receivers (receiving stats)
  - Rushing leaders
  - Defensive leaders (tackles, sacks, interceptions)
  - Special teams (kickers, punters, returners)
- **League Leaders**: Consolidated summary of top performers across all categories
- **Playoff Picture**: Current playoff seeding based on standings ("If playoffs started today")
- **Automated Updates**: Data refreshes automatically every Tuesday at 6 AM EST via GitHub Actions

## 📋 Features

### Core Features
- ✅ Clean, modern design optimized for all devices
- ✅ Responsive layout for desktop, tablet, and mobile
- ✅ Easy navigation with dropdown menus
- ✅ Comprehensive data tables with click-to-sort functionality
- ✅ Live data from ESPN Public API
- ✅ Automated weekly data updates via GitHub Actions
- ✅ localStorage caching (5-minute expiration) for improved performance
- ✅ Well-commented, maintainable codebase

### Enhanced Interactivity (Phase 4)
- ✅ **Search & Filter**: Real-time search on player tables
- ✅ **Team Filters**: Dynamic dropdown filters for all player stat pages
- ✅ **Scroll-to-Top Button**: Fixed button appears after scrolling 300px
- ✅ **Loading Animations**: Smooth loading states and transitions
- ✅ **Keyboard Navigation**: Shortcuts (Alt+H, Alt+S, Alt+T, Alt+P, Esc)
- ✅ **Smooth Scrolling**: Enhanced user experience with CSS scroll behavior
- ✅ **Accessibility**: ARIA labels, screen reader support, focus indicators

### Additional Statistics Pages (Phase 5)
- ✅ **Defensive Leaders**: Tabbed interface with tackles, sacks, and interceptions
- ✅ **Special Teams**: Tabbed interface with kickers, punters, and return specialists
- ✅ **League Leaders Summary**: Consolidated dashboard showing top 5 performers across 12 categories
- ✅ **Playoff Picture**: Dynamic playoff seeding with current standings, division winners, wild cards, and "in the hunt" teams

### Betting Odds Integration (Phase 6 - In Progress)
- ✅ **Toggle Button**: Show/hide betting odds on schedule page
- ✅ **Spread Display**: Point spreads with favorite/underdog indicators
- ✅ **Moneyline**: Money line odds for both teams
- ✅ **Totals**: Over/under totals with pricing
- ✅ **Smart Matching**: Automatically matches odds to games by team names
- ✅ **Caching**: 30-minute localStorage cache for performance
- ✅ **Legal Disclaimers**: Responsible gambling notices and age restrictions
- ✅ **Secure Setup**: GitHub Actions fetches odds weekly using GitHub Secrets
- 🔧 **Setup Required**: See [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md) for configuration

## 🚀 Getting Started

### Prerequisites

No special software is required! The dashboard runs entirely in the browser using static HTML, CSS, and JavaScript.

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/nfl-stats-dashboard.git
   cd nfl-stats-dashboard
   ```

2. **Open in your browser**
   - Simply open `index.html` in your web browser
   - Or use a local development server:
     ```bash
     # Using Python 3
     python -m http.server 8000
     
     # Using Node.js (if you have http-server installed)
     npx http-server
     ```
   - Navigate to `http://localhost:8000` in your browser

### Deployment to GitHub Pages

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Enable GitHub Pages**
   - Go to your repository settings
   - Navigate to "Pages" in the left sidebar
   - Under "Source", select `main` branch and `/root` folder
   - Click "Save"
   - Your site will be live at `https://yourusername.github.io/nfl-stats-dashboard/`

## 📁 Project Structure

```
nfl-stats-dashboard/
├── index.html              # Home page with welcome message
├── schedule.html           # Game schedule page
├── standings.html          # NFL standings by division/conference
├── team-stats.html         # Team statistics page
├── qb-leaders.html         # Quarterback leaders page
├── receiver-leaders.html   # Receiver leaders page
├── rushing-leaders.html    # Rushing leaders page
├── defensive-leaders.html  # Defensive stats (tackles, sacks, interceptions)
├── special-teams.html      # Special teams (kickers, punters, returners)
├── league-leaders.html     # League-wide leaders summary dashboard
├── playoff-picture.html    # Current playoff seeding and bracket
├── about.html              # About page with project info
├── styles.css              # Main stylesheet with responsive design (800+ lines)
├── app.js                  # JavaScript for data handling and interactivity (1400+ lines)
├── api.js                  # API integration module for ESPN data
├── .github/
│   └── workflows/
│       └── update-data.yml # GitHub Actions workflow for automated updates
├── scripts/
│   └── fetch-data.js       # Node.js script to fetch NFL data from ESPN API
├── data/                   # JSON data files (auto-updated by GitHub Actions)
│   ├── schedule.json
│   ├── standings.json
│   ├── team-stats.json
│   ├── player-stats.json
│   ├── odds.json           # Betting odds (requires GitHub Secret setup)
│   └── metadata.json
├── README.md               # This file
├── TODO.md                 # Development roadmap (58% complete)
├── TESTING.md              # Testing guide and instructions
├── GITHUB_SECRETS_SETUP.md # Guide for setting up betting odds API key
├── API_STATUS.md           # API integration status and details
└── project_description.md  # Original project requirements
```

## 🎨 Design Details

The dashboard uses a modern color scheme inspired by the NFL:
- **Primary Color**: NFL Blue (#013369)
- **Secondary Color**: NFL Red (#D50A0A)
- **Accent Color**: Gold (#FFB612)

The design is fully responsive with breakpoints for:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (<768px)

## 💻 Technology Stack

- **HTML5**: Semantic markup for accessibility with ARIA labels
- **CSS3**: Modern styling with CSS variables, flexbox, grid, and animations
- **JavaScript (ES6+)**: Vanilla JavaScript - no frameworks
  - Dynamic content loading and DOM manipulation
  - localStorage caching with expiration
  - Real-time search and filtering
  - Sortable tables
  - Keyboard event handling
- **ESPN Public API**: Live NFL statistics data
- **GitHub Pages**: Free hosting for static websites
- **GitHub Actions**: Automated weekly data updates (active)

## 🔄 Automated Data Updates

The dashboard features **automated weekly data updates** powered by GitHub Actions:

### How It Works

1. **GitHub Actions Workflow** (`.github/workflows/update-data.yml`)
   - Runs every **Tuesday at 6 AM EST** to capture all weekly NFL games (Thursday-Monday)
   - Can be manually triggered from the Actions tab
   - Automatically commits and pushes updated data files

2. **Data Fetching Script** (`scripts/fetch-data.js`)
   - Node.js script that fetches data from ESPN's public API
   - Retrieves schedule, standings, team stats, and player leaders
   - Saves data as JSON files in the `data/` directory

3. **Live Data** (Browser)
   - Dashboard pages fetch data directly from ESPN API when loaded
   - 5-minute localStorage caching for optimal performance
   - Automatic error handling and fallbacks

### Manual Updates

To manually fetch updated data:

```bash
# Run the fetch script locally
node scripts/fetch-data.js

# Or trigger the GitHub Action
# Go to Actions tab → "Update NFL Stats Data" → "Run workflow"
```

### Data Sources

- **Primary**: ESPN Public API (live data)
- **Backup**: JSON files in `data/` directory (weekly snapshots)
- **Cache**: localStorage (5-minute expiration)

## 🎯 Key Highlights

### 11 Interactive Pages
1. **Home** - Welcome and navigation hub
2. **Schedule** - Week-by-week game schedule with optional betting odds
3. **Standings** - Division and conference standings
4. **Team Stats** - Comprehensive team statistics
5. **QB Leaders** - Top quarterbacks with search/filter
6. **Receiver Leaders** - Top receivers with search/filter
7. **Rushing Leaders** - Top rushers with search/filter
8. **Defensive Leaders** - Tackles, sacks, interceptions (tabbed)
9. **Special Teams** - Kickers, punters, returners (tabbed)
10. **League Leaders** - Top 5 across 12 statistical categories
11. **Playoff Picture** - Current playoff seeding and scenarios

### Smart Features
- **Sortable Tables**: Click any column header to sort
- **Real-time Search**: Filter players as you type
- **Team Filtering**: Dropdown filters dynamically populated from table data
- **Keyboard Shortcuts**: Navigate quickly with Alt+H/S/T/P, clear filters with Esc
- **Responsive Design**: Optimized for all screen sizes
- **Loading States**: Smooth animations while data loads
- **Accessibility**: Full ARIA support and keyboard navigation

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. **Make your changes**
   - Follow existing code style and conventions
   - Add comments to explain complex logic
   - Test on multiple devices/browsers
4. **Commit your changes**
   ```bash
   git commit -m "Add: Brief description of changes"
   ```
5. **Push to your branch**
   ```bash
   git push origin feature/YourFeatureName
   ```
6. **Open a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues

### Working with GitHub Copilot Agent

If you're using GitHub Copilot agent to make changes:
- See [Agent Session Management Guide](AGENT_SESSION_MANAGEMENT.md) for best practices
- Use the [Quick Cleanup Guide](QUICK_START_AGENT_CLEANUP.md) if sessions get stuck
- Keep only 1-2 active agent sessions at a time
- Provide clear, specific instructions in your prompts

### Code Style Guidelines

- Use semantic HTML5 elements
- Follow BEM naming convention for CSS classes where appropriate
- Use meaningful variable and function names in JavaScript
- Add comments for complex logic
- Ensure responsive design principles are maintained
- Test accessibility features

## 🐛 Bug Reports

Found a bug? Please open an issue with:
- A clear, descriptive title
- Steps to reproduce the problem
- Expected vs actual behavior
- Screenshots if applicable
- Browser and device information

## 📊 Current Progress

**Overall Completion: 58% (76/131 tasks)**

- ✅ **Phase 1**: Initial Setup - 100% complete
- ✅ **Phase 2**: Data Integration - 100% complete  
- ✅ **Phase 3**: GitHub Actions - 88% complete
- ✅ **Phase 4**: Enhanced Interactivity - 100% complete
- ✅ **Phase 5**: Additional Statistics Pages - 100% complete
- 🚧 **Betting Odds**: Integration - 85% complete (34/40 tasks)

See [TODO.md](TODO.md) for the complete development roadmap.

## 🎰 Betting Odds Setup (Optional)

The schedule page includes an optional betting odds feature that displays spreads, moneylines, and totals for upcoming games. To enable this feature:

1. **Get an API Key**
   - Sign up at [The Odds API](https://the-odds-api.com/)
   - Free tier provides 500 requests/month (adequate for weekly updates)

2. **Configure GitHub Secret**
   - Go to repository Settings → Secrets and variables → Actions
   - Create secret named `ODDS_API_KEY` with your API key
   - See [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md) for detailed instructions

3. **Data Updates**
   - GitHub Actions will automatically fetch odds weekly
   - Odds are saved to `data/odds.json`
   - Schedule page reads from static file (no API key exposure)

**Important**: Betting odds are for informational purposes only. Must be 21+ to bet. Not available in all jurisdictions. Please gamble responsibly.

## 📝 Future Enhancements

Key upcoming features:

- Complete betting odds testing and documentation (Phase 6 - 15% remaining)
- Player comparison tools (Phase 6)
- Historical statistics and season archives (Phase 6)
- Advanced filtering with date ranges (Phase 7)
- Interactive charts and visualizations (Phase 8)
- Dark mode toggle (Phase 9)
- User preferences and favorites (Phase 10)
- And much more!

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Data sources: NFL official statistics (to be integrated)
- Inspiration: NFL fans and the need for accessible statistics
- Community: Open source contributors

## 📧 Contact

Questions or feedback? Open an issue on GitHub or reach out to the repository maintainer.

---

**Note**: This project is not affiliated with or endorsed by the National Football League (NFL). All team names, logos, and statistics are property of their respective owners.

## 🔗 Quick Links

- [Live Demo](https://yourusername.github.io/nfl-stats-dashboard/) (Update with your URL)
- [Report a Bug](https://github.com/yourusername/nfl-stats-dashboard/issues)
- [Request a Feature](https://github.com/yourusername/nfl-stats-dashboard/issues)
- [View Roadmap](TODO.md)
- [Agent Session Management](AGENT_SESSION_MANAGEMENT.md) - Guide for managing GitHub Copilot agent sessions
- [Quick Cleanup Guide](QUICK_START_AGENT_CLEANUP.md) - Fast fix for stuck agent sessions

---

Made with ❤️ for NFL fans everywhere
