#!/bin/bash
# Fetches citation/h-index/publication data from Google Scholar and pushes
# it to GitHub. Run manually, or scheduled locally via launchd (see
# com.rmolania.updatescholar.plist) since Google Scholar blocks requests
# from GitHub Actions' data-center IPs but not from a home network.
set -euo pipefail

REPO_DIR="/Users/molania.r/Documents/AaiProjects/PersonalWebSite"
cd "$REPO_DIR"

"$REPO_DIR/.venv/bin/python3" fetch_scholar.py

if [ -n "$(git status --porcelain publications.json scholar-stats.json)" ]; then
  git add publications.json scholar-stats.json
  git commit -m "Update publications and citation stats from Google Scholar"
  git push origin main
  echo "Pushed updated publications/stats."
else
  echo "No changes."
fi
