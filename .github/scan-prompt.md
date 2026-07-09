You are running unattended in GitHub Actions on the ai-policy-adolescent
repository, as stage 2 of the change-tracking pipeline. Stage 1
(`scripts/scan.py`) already ran: it detected changed sources and wrote new
full-text captures and diffs under `data/snapshots/<slug>/`. Your job is to
classify those changes into governance events. A human will review your work
as a pull request; be conservative in claims and surface ambiguity rather
than hiding it.

First read `rules/CLAUDE_platform_governance_events.md` (the constitution).
It is the source of truth for scope, taxonomy codes, field definitions, and
classification rules. Then, for each changed source slug listed at the end of
this prompt:

1. Read the newest `data/snapshots/<slug>/<date>.diff` and, for context, the
   matching `<date>.txt` capture. The previous capture named in the diff
   header is also available if you need the before-state.
2. Decide whether the change is taxonomy-relevant per constitution Sections 3
   and 5:
   - **Relevant**: append a new event object to the `events` array in
     `data/events.json`, matching the existing objects' schema exactly (all
     required fields; taxonomy codes verbatim from Section 5; a verbatim
     `relevant_quote` from the new capture; ISO dates; `run_id` set to
     today's date as YYYYMMDD). Never modify or delete existing events.
   - **Not relevant** (formatting, navigation, marketing copy, extraction
     noise): record no event.
3. Date rules (constitution Sections 3.3 and 4.2): never invent dates. If the
   new text states an effective/announcement date, use it. Otherwise the
   change is only known to have occurred between the two capture dates: use
   the new capture date with `date_basis` = `document_date`,
   `date_confidence` = `low`, and `human_review_needed` = `true` explaining
   the uncertainty. Set `human_review_needed` = `true` whenever affected user
   groups, defaults, or rollout status are unclear.
4. If you added events, update `updated_at` in `data/events.json`
   (YYYY-MM-DD, today).
5. Write a run record to `data/runs/<YYYYMMDD>.json`:
   `{"run_id", "run_date", "trigger": "scheduled_scan", "changed_sources":
   [slugs], "events_added": [event ids], "no_event_changes": [{"slug",
   "reason"}], "notes"}`.
6. Validate your work: run
   `python scripts/export.py --csv --out-dir "$RUNNER_TEMP/qc-check" --force`
   and fix any QC failures it reports until it passes.
7. Write a concise markdown PR body to the file path given below the changed
   sources list. Cover: what changed in each source (one or two sentences),
   which events you added and why (or why a change produced no event), and
   what the reviewer should verify first. Reference the diff paths so the
   reviewer can open them.

Constraints:
- The snapshots are your evidence. Do not fetch live pages that block
  automated access, and never bypass bot protections. You may consult the
  Wayback Machine or web search to corroborate dates, but the event's
  `relevant_quote` must come from the stored capture.
- Do not modify anything outside `data/` except the QC output directory and
  the PR body file.
- If a diff is pure noise for every changed source, it is a valid outcome to
  add zero events: say so in the run record and PR body.
