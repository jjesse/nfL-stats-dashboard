# Automation Setup Guide

This document explains how the automated data updates work and how to configure them.

## Overview

The NFL Stats Dashboard uses GitHub Actions to automatically fetch and update NFL statistics data every week. This ensures the dashboard always displays current information without manual intervention.

## Components

### 1. GitHub Actions Workflow

**File**: `.github/workflows/update-data.yml`

The workflow is configured to run on three triggers:

```yaml
on:
  schedule:
    - cron: '0 11 * * 2'  # Every Tuesday at 6 AM EST (11 AM UTC)
  workflow_dispatch:       # Manual trigger
  push:
    branches: [ main ]
    paths:
      - 'scripts/fetch-data.js'
      - '.github/workflows/update-data.yml'
```

**Schedule Explanation**:
- Runs every **Tuesday at 6 AM EST**
- Captures all NFL games from the previous week:
  - Thursday Night Football
  - Sunday games (early and late)
  - Sunday Night Football
  - Monday Night Football

**Workflow Steps**:
1. Checkout repository
2. Setup Node.js v18
3. Run data fetching script
4. Check for data changes
5. Commit and push updated JSON files (if changed)

### 2. Data Fetching Script

**File**: `scripts/fetch-data.js`

A Node.js script that fetches NFL data from ESPN's public API.

**Data Sources**:
- Schedule: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
- Teams: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{id}`
- Standings: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/standings`
- Player Leaders: `https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{year}/types/2/leaders`

**Data Collected**:
- **Schedule** (weeks 14-18): Game matchups, scores, venues, dates/times
- **Standings**: Division-by-division standings with win/loss records
- **Team Stats**: All 32 NFL teams with comprehensive statistics
- **Player Stats**: Top 10 leaders in QB, Receiving, and Rushing categories

**Output Files** (saved to `data/` directory):
- `schedule.json` - Game schedule data
- `standings.json` - Division standings
- `team-stats.json` - Team statistics
- `player-stats.json` - Player leader boards
- `metadata.json` - Update timestamp and metadata

### 3. Permissions Configuration

The workflow requires write permissions to commit updated data:

```yaml
permissions:
  contents: write
```

This allows GitHub Actions Bot to:
- Commit updated JSON files
- Push changes back to the repository

## Manual Trigger

### Via GitHub Interface

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. Select **Update NFL Stats Data** workflow
4. Click **Run workflow** button
5. Select branch (usually `main`)
6. Click **Run workflow**

### Via Local Script

```bash
# Navigate to project directory
cd nfl-stats-dashboard

# Run the fetch script
node scripts/fetch-data.js

# Review changes
git status
git diff data/

# Commit and push
git add data/
git commit -m "chore: Update NFL stats data"
git push origin main
```

## Customization

### Change Update Schedule

Edit `.github/workflows/update-data.yml`:

```yaml
schedule:
  # Examples:
  - cron: '0 11 * * *'     # Daily at 6 AM EST
  - cron: '0 11 * * 0,2'   # Sunday and Tuesday at 6 AM EST
  - cron: '0 */6 * * *'    # Every 6 hours
  - cron: '0 11 * * 1-5'   # Weekdays at 6 AM EST
```

**Cron Format**: `minute hour day month weekday`
- `0 11 * * 2` = At 11:00 AM UTC (6:00 AM EST) on Tuesday
- `*` = any value
- `*/6` = every 6 (hours, minutes, etc.)
- `2` = Tuesday (0=Sunday, 1=Monday, ..., 6=Saturday)

### Modify Data Sources

Edit `scripts/fetch-data.js`:

```javascript
// Add more weeks to schedule
const WEEKS = [14, 15, 16, 17, 18, 19]; // Include week 19 (playoffs)

// Fetch more player stats
const LEADER_LIMIT = 20; // Get top 20 instead of top 10

// Add new API endpoints
async function fetchDefensiveStats() {
  // Implement defensive player stats
}
```

### Add Notification

To receive notifications when data updates fail:

```yaml
- name: Notify on failure
  if: failure()
  uses: actions/github-script@v6
  with:
    script: |
      github.rest.issues.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: 'Data Update Failed',
        body: 'The automated NFL stats update failed. Check the workflow logs.'
      })
```

## Monitoring

### Check Workflow Status

- **Badge**: The README includes a status badge showing the last run
- **Actions Tab**: View detailed logs of all workflow runs
- **Commit History**: See data update commits with timestamps

### View Logs

1. Go to **Actions** tab
2. Click on a workflow run
3. Click on **update-data** job
4. Expand steps to see detailed output

### Troubleshooting

**Common Issues**:

1. **Permission Denied (403 Error)**
   - Ensure `permissions: contents: write` is set
   - Check repository settings → Actions → General → Workflow permissions

2. **API Rate Limiting**
   - ESPN API may throttle excessive requests
   - The script includes delays between requests
   - Reduce frequency if needed

3. **SSL Certificate Errors**
   - Script includes `NODE_TLS_REJECT_UNAUTHORIZED = '0'` to handle certificate issues
   - This is safe for public APIs with valid certificates

4. **No Changes Detected**
   - Normal if stats haven't changed since last run
   - Check logs for "No data changes detected"

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions (Weekly)                  │
│                                                              │
│  1. Trigger: Tuesday 6 AM EST                               │
│  2. Run: node scripts/fetch-data.js                         │
│  3. Save: data/*.json files                                 │
│  4. Commit & Push: Updated files to repo                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                         │
│                                                              │
│  - data/schedule.json                                       │
│  - data/standings.json                                      │
│  - data/team-stats.json                                     │
│  - data/player-stats.json                                   │
│  - data/metadata.json                                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Pages (Live)                      │
│                                                              │
│  1. User visits: https://jjesse.github.io/nfl-stats-dash... │
│  2. Browser loads: HTML/CSS/JS                              │
│  3. JavaScript fetches: ESPN API (live data)                │
│  4. Cache: localStorage (5 min)                             │
│  5. Fallback: data/*.json files (if API fails)              │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices

1. **Test Locally First**
   - Run `node scripts/fetch-data.js` before pushing changes
   - Verify JSON files are correctly formatted

2. **Review Changes**
   - Check diffs before committing data updates
   - Ensure no unexpected data loss

3. **Monitor Performance**
   - Watch workflow execution times
   - Optimize script if fetching takes too long

4. **Keep Dependencies Updated**
   - Node.js version in workflow
   - Any npm packages (if added in future)

5. **Document Changes**
   - Update this file when modifying automation
   - Add comments to workflow and scripts

## Future Enhancements

Potential improvements to the automation system:

- [ ] Add error notifications (email, Slack, Discord)
- [ ] Implement data validation checks
- [ ] Create data backup/archive system
- [ ] Add performance metrics and logging
- [ ] Support multiple NFL seasons
- [ ] Implement incremental updates (only changed data)
- [ ] Add data quality checks before committing
- [ ] Create dashboard for monitoring automation health

---

**Last Updated**: December 7, 2025

**Maintainer**: See repository contributors
