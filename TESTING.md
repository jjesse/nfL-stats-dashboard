# API Integration Testing Guide

This document provides testing instructions for the NFL Stats Dashboard API integration.

## Overview

The dashboard now uses ESPN's public API to fetch real-time NFL data. This guide will help you test and verify the integration.

## Testing Checklist

### ✅ Basic Functionality Tests

1. **Home Page**
   - [ ] Page loads without errors
   - [ ] Navigation menu works
   - [ ] All links are functional

2. **Schedule Page** (`schedule.html`)
   - [ ] Table loads with "Loading schedule data..." message initially
   - [ ] Real game data populates after loading
   - [ ] Displays: Date, Time, Teams, Records, Venue
   - [ ] Check browser console for any errors

3. **Team Stats Page** (`team-stats.html`)
   - [ ] Table loads with loading indicator
   - [ ] All 32 NFL teams displayed
   - [ ] Sorted by win percentage
   - [ ] Data includes: Wins, Losses, Points, Differential

4. **Quarterback Leaders** (`qb-leaders.html`)
   - [ ] Top 10 QBs displayed
   - [ ] Stats include: Yards, TDs, Completions, Rating
   - [ ] Player names and teams are correct

5. **Receiver Leaders** (`receiver-leaders.html`)
   - [ ] Top 10 receivers displayed
   - [ ] Stats include: Receptions, Yards, TDs
   - [ ] Data is current

6. **Rushing Leaders** (`rushing-leaders.html`)
   - [ ] Top 10 rushers displayed
   - [ ] Stats include: Attempts, Yards, TDs, YPG
   - [ ] Data is accurate

### ✅ Caching Tests

1. **First Load**
   - Open browser DevTools (F12)
   - Go to Network tab
   - Load a statistics page
   - Verify API calls are made to ESPN

2. **Cached Load**
   - Refresh the same page within 5 minutes
   - Check console for "Using cached data" messages
   - Verify no new API calls in Network tab

3. **Cache Expiration**
   - Wait 5+ minutes
   - Refresh the page
   - New API calls should be made

4. **Clear Cache**
   - Open browser console
   - Type: `NFLAPI.clearCache()`
   - Refresh page
   - New data should be fetched

### ✅ Error Handling Tests

1. **Network Disconnection**
   - Open DevTools → Network tab
   - Set throttling to "Offline"
   - Try loading a page
   - Should show error message in table

2. **API Timeout**
   - Verify timeout error message appears if API is slow
   - Error should be user-friendly

3. **No Data Available**
   - Check behavior when API returns empty data
   - Should show "No data available" message

### ✅ Cross-Browser Testing

Test on multiple browsers:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (if on Mac)
- [ ] Edge

### ✅ Responsive Design Testing

Test on different screen sizes:
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

## How to Test Locally

1. **Start Local Server**
   ```bash
   cd /home/jjesse/github/nfl-stats-dashboard
   python3 -m http.server 8000
   ```

2. **Open in Browser**
   Navigate to: `http://localhost:8000`

3. **Open DevTools**
   - Press F12 or right-click → Inspect
   - Check Console tab for any errors
   - Check Network tab for API calls

## Common Issues and Solutions

### Issue: CORS Error

**Symptom**: Console shows "CORS policy" error

**Solution**: 
- The dashboard is designed to work from a web server, not file:// protocol
- Make sure you're accessing via http://localhost
- If deploying to GitHub Pages, CORS should work automatically
- For local development with strict CORS, uncomment the CORS proxy in `api.js`:
  ```javascript
  corsProxy: 'https://cors-anywhere.herokuapp.com/'
  ```

### Issue: No Data Loading

**Symptom**: Tables show "Loading..." forever

**Solution**:
1. Check browser console for errors
2. Verify internet connection
3. Check if ESPN API is accessible: https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard
4. Try clearing cache: `NFLAPI.clearCache()`

### Issue: Incorrect Data Format

**Symptom**: Data displays but looks wrong

**Solution**:
1. ESPN API structure may have changed
2. Check `api.js` data mapping functions
3. Update field names if ESPN changed their response format

### Issue: Slow Loading

**Symptom**: Takes long time to load data

**Solution**:
1. First load will be slower (fetching from API)
2. Subsequent loads should be fast (using cache)
3. Check network speed
4. Consider increasing cache duration in `api.js`

## API Endpoints Used

The dashboard uses these ESPN API endpoints:

1. **Scoreboard/Schedule**
   ```
   https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard
   ```

2. **Team Standings**
   ```
   https://site.api.espn.com/apis/site/v2/sports/football/nfl/standings
   ```

3. **Player Leaders**
   ```
   https://site.api.espn.com/apis/site/v2/sports/football/nfl/leaders
   ```

## Manual API Testing

Test API endpoints directly in browser:

1. **View Schedule Data**
   ```
   https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=2024&seasontype=2&week=14
   ```

2. **View Standings**
   ```
   https://site.api.espn.com/apis/site/v2/sports/football/nfl/standings
   ```

3. **View Leaders**
   ```
   https://site.api.espn.com/apis/site/v2/sports/football/nfl/leaders
   ```

## Performance Benchmarks

Expected load times:

- **First Load (no cache)**: 1-3 seconds
- **Cached Load**: < 100ms
- **API Response Time**: 500ms - 2s
- **Page Render Time**: < 500ms

## Cache Storage

Data is stored in browser's `localStorage`:

- **Cache Duration**: 5 minutes
- **Storage Keys**: 
  - `schedule_[week]_[year]`
  - `team_stats`
  - `qb_stats`
  - `receiver_stats`
  - `rushing_stats`

**View Cache**:
```javascript
// In browser console
Object.keys(localStorage).filter(key => key.includes('stats') || key.includes('schedule'))
```

## Debugging Commands

Open browser console and try:

```javascript
// Test schedule fetch
NFLAPI.getSchedule().then(data => console.log(data));

// Test team stats
NFLAPI.getTeamStats().then(data => console.log(data));

// Test QB stats
NFLAPI.getQBStats().then(data => console.log(data));

// Clear all cached data
NFLAPI.clearCache();

// Check cache duration
// Edit api.js and change CACHE_DURATION value
```

## Next Steps After Testing

Once testing is complete:

1. ✅ Mark Phase 2 as complete in TODO.md
2. 📝 Document any issues found
3. 🐛 Fix bugs if discovered
4. 🚀 Move to Phase 3: GitHub Actions automation
5. 📊 Consider adding loading animations (Phase 4)

## Reporting Issues

If you find bugs during testing:

1. Note the specific page and action
2. Copy console error messages
3. Include browser and OS information
4. Take screenshots if applicable
5. Document steps to reproduce

---

**Testing Status**: Ready for testing
**Last Updated**: December 7, 2025
**API Version**: ESPN Public API (unofficial)
