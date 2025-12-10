# Managing GitHub Copilot Agent Sessions

## Overview

GitHub Copilot coding agent creates pull request branches to work on issues and tasks. Sometimes these agent sessions can get stuck at the "initializing pull request" stage. This guide explains how to identify, manage, and resolve these stuck sessions.

## What Are Agent Sessions?

When you ask GitHub Copilot to work on an issue or task, it creates:
- A new branch (typically named `copilot/...`)
- A draft pull request
- A workspace to make changes

These are called "agent sessions" and represent active work by the Copilot agent.

## Identifying Stuck Sessions

### How to Check for Stuck Agent Sessions

1. **Via GitHub Web Interface:**
   - Go to your repository on GitHub
   - Click on the "Pull requests" tab
   - Look for draft PRs with titles like "[WIP] ..." or "Initializing..."
   - Check if they're stuck without commits or activity

2. **Via GitHub CLI:**
   ```bash
   gh pr list --state open --json number,title,isDraft,author
   ```

3. **Via Git Command Line:**
   ```bash
   git branch -r | grep copilot/
   ```

### Signs of a Stuck Session

- Pull request shows "initializing pull request" for extended period (>5 minutes)
- No commits after initial branch creation
- Agent not responding or making progress
- Multiple sessions created for the same task

## How to Close Stuck Agent Sessions

### Method 1: Close the Pull Request (Recommended)

**Via GitHub Web Interface:**
1. Navigate to the stuck pull request
2. Scroll to the bottom of the PR page
3. Click "Close pull request" button
4. Optionally, add a comment explaining why (e.g., "Session stuck, restarting")

**Via GitHub CLI:**
```bash
# List PRs to find the number
gh pr list

# Close a specific PR
gh pr close <PR_NUMBER>

# Close with a comment
gh pr close <PR_NUMBER> --comment "Closing stuck agent session"
```

### Method 2: Delete the Branch (After Closing PR)

**Only do this AFTER closing the pull request!**

```bash
# Delete remote branch
git push origin --delete copilot/<branch-name>

# Delete local branch (if you have it)
git branch -D copilot/<branch-name>
```

### Method 3: Cancel from GitHub Actions (If Running)

If the agent session is running as a GitHub Action:
1. Go to the "Actions" tab in your repository
2. Find the running workflow for the stuck session
3. Click on the workflow
4. Click "Cancel workflow" button

## How to Work on Existing Agent PRs

If you want to continue work on an existing agent PR (not stuck, just incomplete):

### Option 1: Let the Agent Continue

1. Go to the pull request
2. Add a comment with additional instructions: `@copilot <your instructions>`
3. The agent should respond and continue working

### Option 2: Take Over Manually

If you want to make changes yourself:

```bash
# Fetch the latest changes
git fetch origin

# Check out the agent's branch
git checkout copilot/<branch-name>

# Make your changes
# ... edit files ...

# Commit and push
git add .
git commit -m "Your changes"
git push origin copilot/<branch-name>
```

### Option 3: Start Fresh

If the session is too broken:
1. Close the existing PR
2. Delete the branch
3. Create a new issue or prompt for the agent to start fresh

## Best Practices

### Preventing Stuck Sessions

1. **Be specific in your prompts**: Clear, focused requests help the agent work efficiently
2. **One task at a time**: Avoid asking for multiple unrelated changes in one prompt
3. **Monitor progress**: Check back within a few minutes to ensure the agent started working
4. **Wait before retrying**: If a session seems stuck, wait 5-10 minutes before creating a new one

### Managing Multiple Sessions

1. **Limit concurrent sessions**: Try to keep only 1-2 active agent sessions at a time
2. **Use descriptive names**: If manually creating branches, use clear names
3. **Clean up completed work**: Close and delete branches for merged or abandoned PRs
4. **Track your requests**: Keep notes of what you've asked the agent to do

### Recovery Steps for 7 Stuck Sessions

If you currently have 7 stuck sessions (like in your case), here's what to do:

1. **Identify all stuck PRs:**
   ```bash
   gh pr list --state open
   ```

2. **Close all stuck sessions:**
   ```bash
   # For each stuck PR, run:
   gh pr close <PR_NUMBER> --comment "Closing stuck initialization session"
   ```

3. **Clean up branches (optional):**
   ```bash
   # List all copilot branches
   git branch -r | grep copilot/
   
   # Delete them one by one
   git push origin --delete copilot/<branch-name>
   ```

4. **Start fresh:**
   - Create a new, single, clear request for the agent
   - Monitor it to ensure it starts working properly

## Common Issues and Solutions

### Issue: "Agent not responding to my PR comments"
**Solution:** The agent may have timed out. Close the PR and start a new session.

### Issue: "Multiple PRs created for the same task"
**Solution:** Close all but the most recent one. The agent may have been retrying.

### Issue: "Can't delete branch - PR is still open"
**Solution:** Close the PR first, then delete the branch.

### Issue: "Agent made changes I don't want"
**Solution:** 
- Checkout the branch
- Use `git revert <commit-hash>` to undo specific commits
- Or close the PR and start fresh

### Issue: "Session stuck at 'initializing' for hours"
**Solution:** This is definitely stuck. Close it and create a new request.

## FAQ

**Q: How long should I wait before considering a session stuck?**  
A: Usually 5-10 minutes is enough. If there's no activity after that, it's likely stuck.

**Q: Will closing a PR lose my work?**  
A: The branch and commits remain unless you explicitly delete them. You can always reopen or create a new PR from the same branch.

**Q: Can I have multiple agent sessions working simultaneously?**  
A: Technically yes, but it's not recommended. Stick to 1-2 at a time for best results.

**Q: What causes sessions to get stuck?**  
A: Common causes include:
- Service timeouts or outages
- Unclear or conflicting instructions
- Repository access issues
- Too many concurrent requests

**Q: Should I delete the branches after closing PRs?**  
A: It's a good practice for cleanup, but not required. Branches don't hurt anything if left around.

**Q: Can I restart a closed agent session?**  
A: Not directly. You'll need to create a new request with similar instructions.

## Getting Help

If you continue to have issues with stuck agent sessions:

1. **Check GitHub Status**: Visit [githubstatus.com](https://www.githubstatus.com/) for any ongoing incidents
2. **Repository Settings**: Ensure GitHub Actions and Copilot have proper permissions
3. **Create an Issue**: Document the problem and ask for help
4. **Contact Support**: For persistent issues, reach out to GitHub Support

## Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Managing Pull Requests](https://docs.github.com/en/pull-requests)

---

**Note**: This guide is maintained as part of the repository documentation. Check for updates in the repository.
