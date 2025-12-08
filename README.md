# NFL Stats Dashboard

[![Update NFL Stats Data](https://github.com/jjesse/nfl-stats-dashboard/actions/workflows/update-data.yml/badge.svg)](https://github.com/jjesse/nfl-stats-dashboard/actions/workflows/update-data.yml)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://jjesse.github.io/nfl-stats-dashboard/)

A modern, responsive web dashboard for viewing NFL statistics, schedules, and player performance data. Built with vanilla HTML, CSS, and JavaScript, designed to be hosted on GitHub Pages with automated data updates via GitHub Actions.

## 🏈 Project Overview

The NFL Stats Dashboard provides an easy-to-navigate interface for accessing comprehensive NFL data including:

- **Schedule**: View upcoming games with team records and venue information (Weeks 14-18)
- **Standings**: NFL standings organized by division and conference
- **Team Statistics**: Compare team performance across the league
- **Player Leaders**: Track top performers in passing, receiving, and rushing categories
- **Automated Updates**: Data refreshes automatically every Tuesday at 6 AM EST via GitHub Actions

## 📋 Features

- ✅ Clean, modern design optimized for all devices
- ✅ Responsive layout for desktop, tablet, and mobile
- ✅ Easy navigation with dropdown menus
- ✅ Comprehensive data tables with click-to-sort functionality
- ✅ Live data from ESPN Public API
- ✅ Automated weekly data updates via GitHub Actions
- ✅ localStorage caching for improved performance
- ✅ Well-commented, maintainable codebase

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
├── about.html              # About page with project info
├── styles.css              # Main stylesheet with responsive design
├── app.js                  # JavaScript for data handling and interactivity
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
│   └── metadata.json
├── README.md               # This file
├── TODO.md                 # Development roadmap
├── TESTING.md              # Testing guide and instructions
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

- **HTML5**: Semantic markup for accessibility
- **CSS3**: Modern styling with CSS variables and flexbox/grid
- **JavaScript (ES6+)**: Dynamic content loading and interactivity
- **GitHub Pages**: Free hosting for static websites
- **GitHub Actions**: Automated data updates (planned)

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

## 📝 Future Enhancements

See [TODO.md](TODO.md) for the complete development roadmap. Key upcoming features:

- Real-time data integration via APIs
- GitHub Actions for automated updates
- Enhanced sorting and filtering
- Player comparison tools
- Historical statistics
- Dark mode toggle
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

---

Made with ❤️ for NFL fans everywhere
