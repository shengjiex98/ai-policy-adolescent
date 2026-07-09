# AI Policy — Adolescent Mental Health

Inventory of AI platform governance events relevant to adolescent use of AI
chatbots for mental health needs. Scope, taxonomy, and workflow are defined in
[rules/CLAUDE_platform_governance_events.md](rules/CLAUDE_platform_governance_events.md)
(the "constitution"). V1 scope: Anthropic (Claude), OpenAI (ChatGPT), and
Google DeepMind (Gemini), with dated events since 2023-01-01.

## Workflow

1. **Edit sources** in [data/input_sources.csv](data/input_sources.csv)
   (plain CSV; regenerate the seed list with
   `uv run scripts/make_input_sources.py`).
2. **Run a scrape** (agent-driven): Claude Code fetches each enabled source,
   extracts and classifies events per the constitution, and writes the
   canonical dataset to `data/events_YYYYMMDD.json`.
3. **Export** the run:

   ```sh
   uv run scripts/export.py data/events_YYYYMMDD.json          # web viewer (default)
   uv run scripts/export.py data/events_YYYYMMDD.json --csv    # viewer + CSV files
   ```

4. **View**: open `output/events_viewer_YYYYMMDD.html` in a browser. It is a
   self-contained page (data embedded, no server needed) with grouping by
   company/category/importance/year, sorting by date/company/safety score,
   filters, search, and per-event verification links. The Sources tab shows
   which sources succeeded, were partial, or failed.

5. **Publish to GitHub Pages**: after changes land on `main`, the
   `Deploy web viewer` GitHub Actions workflow builds the latest
   `data/events_YYYYMMDD.json` into a Pages artifact. The hosted site uses a
   stable `index.html` URL for the latest run, plus dated HTML and CSV files.
   The project site URL is
   `https://shengjiex98.github.io/ai-policy-adolescent/` after GitHub Pages is
   enabled with **Source: GitHub Actions** in the repository Pages settings.

The export runs quality-control checks (taxonomy codes, ISO dates, required
fields, review-flag rules) before writing anything and refuses to overwrite
existing dated outputs unless `--force` is passed for CI/site publishing.

## Layout

```
rules/      constitutions defining scope, taxonomy, and output requirements
data/       input_sources.csv and canonical per-run events JSON
scripts/    make_input_sources.py, export.py (standalone uv scripts, stdlib only)
output/     generated viewer HTML, CSV exports, and markdown run reports
.github/    GitHub Pages deployment workflow
```

## Notes

- The constitution specifies `.xlsx` input/output workbooks; this repo uses
  CSV/JSON/HTML instead — an operator-approved simplification (V2). The V1
  xlsx pipeline was removed.
- OpenAI web properties block automated fetching (HTTP 403). Per the
  constitution, bot protections are not bypassed; OpenAI records are built
  from search-derived evidence and flagged `human_review_needed`.
