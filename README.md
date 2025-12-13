# Sendify-Challenge
My solution to the Sendify Code Challenge 2026

## Scraping client-rendered pages

- Render + scrape a dynamic page (Angular/React/etc): `.venv/bin/python dbs_reader.py --url "https://example.com" --mode playwright --wait-for "css=..." --out data.json`
- Scrape from a saved HTML file (no browser needed): `.venv/bin/python dbs_reader.py --html-file site.html --mode html --out data.json`

If Playwright complains about missing browsers, install them once with: `.venv/bin/python -m playwright install chromium`

Output `data.json` contains:
- `data_test`: values extracted from `[data-test="..."]` elements (useful for stable scraping)
- `captured_json`: optional network-captured JSON responses (when `--capture-url-substring` is set)
