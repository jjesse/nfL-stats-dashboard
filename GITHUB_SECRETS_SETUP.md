# GitHub Secrets Setup Guide

This guide explains how to configure the GitHub Secret required for betting odds integration.

## Required Secret: ODDS_API_KEY

The betting odds feature requires an API key from [The Odds API](https://the-odds-api.com/).

### Why Use GitHub Secrets?

- **Security**: API keys are never exposed in code or browser
- **GitHub Pages Compatible**: Works with static hosting by pre-fetching data
- **Free Tier Friendly**: Automated weekly updates stay within 500 requests/month limit

### Setup Instructions

1. **Navigate to Repository Settings**
   - Go to your GitHub repository
   - Click **Settings** tab
   - In the left sidebar, click **Secrets and variables** → **Actions**

2. **Create New Secret**
   - Click **New repository secret** button
   - Set the following values:
     - **Name**: `ODDS_API_KEY`
     - **Secret**: Your API key from The Odds API
   - Click **Add secret**

3. **Verify Setup**
   - The GitHub Actions workflow automatically runs on:
     - Every Tuesday at 6 AM EST (11 AM UTC)
     - Manual trigger via Actions tab
     - Push to main branch
   - Check the Actions tab to see if the workflow runs successfully
   - Look for the "Fetch NFL data" step to confirm odds are fetched

## API Key Information

**Current API Provider**: The Odds API  
**Free Tier**: 500 requests/month  
**Usage Pattern**: ~4 requests/month (weekly updates)  
**Endpoint**: `https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/`

**Markets Fetched**:
- `h2h` - Moneyline (head-to-head)
- `spreads` - Point spreads
- `totals` - Over/under totals

**Odds Format**: American (e.g., -110, +150)

## How It Works

1. **GitHub Actions** runs the workflow on schedule
2. **Workflow** passes `ODDS_API_KEY` from Secrets to the script
3. **Script** (`scripts/fetch-data.js`) fetches odds from The Odds API
4. **Data** is saved to `data/odds.json` 
5. **Changes** are committed back to the repository
6. **GitHub Pages** serves the updated JSON file
7. **Schedule page** reads odds from the static JSON file

## Testing Locally

If you want to test odds fetching locally:

1. Create a `.env` file in the project root:
   ```bash
   ODDS_API_KEY=your_api_key_here
   ```

2. Run the fetch script:
   ```bash
   node scripts/fetch-data.js
   ```

3. Check `data/odds.json` for results

**Important**: Never commit your `.env` file! It's already in `.gitignore`.

## Troubleshooting

### Workflow shows "ODDS_API_KEY not found"
- Secret name must be exactly `ODDS_API_KEY` (case-sensitive)
- Verify the secret is created in the correct repository
- Check that the workflow has access to repository secrets

### No odds data in data/odds.json
- Check GitHub Actions logs for errors
- Verify API key is valid at https://the-odds-api.com/
- Check API quota hasn't been exceeded
- Ensure NFL season is active (API returns empty during off-season)

### API quota exceeded
- Free tier: 500 requests/month
- Current usage: ~4 requests/month (weekly updates)
- If exceeded, consider:
  - Reducing update frequency
  - Upgrading to paid tier
  - Using cached data until quota resets

## Security Best Practices

✅ **DO**:
- Store API key only in GitHub Secrets
- Use `.env` for local development only
- Keep `.env` in `.gitignore`
- Rotate API keys periodically

❌ **DON'T**:
- Commit API keys to version control
- Share API keys in issues/PRs
- Include keys in client-side JavaScript
- Use keys in URLs (use env variables in backend only)

## API Key Rotation

To update or rotate your API key:

1. Get new API key from The Odds API
2. Go to repository Settings → Secrets and variables → Actions
3. Click **ODDS_API_KEY** to edit
4. Update the secret value
5. Save changes
6. Next workflow run will use the new key

## Support

- **The Odds API Documentation**: https://the-odds-api.com/liveapi/guides/v4/
- **GitHub Secrets Documentation**: https://docs.github.com/en/actions/security-guides/encrypted-secrets
- **Project Issues**: https://github.com/[your-username]/nfl-stats-dashboard/issues
