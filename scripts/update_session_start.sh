#!/bin/bash

# Auto-update SESSION_RESUME.md at session start
# Called by Claude Code SessionStart hook

RESUME_FILE="/Users/bradleyfay/autodocs/planning/IMPLEMENTATION/SESSION_RESUME.md"
TEMP_FILE="/tmp/session_resume_update.md"

# Get current state
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
GIT_STATUS=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
LAST_COMMIT=$(git log --oneline -1 2>/dev/null || echo "No commits")
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

# Update the session status section
sed '/## Current Session Status/,/## What You Were Working On/ {
  /## Current Session Status/!{
    /## What You Were Working On/!d
  }
}' "$RESUME_FILE" > "$TEMP_FILE"

# Insert updated status
cat >> "$TEMP_FILE" << EOF
## Current Session Status
**Last Updated**: $TIMESTAMP (Auto-updated by hook)
**Current Branch**: $CURRENT_BRANCH
**Git Status**: $GIT_STATUS files changed
**Last Commit**: $LAST_COMMIT

## What You Were Working On
EOF

# Append the rest of the file
sed -n '/## What You Were Working On/,$ p' "$RESUME_FILE" | tail -n +2 >> "$TEMP_FILE"

# Replace original file
mv "$TEMP_FILE" "$RESUME_FILE"

echo "📝 SESSION_RESUME.md updated for session start" >&2
