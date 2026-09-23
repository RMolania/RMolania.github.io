"""Fetch citation count and h-index from a Google Scholar profile
and write them to scholar-stats.json for the website to load.

The publication list is maintained by hand in index.html and is not
touched by this script.

Run by .github/workflows/update-publications.yml on a daily schedule.
"""
import json
import sys

from scholarly import scholarly

SCHOLAR_ID = "u-bNAS8AAAAJ"   # Ramyar Molania
STATS_FILE = "scholar-stats.json"


def main() -> int:
    try:
        author = scholarly.search_author_id(SCHOLAR_ID)
        author = scholarly.fill(author, sections=["indices"])
    except Exception as exc:  # Scholar occasionally rate-limits; keep old file
        print(f"Could not reach Google Scholar: {exc}", file=sys.stderr)
        return 1

    citations = author.get("citedby")
    hindex = author.get("hindex")
    if citations is None or hindex is None:
        print("Could not parse citation stats; keeping existing file.", file=sys.stderr)
        return 1

    with open(STATS_FILE, "w", encoding="utf-8") as fh:
        json.dump({"citations": citations, "hindex": hindex}, fh, indent=2)
    print(f"Wrote stats to {STATS_FILE}: {citations} citations, h-index {hindex}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
