# Quick Start: Cleaning Up Stuck Agent Sessions

## TL;DR - Fix It Now!

If you have multiple stuck agent sessions at "initializing pull request", follow these steps:

### Step 1: List All Open PRs

```bash
gh pr list --state open
```

Or visit: `https://github.com/YOUR_USERNAME/YOUR_REPO/pulls`

### Step 2: Close Each Stuck PR

**Using GitHub CLI:**
```bash
# Replace <NUMBER> with each PR number
gh pr close 2 --comment "Closing stuck session"
gh pr close 3 --comment "Closing stuck session"
gh pr close 4 --comment "Closing stuck session"
# ... continue for all stuck sessions
```

**Using GitHub Web Interface:**
1. Click on each PR
2. Scroll to bottom
3. Click "Close pull request"

### Step 3: Clean Up Branches (Optional but Recommended)

```bash
# List all copilot branches
git fetch --all
git branch -r | grep copilot/

# Delete each one
git push origin --delete copilot/branch-name-1
git push origin --delete copilot/branch-name-2
# ... continue for all branches
```

### Step 4: Start Fresh

Now you can create a new, single, clear request for the agent!

## Script to Close Multiple PRs

**⚠️ IMPORTANT**: Always verify PR numbers first!

```bash
# Step 1: List all PRs and note the numbers you want to close
gh pr list --state open

# Step 2: Only close the ones you've verified are stuck
# Replace 2,3,4,5,6,7,8 with your actual stuck PR numbers
for i in 2 3 4 5 6 7 8; do 
    gh pr close $i --comment "Closing stuck initialization session"
done
```

## Prevention Tips

1. ✅ **Wait 5-10 minutes** before deciding a session is stuck
2. ✅ **Only create one session at a time** - don't spam requests
3. ✅ **Use clear, specific prompts** - helps the agent start quickly
4. ✅ **Monitor new sessions** - check after a few minutes to ensure progress

## When to Use This Guide

Use this guide if:
- ❌ You see multiple "initializing pull request" messages
- ❌ Agent hasn't started working after 10+ minutes
- ❌ You accidentally created many duplicate sessions
- ❌ You want to start over with a clean slate

## Need More Details?

See the full guide: [AGENT_SESSION_MANAGEMENT.md](AGENT_SESSION_MANAGEMENT.md)

---

**Quick Help**: Having trouble? Check that you have:
- GitHub CLI installed: `gh --version`
- Authenticated: `gh auth status`
- Correct permissions on the repository
