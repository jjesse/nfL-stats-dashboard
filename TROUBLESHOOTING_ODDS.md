# Troubleshooting Betting Odds - Quick Guide

## Issue: N/A Showing for Odds

### Quick Diagnosis
1. Check if `data/odds.json` exists
2. If not, the odds haven't been fetched yet
3. This is usually due to missing/invalid API key

### Common Issues & Solutions

#### 1. HTTP 403 Forbidden Error

**Symptoms**: Script shows "Failed to fetch odds: HTTP 403"

**Causes**:
- API key not activated (email verification required)
- Invalid or expired API key
- Account suspended or quota exceeded
- API key typed incorrectly

**Solutions**:
1. Log in to https://the-odds-api.com/account
2. Verify your email address if prompted
3. Check API key status (should show "Active")
4. Check remaining quota (should show X/500 requests)
5. Copy API key again (avoid copy/paste errors)
6. If quota = 0, wait for monthly reset or upgrade

#### 2. ODDS_API_KEY Not Found

**Symptoms**: Script shows "⚠ ODDS_API_KEY not found"

**Local Testing**:
```bash
# Set the key in your .env file
echo "ODDS_API_KEY=your_api_key_here" > .env

# Or run with inline environment variable
ODDS_API_KEY=your_key node scripts/fetch-data.js
```

**GitHub Actions**:
1. Go to repository Settings
2. Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `ODDS_API_KEY`
5. Value: Your API key from The Odds API
6. Click "Add secret"

#### 3. No Games Available

**Symptoms**: Odds fetch succeeds but shows "0 games"

**Causes**:
- NFL off-season (no upcoming games)
- Games already completed (odds removed)
- API doesn't have odds for future weeks yet

**Solutions**:
- Odds are usually available 3-7 days before games
- During playoffs/off-season, no odds may be available
- This is expected behavior, not an error

#### 4. Team Names Don't Match

**Symptoms**: Odds fetched but still showing N/A on schedule page

**Causes**:
- Team name mismatch between ESPN API and Odds API
- Different abbreviations or city names

**Solutions**:
- Check browser console for matching errors
- Verify team names in `data/odds.json` vs `data/schedule.json`
- May need to update `normalizeTeamName()` function in `app.js`

## Testing Locally

### Test 1: Verify API Key Works
```bash
# Test with curl
curl "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey=YOUR_KEY&regions=us&markets=h2h"
```

Expected response: JSON with games array (or empty array if no games)
Error response: 403 = invalid key, 429 = rate limited

### Test 2: Run Fetch Script
```bash
# With .env file
node scripts/fetch-data.js

# With inline key
ODDS_API_KEY=your_key node scripts/fetch-data.js
```

Expected output:
```
Fetching betting odds...
  ✓ Odds fetched for X games
  ℹ API requests used: Check response headers for remaining quota
```

### Test 3: Verify Data File
```bash
# Check if file created
ls -la data/odds.json

# View first few lines
cat data/odds.json | head -50

# Count games
cat data/odds.json | grep -c '"id"'
```

### Test 4: Test on Schedule Page
1. Open `schedule.html` in browser
2. Open Developer Console (F12)
3. Click "Show Betting Odds" button
4. Check console for errors
5. Look for "Using cached betting odds data" or "Loaded betting odds"

## GitHub Actions Testing

### Check Workflow Runs
1. Go to repository → Actions tab
2. Click "Update NFL Stats Data" workflow
3. View latest run
4. Check "Fetch NFL data" step for odds messages

### Manual Trigger
1. Go to Actions tab
2. Select "Update NFL Stats Data"
3. Click "Run workflow" button
4. Wait for completion (~1-2 minutes)
5. Check if `data/odds.json` was committed

### Check Secret Configuration
```bash
# Secrets aren't visible, but you can verify they're set
# Go to: Settings → Secrets and variables → Actions
# Should see: ODDS_API_KEY with "Updated X days ago"
```

## API Key Checklist

- [ ] Account created at The Odds API
- [ ] Email address verified
- [ ] API key copied correctly (no spaces)
- [ ] Key status shows "Active" in dashboard
- [ ] Quota shows remaining requests (X/500)
- [ ] `.env` file created locally (for testing)
- [ ] `.env` file in `.gitignore` (never commit!)
- [ ] GitHub Secret created in repository
- [ ] Secret name is exactly `ODDS_API_KEY`
- [ ] Workflow has been triggered at least once

## Still Not Working?

### Check These:

1. **Browser Cache**: Hard refresh (Ctrl+Shift+R)
2. **localStorage**: Clear cache in Developer Tools → Application → Local Storage
3. **File Permissions**: Ensure `data/` folder is writable
4. **Network Issues**: Check if The Odds API is accessible from your network
5. **Firewall/VPN**: Some networks block gambling-related APIs

### Get Help:

1. Check The Odds API documentation: https://the-odds-api.com/liveapi/guides/v4/
2. Contact The Odds API support: support@the-odds-api.com
3. Open GitHub issue with:
   - Error message (hide API key!)
   - Browser console logs
   - Whether local test worked
   - GitHub Actions logs (if applicable)

## Expected Behavior

✅ **Working Correctly**:
- Schedule page loads normally
- "Show Betting Odds" button appears
- Clicking button reveals 3 new columns
- Odds display with icons (📊 💰 🎯)
- Favorite teams show in red, underdogs in green
- "N/A" only for games without available odds

⚠️ **Not Working**:
- Button doesn't appear → Check if `schedule.html` has odds controls
- Button appears but odds columns empty → Check `data/odds.json` exists
- All odds show "N/A" → Team name matching issue or no data
- Error in console → Check browser console for specific error

## Quick Test Command

Run this to test everything at once:

```bash
# Test the full pipeline
cd /home/jjesse/github/nfl-stats-dashboard

# 1. Fetch with your key
ODDS_API_KEY=your_key node scripts/fetch-data.js

# 2. Check if file created
ls -la data/odds.json

# 3. Preview the data
cat data/odds.json | jq '.[0]' 2>/dev/null || cat data/odds.json | head -30

# 4. Start local server
python3 -m http.server 8000
# Then visit: http://localhost:8000/schedule.html
```

Good luck! 🍀
