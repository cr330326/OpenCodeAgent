# Git Commit and Push

Commit all changes and push to GitHub remote repository.

## Instructions

1. Check current git status to see all changes
2. Stage all changes with `git add .`
3. Ask the user for a commit message (or suggest one based on the changes)
4. Create a commit with the message using conventional commit format (feat:, fix:, docs:, etc.)
5. Push to the remote repository

## Commands to Execute

```bash
# Check status
git status

# Stage all changes
git add .

# Commit (use the message provided by user or suggested)
git commit -m "<commit_message>"

# Push to remote
git push
```

## Notes

- Always use conventional commit prefixes: feat:, fix:, docs:, test:, refactor:, style:, chore:
- If there are no changes to commit, inform the user
- If push fails due to remote changes, suggest pulling first
