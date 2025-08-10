#!/bin/bash

# Auto-update SESSION_RESUME.md at session end
# Called by Claude Code Stop hook

RESUME_FILE="/Users/bradleyfay/autodocs/planning/IMPLEMENTATION/SESSION_RESUME.md"
TEMP_FILE="/tmp/session_end_update.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

# Get current state
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
RECENT_COMMITS=$(git log --oneline -3 2>/dev/null || echo "No recent commits")
MODIFIED_FILES=$(git status --porcelain 2>/dev/null | head -10)

# Create session end summary
SESSION_SUMMARY=$(cat << EOF

### Session Ended: $TIMESTAMP
**Final Branch**: $CURRENT_BRANCH
**Files with Changes**:
$(echo "$MODIFIED_FILES" | sed 's/^/  - /')

**Recent Commits**:
$(echo "$RECENT_COMMITS" | sed 's/^/  - /')

**Context for Next Session**:
- Check git status for any uncommitted work
- Review recent commits above for what was accomplished
- Continue with tasks noted in "Next Actions" section

EOF
)

# Find the "Session-Specific Notes" section and add the summary
awk -v summary="$SESSION_SUMMARY" '
/^## Session-Specific Notes/ {
    print $0
    print summary
    skip_until_next_section = 1
    next
}
skip_until_next_section && /^## / && !/^## Session-Specific Notes/ {
    skip_until_next_section = 0
}
!skip_until_next_section { print }
' "$RESUME_FILE" > "$TEMP_FILE"

mv "$TEMP_FILE" "$RESUME_FILE"

echo "📝 SESSION_RESUME.md updated for session end" >&2
