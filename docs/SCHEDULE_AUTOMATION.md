# NFL Schedule Automation Documentation

## Overview

This document describes the automated NFL schedule update system implemented in the NFL-stats-dashboard.

## Current Status (Week 14, December 2025)

The NFL schedule system is now fully automated and will update automatically throughout the season.

## Schedule Data Source

The schedule processor (`src/data-processors/schedule-processor.py`) fetches live NFL schedule and game results from:
- **Pro Football Reference**: https://www.pro-football-reference.com/years/{SEASON}/games.htm

## Season Detection Logic

The system automatically detects the current NFL season based on the date:

- **January - July**: Returns previous year's season (e.g., Feb 2025 → 2024 season)
- **August - December**: Returns current year's season (e.g., Dec 2025 → 2025 season)

This matches the NFL season structure:
- Season starts in September
- Regular season ends in January
- Playoffs run through February

### Example:
- Date: December 6, 2025 → **2025 NFL Season** (Week 14)
- Date: February 15, 2025 → **2024 NFL Season** (Playoffs/Super Bowl)

## Automated Updates

The schedule is automatically updated by **multiple GitHub Actions workflows**:

### 1. **update-nfl-data-with-accuracy.yml**
- **Schedule**: Every 6 hours (`0 */6 * * *`)
- **Includes**: Schedule processor, player stats, team stats, awards predictions
- **Most comprehensive workflow**

### 2. **nfl-stats-simple.yml**
- **Schedule**: Every 6 hours (`0 */6 * * *`)
- **Includes**: Schedule processor, player stats, team stats, accuracy tracking

### 3. **update-stats.yml**
- **Schedule**: Every 6 hours (`0 */6 * * *`)
- **Includes**: Schedule processor, player stats, team stats, awards

### 4. **update-all.yml**
- **Schedule**: Daily at 8 AM UTC (`0 8 * * *`)
- **Includes**: Schedule processor, player stats, team stats

## Output Files

The schedule processor generates:

1. **docs/schedule_results.csv** - Current season schedule with columns:
   - Week, Date, Time, Away_Team, Away_Score, Home_Team, Home_Score, Winner, Status

2. **docs/schedule_overview.png** - Visualization showing:
   - Games per week
   - Game status distribution
   - Games by day of week
   - Total points distribution

3. **docs/last_updated_schedule.txt** - Timestamp of last update

4. **archive/schedule_results_{timestamp}.csv** - Historical archive

## Dashboard Integration

The schedule data is displayed on the main dashboard (`docs/index.html`) in the **📅 Schedule Tab**:

- **Season Progress**: Shows completed games, remaining games, and current week
- **Week Selector**: Filter games by specific week
- **Team Filter**: View all games for a specific team
- **Status Filter**: Show only completed or upcoming games
- **Weekly View**: Card-based display of games for selected week
- **Complete Table**: Full season schedule with all details

## Manual Updates

If you need to manually update the schedule:

```bash
python src/data-processors/schedule-processor.py
```

This will:
1. Fetch the latest schedule data from Pro Football Reference
2. Process and clean the data
3. Generate visualizations
4. Save to docs/ and archive/ directories

## Troubleshooting

### "Could not load schedule data" Error

**Solution**: Run the schedule processor manually:
```bash
python src/data-processors/schedule-processor.py
```

### Schedule shows wrong season

**Check**: 
1. Verify system date/time is correct
2. Review season detection logic in `schedule-processor.py` line 54-70
3. Season should match: Jan-Jul → Previous year, Aug-Dec → Current year

### Missing weeks in schedule

**Cause**: The schedule processor fetches all available data from Pro Football Reference
**Solution**: 
1. Wait for the next automated update (runs every 6 hours)
2. Manually trigger the workflow in GitHub Actions
3. Run the processor manually if needed

## Testing

Tests for season calculation are in `tests/test_data_processors.py`:

```bash
# Run season calculation tests
python -m pytest tests/test_data_processors.py::TestNFLSeasonCalculation -v
```

## Future Enhancements

Potential improvements:
- Add week number validation
- Include playoff bracket generation
- Add bye week tracking
- Include weather data for games
- Add spread/betting line information
- Include TV network and time zone information
