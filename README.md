# AI Policy — Adolescent Mental Health

Longitudinal inventory of AI platform governance events relevant to adolescent
use of AI chatbots for mental health needs: a baseline of current policies plus
tracked changes over time. Scope, taxonomy, and workflow are defined in
[rules/CLAUDE_platform_governance_events.md](rules/CLAUDE_platform_governance_events.md)
(the "constitution"). Current scope: Anthropic (Claude), OpenAI (ChatGPT), and
Google DeepMind (Gemini), with dated events since 2023-01-01.

## Data model

Git is the version store; everything is flat, diffable text.

```
data/
  sources.csv          canonical source list (hand-edited; one row per source)
  events.json          cumulative event registry (append-only; one entry per
                       classified governance event or baseline snapshot)
  state.json           per-source scan state: content hash, last checked,
                       last changed, fetch status
  snapshots/<slug>/    full-text captures, one <date>.txt per change detected,
                       plus <date>.diff against the previous capture
  runs/                per-run audit records (source logs, notes)
```

## Workflow

1. **Edit sources** directly in [data/sources.csv](data/sources.csv). Each row
   needs a stable `source_slug` (names the snapshot directory).
2. **Scan** (deterministic, no LLM):

   ```sh
   uv run scripts/scan.py            # fetch → normalize → hash → snapshot+diff
   uv run scripts/scan.py --dry-run  # report changes without writing
   ```

   Unchanged sources only update `last_checked`. Changed sources get a new
   snapshot and diff, and are listed as `CHANGED` for stage 2.
3. **Classify** (agent-driven): for each changed source, Claude Code reads the
   new `.diff`/`.txt` against the constitution and appends any
   taxonomy-relevant events to `data/events.json` (trivial changes are noted
   but produce no event). Verification evidence (quotes, dates, archive URLs)
   goes on the event record.
4. **Export**:

   ```sh
   uv run scripts/export.py          # self-contained web viewer (default)
   uv run scripts/export.py --csv    # viewer + CSV files
   ```

5. **View**: open `output/events_viewer_YYYYMMDD.html`. Grouping by
   company/category/importance/year, sorting, filters, search, per-event
   verification links; the Sources tab shows each source's scan status, last
   check, and last change.
6. **Publish**: pushes to `main` that touch the data or exporter trigger the
   `Deploy web viewer` workflow, which rebuilds the site at
   `https://shengjiex98.github.io/ai-policy-adolescent/` (stable `index.html`
   plus dated HTML/CSV artifacts).

The export runs quality-control checks (taxonomy codes, ISO dates, required
fields, review-flag rules) before writing anything and refuses to overwrite
existing dated outputs unless `--force` is passed for CI/site publishing.

## Automation

The `Weekly source scan` workflow (`.github/workflows/scan.yml`, Mondays
13:00 UTC or manual dispatch) runs the two stages unattended:

1. `scan.py` runs deterministically. If nothing changed, the state
   bookkeeping is committed straight to `main` and the run ends — no LLM is
   invoked.
2. If sources changed, the workflow runs Claude Code headlessly with
   [.github/scan-prompt.md](.github/scan-prompt.md): it classifies the new
   diffs against the constitution, appends events to `data/events.json`,
   writes a run record, and drafts the PR body. A QC gate re-validates the
   registry, then a pull request is opened for human review.

Publication stays PR-gated: the agent proposes, a human merges, and the merge
triggers the Pages redeploy. Setup requires one repository secret,
`ANTHROPIC_API_KEY` (Settings → Secrets and variables → Actions). The
schedule only takes effect once the workflow file is on `main`.

## Layout

```
rules/      constitutions defining scope, taxonomy, and output requirements
data/       sources.csv, events.json, state.json, snapshots/, runs/
scripts/    scan.py (change detection), export.py (viewer/CSV) — stdlib only
output/     generated viewer HTML, CSV exports, and markdown run reports
.github/    GitHub Pages deployment workflow
```

## Notes

- The constitution specifies `.xlsx` input/output workbooks; this repo uses
  CSV/JSON/HTML instead — an operator-approved simplification. The original
  xlsx pipeline was removed.
- OpenAI web properties block automated fetching of live pages (HTTP 403).
  `scan.py` retrieves those sources from Wayback Machine snapshots instead
  (sources whose `notes` mention Wayback, plus an automatic fallback on 403).
  Verbatim quotes and dates were verified against archived text; snapshot URLs
  live in each event's `supporting_source_urls`. Per the constitution, bot
  protections are never bypassed.
- Snapshots captured before 2026-07-09 were migrated from an earlier extraction
  format; diffs against them reflect extraction differences as well as content
  changes. Captures from 2026-07-09 onward use `scan.py`'s normalizer and are
  directly comparable.
