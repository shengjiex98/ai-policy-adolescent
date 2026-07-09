# Platform Governance Events — Run Report

- **Run date:** 2026-07-01
- **Run ID:** 20260701
- **Constitution:** `rules/CLAUDE_platform_governance_events.md`
- **Scope (V1):** Anthropic (Claude), OpenAI (ChatGPT), Google DeepMind (Gemini). Dated events since 2023-01-01 plus baseline snapshots. Simplified 3-sheet output schema.
- **Method:** agent-driven run (Claude Code fetched and classified sources directly; export via `scripts/export_workbook.py`).

## Sources

| Metric | Count |
|---|---:|
| Sources listed in `data/input_sources.xlsx` | 15 |
| Attempted | 15 |
| Successful | 7 |
| Partial | 7 |
| Failed | 1 |
| Skipped | 0 |

**Failures and partials:**

- All 6 OpenAI sources (openai.com, help.openai.com) returned **HTTP 403** to direct fetches. Per constitution Section 2 Step 3 and Section 14, anti-bot protections were not bypassed. OpenAI evidence was instead assembled from web-search results describing the official pages; every OpenAI record is flagged `human_review_needed = TRUE` so a human can verify quotes and dates against the live pages. The ChatGPT Release Notes source produced no usable content at all (failed).
- Anthropic News and Google Gemini Blog hub pages only surface recent (2026) posts; historical safety posts were fetched directly by URL instead (successful).

## Records

| Metric | Count |
|---|---:|
| Records in `platform_events` | 19 |
| Dated events | 15 |
| Baseline policy snapshots | 4 |
| `major_safety_relevant_event` | 14 |
| `minor_contextual_update` | 1 |
| Excluded records | 0 |
| Records needing human review | 14 |

By company: OpenAI 9, Anthropic 5, Google 5.

## Major safety-relevant events

| Date | Company | Event |
|---|---|---|
| 2023-11-15 | Google | Bard opened to teens with safety guardrails |
| 2024-02-13 | OpenAI | ChatGPT memory and temporary chat launched |
| 2024-06-06 | Anthropic | Usage policy permits minor-facing API products with safeguards |
| 2025-02-12 | Google | ML age-estimation testing announced |
| 2025-04-29 | OpenAI | GPT-4o sycophancy update rolled back |
| 2025-05-05 | Google | Gemini opened to under-13 children via Family Link |
| 2025-08-26 | OpenAI | Crisis-safeguard commitments after teen suicide lawsuit |
| 2025-08-28 | Anthropic | Consumer terms: model-training choice and 5-year retention |
| 2025-09-16 | OpenAI | Teen safety principles and age-prediction system announced |
| 2025-09-29 | OpenAI | Parental controls launched for ChatGPT |
| 2025-10-27 | OpenAI | Default model updated for sensitive conversations (170+ clinicians) |
| 2025-10-29 | OpenAI | Usage policies restrict tailored medical/legal advice |
| 2025-12-18 | OpenAI | Model Spec updated with Under-18 Principles |
| 2025-12-18 | Anthropic | Wellbeing measures: crisis banner (988), underage detection |

## High-confirmatory records

- `OPENAI-CHATGPT-2025-08-26-CRISIS-SAFEGUARDS`
- `OPENAI-CHATGPT-2025-09-16-TEEN-SAFETY-AGE-PREDICTION`
- `OPENAI-CHATGPT-2025-09-29-PARENTAL-CONTROLS`
- `OPENAI-CHATGPT-2025-10-27-SENSITIVE-CONVERSATIONS`
- `OPENAI-CHATGPT-2025-12-18-MODEL-SPEC-U18`
- `ANTHROPIC-CLAUDE-2025-12-18-WELLBEING-CRISIS-RESOURCES`
- `GOOGLE-GEMINI-2023-11-15-BARD-TEEN-ACCESS`
- `GOOGLE-GEMINI-2025-05-05-UNDER13-FAMILY-LINK`

## Duplicate reconciliation and source conflicts

- OpenAI's 2025-09-16 announcements ("Teen safety, freedom, and privacy" and "Building towards age prediction", same day) were merged into one event with the second post retained in `supporting_source_urls`.
- The Parental Controls FAQ (help center) was folded into the 2025-09-29 launch event as a supporting source rather than a separate baseline snapshot.
- Secondary press reports differ on the parental-controls launch date (Sept 29 vs 30); Sept 29 used, flagged for review.
- No text hashes from prior runs (first run), so no change detection was performed.

## Recommended next steps for human review

1. **High priority:** verify quotes and dates for all 9 OpenAI events against the live openai.com pages (blocked to automated fetch, HTTP 403) — see `review_queue` sheet.
2. Confirm the rollout start date for Gemini under-13 access (currently week of 2025-05-05 from third-party reporting).
3. Diff Anthropic's Privacy Policy version effective 2026-07-08 against the prior version; it may contain a codable privacy event (takes effect one week after this run).
4. Compare Anthropic's Usage Policy (effective 2025-09-15) against its prior version to determine what changed.
5. For V2: add archived (Wayback) sources for OpenAI pages to obtain fetchable canonical text, and consider expanding sources to system cards and app-store metadata.

---

## Addendum (2026-07-09): Wayback Machine verification of restricted OpenAI pages

All OpenAI web properties return HTTP 403 to automated fetches, so the original
run relied on search-derived evidence with `human_review_needed = TRUE` on all
9 OpenAI records. On 2026-07-09 those records were re-verified against Wayback
Machine snapshots of the official pages:

- **All 9 publication/effective dates confirmed exactly** as recorded,
  including the GPT-5 default rollout (August 7, 2025), confirmed from the
  archived ChatGPT Release Notes entry.
- **All quotes replaced with verbatim text** from the archived official pages;
  snapshot URLs added to `supporting_source_urls`; extracted snapshot text
  preserved in `data/raw/wayback/`.
- **Review flags cleared** on all 9 OpenAI records; `classification_confidence`
  raised to `high`. Records needing human review: 14 → 5 (remaining: Gemini
  under-13 rollout date, two Anthropic policy-version diffs, two undated
  Google baselines).
- **Source log updated**: 5 previously failed/partial OpenAI sources are now
  `success` via archive snapshots. `OpenAI Age Prediction Help` remains
  `partial` (no Wayback snapshot exists for that help-center article).
- `input_sources.csv` now notes the Wayback retrieval path for all OpenAI
  sources so future runs use archives directly.
