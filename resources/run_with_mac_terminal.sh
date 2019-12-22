#!/bin/bash
osascript - "$@" <<EOF
on run argv
tell application "Terminal"
    activate
    do script "" & (item 1 of argv)
end tell
end run
EOF