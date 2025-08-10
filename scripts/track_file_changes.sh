#!/bin/bash

# Track file modifications for SESSION_RESUME.md
# Called by Claude Code PostToolUse hook after Edit/Write operations

TOOL_NAME="$1"
FILE_PATH="$2"
RESUME_FILE="/Users/bradleyfay/autodocs/planning/IMPLEMENTATION/SESSION_RESUME.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

# Only track significant files (not temp files or logs)
case "$FILE_PATH" in
  *.md|*.py|*.toml|*.json|*.yml|*.yaml|*.txt)
    # This is a file we want to track
    ;;
  */planning/IMPLEMENTATION/SESSION_RESUME.md)
    # Don't track changes to the resume file itself to avoid loops
    exit 0
    ;;
  *)
    # Skip other file types
    exit 0
    ;;
esac

# Extract just the filename from path
FILENAME=$(basename "$FILE_PATH")

# Update the "Files Recently Modified" section
TEMP_FILE="/tmp/track_changes_update.md"

# Find and update the "Files Recently Modified" section
awk -v file="$FILENAME" -v path="$FILE_PATH" -v timestamp="$TIMESTAMP" -v tool="$TOOL_NAME" '
/^## Files Recently Modified/ {
    print $0
    print "*Auto-updated with recently modified files*"
    print ""
    print "**" timestamp "** - Modified `" file "` using " tool
    print "  - Path: " path
    print ""
    # Skip until next section, then resume normal printing
    skip_until_next_section = 1
    next
}
skip_until_next_section && /^## / && !/^## Files Recently Modified/ {
    skip_until_next_section = 0
}
!skip_until_next_section { print }
' "$RESUME_FILE" > "$TEMP_FILE"

mv "$TEMP_FILE" "$RESUME_FILE"

echo "📝 Tracked file change: $FILENAME" >&2
