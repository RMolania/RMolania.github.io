# Personal website

Static site (`index.html`) hosted on GitHub Pages. Publications are refreshed daily
from Google Scholar by `.github/workflows/update-publications.yml`, which runs
`fetch_scholar.py` and commits `publications.json`.

## Deploy
1. Create a repo (`<username>.github.io` for a root URL) and push these files to `main`.
2. Settings → Pages → Source: "Deploy from a branch" → `main` / `(root)`.
3. Settings → Actions → General → Workflow permissions → "Read and write permissions".
4. Actions tab → "Update publications" → Run workflow (first run creates `publications.json`).

## Files the page expects
`portrait.jpg`, `logo.svg`, `favicon-32.png`, `logo-hms.jpg`, `logo-dfci.jpg`, `cv.pdf`

## Custom paper images
Add `"image": "images/foo.png"` to an entry in `publications.json`; it is preserved on updates.
