"""Fetch the latest publications from a Google Scholar profile
and write them to publications.json for the website to load.

Run by .github/workflows/update-publications.yml on a daily schedule.
"""
import json
import re
import sys

from scholarly import scholarly

SCHOLAR_ID = "u-bNAS8AAAAJ"   # Ramyar Molania
MAX_PUBS = 15                  # how many recent papers to show on the site
OUT_FILE = "publications.json"


def short_authors(authors: str) -> str:
    """First author, '…', you, '…', last author -- keeps long consortium lists tidy."""
    names = [a.strip() for a in authors.split(",") if a.strip()]
    if len(names) <= 4:
        return ", ".join(names)
    keep = [names[0], "…"]
    me = [n for n in names[1:-1] if "molania" in n.lower()]
    if me:
        keep += [me[0], "…"]
    keep.append(names[-1])
    return ", ".join(keep)


def clean_venue(venue: str) -> str:
    """Drop volume/page/year tails such as 'Journal 41 (16_suppl), 504-504, 2023'."""
    venue = re.split(r"\s+\d+\s*(\(|,)", venue)[0]
    venue = re.sub(r",\s*\d{4}$", "", venue)
    return venue.strip()


def main() -> int:
    try:
        author = scholarly.search_author_id(SCHOLAR_ID)
        author = scholarly.fill(author, sections=["publications"], sortby="year")
    except Exception as exc:  # Scholar occasionally rate-limits; keep old file
        print(f"Could not reach Google Scholar: {exc}", file=sys.stderr)
        return 1

    pubs = []
    for pub in author.get("publications", [])[:MAX_PUBS]:
        try:
            pub = scholarly.fill(pub)  # get full author list + venue
        except Exception:
            pass  # fall back to the summary fields
        bib = pub.get("bib", {})
        title = bib.get("title", "").strip()
        year = str(bib.get("pub_year", "")).strip()
        authors = short_authors(bib.get("author", "").replace(" and ", ", ").strip())
        venue = clean_venue(
            bib.get("journal") or bib.get("citation", "")
        )
        url = pub.get("pub_url", "") or (
            f"https://scholar.google.com/citations?view_op=view_citation&hl=en"
            f"&user={SCHOLAR_ID}&citation_for_view={pub.get('author_pub_id', '')}"
        )
        if title and year:
            pubs.append(
                {
                    "year": year,
                    "title": title,
                    "authors": authors,
                    "venue": venue,
                    "url": url,
                }
            )

    if not pubs:
        print("No publications parsed; keeping existing file.", file=sys.stderr)
        return 1

    # keep any manually added "image" fields from the previous file
    try:
        with open(OUT_FILE, encoding="utf-8") as fh:
            old = {p["title"].strip().lower(): p.get("image") for p in json.load(fh)}
        for p in pubs:
            img = old.get(p["title"].strip().lower())
            if img:
                p["image"] = img
    except Exception:
        pass

    pubs.sort(key=lambda p: p["year"], reverse=True)
    with open(OUT_FILE, "w", encoding="utf-8") as fh:
        json.dump(pubs, fh, ensure_ascii=False, indent=2)
    print(f"Wrote {len(pubs)} publications to {OUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
