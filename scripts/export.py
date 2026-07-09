# /// script
# requires-python = ">=3.11"
# ///
"""Export the event registry to the default web viewer, optionally CSV.

Reads the longitudinal store: data/events.json (cumulative event registry),
data/state.json (per-source scan state), and data/sources.csv (source list).

Usage:
    uv run scripts/export.py                # HTML viewer
    uv run scripts/export.py --csv          # viewer + CSV files
    python scripts/export.py --csv --out-dir site --force --index   # CI/site

Applies the V1 subset of QC rules from the constitution (Section 11) and
fails loudly if any check is violated. Never overwrites existing outputs
unless --force is passed.
"""

import argparse
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# Section 5 taxonomy: category -> valid subcategory codes
TAXONOMY = {
    "A_AGE_ELIGIBILITY_ASSURANCE": ["A1_MINIMUM_AGE_POLICY", "A2_AGE_PREDICTION_OR_AGE_INFERENCE", "A3_ID_CHECK_OR_AGE_VERIFICATION", "A4_DEFAULT_TEEN_EXPERIENCE", "A5_UNDER_13_SUPERVISED_ACCESS", "A6_AGE_ENFORCEMENT_AND_ACCOUNT_ACTIONS"],
    "B_TEEN_MODE_YOUTH_SAFETY_DEFAULTS": ["B1_STRICTER_CONTENT_FILTERS_FOR_MINORS", "B2_REDUCED_PERSONALIZATION_OR_MEMORY_FOR_MINORS", "B3_SENSITIVE_TOPIC_HANDLING_FOR_TEENS", "B4_EDUCATION_OR_SCHOOL_ACCOUNT_PROTECTIONS", "B5_YOUTH_DEFAULT_PRIVACY_SETTINGS", "B6_SAFE_COMPLETION_STYLE_FOR_MINORS"],
    "C_PARENTAL_FAMILY_CONTROLS": ["C1_PARENT_DASHBOARD_OR_FAMILY_CENTER", "C2_DISABLE_OR_RESTRICT_AI_FEATURES_FOR_MINOR", "C3_PARENTAL_VISIBILITY_AND_MINOR_PRIVACY_BALANCE", "C4_CRISIS_OR_SELF_HARM_ALERTS_TO_PARENT_TRUSTED_CONTACT", "C5_PARENTAL_EDUCATION_AND_GUIDANCE"],
    "D_SELF_HARM_CRISIS_HANDLING": ["D1_988_OR_CRISIS_RESOURCE_ROUTING", "D2_SELF_HARM_OR_SUICIDE_RESPONSE_PROTOCOL", "D3_EMERGENCY_ESCALATION_OR_DUTY_TO_ACT_POLICY", "D4_TRUSTED_ADULT_OR_CLINICIAN_DISCLOSURE_PROMPT", "D5_EATING_DISORDER_SUBSTANCE_ABUSE_OR_ABUSE_CRISIS_HANDLING", "D6_NOT_A_CRISIS_SERVICE_DISCLAIMER"],
    "E_HARMFUL_CONTENT_REFUSAL_SAFETY_FILTERS": ["E1_SELF_HARM_METHODS_OR_INSTRUCTIONS_REFUSAL", "E2_VIOLENCE_ABUSE_EXPLOITATION_REFUSAL", "E3_SEXUAL_CONTENT_INVOLVING_MINORS_REFUSAL", "E4_ILLICIT_SUBSTANCES_OR_MEDICAL_MISUSE_REFUSAL", "E5_EATING_DISORDER_OR_BODY_HARM_REFUSAL", "E6_EVASION_JAILBREAK_OR_UNSAFE_COACHING_REFUSAL", "E7_BULLYING_HARASSMENT_OR_COERCION_REFUSAL"],
    "F_MENTAL_HEALTH_ADVICE_BOUNDARIES": ["F1_DIAGNOSIS_TREATMENT_REFUSAL_OR_LIMITATION", "F2_NOT_THERAPIST_OR_NOT_MEDICAL_ADVICE_DISCLOSURE", "F3_MEDICATION_OR_CLINICAL_CARE_ADVICE_LIMITS", "F4_SUPPORTIVE_NONCLINICAL_FRAMING", "F5_THERAPIST_ROLEPLAY_OR_SIMULATED_CLINICIAN_RESTRICTION", "F6_PROFESSIONAL_HELP_SEEKING_PROMPTS"],
    "G_PRIVACY_MEMORY_RETENTION_TRAINING": ["G1_CHAT_HISTORY_RETENTION_POLICY", "G2_MEMORY_CONTROLS", "G3_MODEL_TRAINING_OPT_OUT_OR_DATA_USE", "G4_HUMAN_REVIEW_OF_CONVERSATIONS", "G5_SENSITIVE_CONVERSATION_HANDLING", "G6_THIRD_PARTY_SHARING_OR_SUBPROCESSORS", "G7_DELETION_EXPORT_OR_ACCOUNT_DATA_RIGHTS"],
    "H_TRANSPARENCY_REPORTING_EVALUATION": ["H1_RELEASE_NOTES_OR_CHANGELOG", "H2_MODEL_CARD_OR_SYSTEM_CARD", "H3_SAFETY_REPORT_OR_TRANSPARENCY_REPORT", "H4_RED_TEAMING_OR_INDEPENDENT_EVALUATION", "H5_POLICY_VERSIONING_OR_DOCUMENTED_GOVERNANCE_PROCESS"],
    "I_PRODUCT_MODEL_INTEGRATION_EVENTS": ["I1_NEW_MODEL_RELEASE_OR_MODEL_REPLACEMENT", "I2_VOICE_VIDEO_OR_MULTIMODAL_ROLLOUT", "I3_COMPANION_CHARACTER_OR_ROLEPLAY_MODE", "I4_SOCIAL_MEDIA_OR_MESSAGING_INTEGRATION", "I5_API_OR_DEVELOPER_POLICY_CHANGE", "I6_HEALTHCARE_EDUCATION_OR_ENTERPRISE_INTEGRATION"],
    "J_ACCESS_MARKET_APP_STORE_ACCOUNT": ["J1_APP_STORE_AGE_RATING_OR_METADATA", "J2_GEOGRAPHIC_ROLLOUT_OR_RESTRICTION", "J3_ACCOUNT_ELIGIBILITY_OR_CONSENT_RULES", "J4_FEATURE_ACCESS_RESTRICTION_OR_PERMISSIONING"],
    "K_INCIDENT_RESPONSE_PRODUCT_CHANGE": ["K1_SAFETY_INCIDENT_RESPONSE", "K2_LITIGATION_SETTLEMENT_OR_REGULATORY_RESPONSE", "K3_PUBLIC_CONTROVERSY_GOVERNANCE_CHANGE"],
}

EVENT_FIELDS = [
    "event_id", "company", "platform", "event_title", "event_summary",
    "event_importance", "event_type", "event_date", "date_basis",
    "date_confidence", "primary_category_code", "primary_subcategory_code",
    "safety_relevance_score", "expected_direction", "affected_user_group",
    "analytic_priority", "mechanism_summary", "survey_exposure_mapping",
    "source_name", "source_url", "supporting_source_urls", "relevant_quote",
    "classification_confidence", "human_review_needed", "human_review_reason",
]

SOURCE_STATE_FIELDS = [
    "source_slug", "source_name", "source_url", "company", "platform",
    "status", "last_checked", "last_changed", "last_snapshot", "note",
]

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

IMPORTANCE_VALUES = {"major_safety_relevant_event", "minor_contextual_update", "baseline_policy_snapshot", "exclude"}
CONFIDENCE_VALUES = {"high", "medium", "low"}


def qc(events: list[dict]) -> list[str]:
    errors = []
    seen_ids = set()
    for ev in events:
        eid = ev.get("event_id", "<missing event_id>")
        if eid in seen_ids:
            errors.append(f"{eid}: duplicate event_id")
        seen_ids.add(eid)
        for field in EVENT_FIELDS:
            if field in ("supporting_source_urls", "human_review_reason"):
                continue
            if ev.get(field) in (None, ""):
                errors.append(f"{eid}: missing required field {field}")
        cat = ev.get("primary_category_code")
        sub = ev.get("primary_subcategory_code")
        if cat not in TAXONOMY:
            errors.append(f"{eid}: unknown primary_category_code {cat}")
        elif sub not in TAXONOMY[cat]:
            errors.append(f"{eid}: subcategory {sub} not valid under {cat}")
        date = ev.get("event_date", "")
        if date != "unknown" and not ISO_DATE.match(str(date)):
            errors.append(f"{eid}: event_date {date!r} is neither ISO YYYY-MM-DD nor 'unknown'")
        if ev.get("event_importance") not in IMPORTANCE_VALUES:
            errors.append(f"{eid}: invalid event_importance {ev.get('event_importance')}")
        if ev.get("classification_confidence") not in CONFIDENCE_VALUES:
            errors.append(f"{eid}: invalid classification_confidence")
        if ev.get("classification_confidence") == "low" and not ev.get("human_review_needed"):
            errors.append(f"{eid}: low classification_confidence requires human_review_needed")
        if ev.get("event_importance") == "major_safety_relevant_event" and int(ev.get("safety_relevance_score", 0)) < 2:
            errors.append(f"{eid}: major event requires safety_relevance_score >= 2")
        if ev.get("human_review_needed") and not ev.get("human_review_reason"):
            errors.append(f"{eid}: human_review_needed without human_review_reason")
        if not str(ev.get("source_url", "")).startswith("http"):
            errors.append(f"{eid}: source_url is not a URL")
    return errors


def check_writable(path: Path, force: bool) -> None:
    if path.exists() and not force:
        sys.exit(f"Refusing to overwrite existing output: {path}")


def load_payload() -> dict:
    """Assemble the viewer/CSV payload from the longitudinal store."""
    registry = json.loads((DATA / "events.json").read_text())
    state = json.loads((DATA / "state.json").read_text())
    with (DATA / "sources.csv").open() as f:
        source_rows = list(csv.DictReader(f))
    hints = {row["source_slug"]: row for row in source_rows}
    sources = []
    for slug, entry in state.items():
        hint = hints.get(slug, {})
        sources.append({
            "source_slug": slug,
            "source_name": entry.get("source_name", slug),
            "source_url": entry.get("source_url", ""),
            "company": hint.get("company_hint", ""),
            "platform": hint.get("platform_hint", ""),
            "status": entry.get("last_status", "unknown"),
            "last_checked": entry.get("last_checked", ""),
            "last_changed": entry.get("last_changed", ""),
            "last_snapshot": entry.get("last_snapshot", ""),
            "note": entry.get("note", ""),
        })
    return {
        "generated": dt.date.today().isoformat(),
        "updated_at": registry.get("updated_at", ""),
        "events": registry["events"],
        "sources": sources,
    }


def write_csvs(payload: dict, out_dir: Path, date_tag: str, force: bool = False) -> list[Path]:
    events_path = out_dir / f"platform_events_{date_tag}.csv"
    sources_path = out_dir / f"sources_state_{date_tag}.csv"
    for path in (events_path, sources_path):
        check_writable(path, force)
    with events_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=EVENT_FIELDS + ["run_id"], extrasaction="ignore")
        writer.writeheader()
        for ev in payload["events"]:
            row = {k: ev.get(k, "") for k in EVENT_FIELDS + ["run_id"]}
            row["human_review_needed"] = "TRUE" if ev.get("human_review_needed") else "FALSE"
            writer.writerow(row)
    with sources_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SOURCE_STATE_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(payload["sources"])
    return [events_path, sources_path]


VIEWER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Platform Governance Events — __RUN_DATE__</title>
<style>
:root {
  --bg: #ffffff; --fg: #1a1d21; --muted: #6b7280; --line: #e5e7eb;
  --panel: #f6f7f9; --accent: #2563eb; --accent-fg: #ffffff;
  --major: #b45309; --major-bg: #fef3c7;
  --minor: #4b5563; --minor-bg: #e5e7eb;
  --baseline: #1d4ed8; --baseline-bg: #dbeafe;
  --review: #7c3aed; --review-bg: #ede9fe;
  --ok: #15803d; --ok-bg: #dcfce7;
  --warn: #b45309; --warn-bg: #fef3c7;
  --fail: #b91c1c; --fail-bg: #fee2e2;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #111417; --fg: #e6e8ea; --muted: #9aa1a9; --line: #2a2f35;
    --panel: #1a1f24; --accent: #60a5fa; --accent-fg: #0b1220;
    --major: #fbbf24; --major-bg: #45340a;
    --minor: #cbd5e1; --minor-bg: #2e353d;
    --baseline: #93c5fd; --baseline-bg: #172a54;
    --review: #c4b5fd; --review-bg: #33245c;
    --ok: #4ade80; --ok-bg: #133821;
    --warn: #fbbf24; --warn-bg: #45340a;
    --fail: #f87171; --fail-bg: #4a1414;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font: 14px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
header { padding: 20px 24px 8px; }
header h1 { margin: 0 0 4px; font-size: 20px; }
header .sub { color: var(--muted); font-size: 13px; }
nav.tabs { display: flex; gap: 4px; padding: 12px 24px 0; border-bottom: 1px solid var(--line); }
nav.tabs button {
  border: 1px solid var(--line); border-bottom: none; background: var(--panel); color: var(--fg);
  padding: 7px 16px; border-radius: 8px 8px 0 0; cursor: pointer; font-size: 13px;
}
nav.tabs button.active { background: var(--bg); font-weight: 600; border-color: var(--line); position: relative; top: 1px; }
main { padding: 16px 24px 48px; }
.toolbar { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 14px; }
.toolbar label { font-size: 12px; color: var(--muted); display: flex; align-items: center; gap: 6px; }
.toolbar select, .toolbar input[type="search"] {
  background: var(--panel); color: var(--fg); border: 1px solid var(--line);
  border-radius: 6px; padding: 5px 8px; font-size: 13px;
}
.toolbar input[type="search"] { width: 220px; }
.toolbar .count { margin-left: auto; color: var(--muted); font-size: 12px; }
.tablewrap { overflow-x: auto; border: 1px solid var(--line); border-radius: 8px; }
table { border-collapse: collapse; width: 100%; min-width: 900px; }
th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { font-size: 12px; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); background: var(--panel); position: sticky; top: 0; }
tr.event { cursor: pointer; }
tr.event:hover { background: var(--panel); }
tr.grouphead td {
  background: var(--panel); font-weight: 600; font-size: 13px; padding: 6px 10px;
  border-top: 2px solid var(--line);
}
td.date { white-space: nowrap; font-variant-numeric: tabular-nums; }
td.date .basis { display: block; font-size: 11px; color: var(--muted); }
.badge {
  display: inline-block; padding: 1px 8px; border-radius: 999px; font-size: 11px; font-weight: 600;
  white-space: nowrap;
}
.b-major { color: var(--major); background: var(--major-bg); }
.b-minor { color: var(--minor); background: var(--minor-bg); }
.b-baseline { color: var(--baseline); background: var(--baseline-bg); }
.b-review { color: var(--review); background: var(--review-bg); }
.b-ok { color: var(--ok); background: var(--ok-bg); }
.b-warn { color: var(--warn); background: var(--warn-bg); }
.b-fail { color: var(--fail); background: var(--fail-bg); }
.cat { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px; }
a { color: var(--accent); }
tr.detail td { background: var(--panel); padding: 14px 16px; }
.detail-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 8px 20px; margin: 10px 0; }
.detail-grid div { font-size: 12px; }
.detail-grid .k { color: var(--muted); }
blockquote {
  margin: 10px 0; padding: 8px 12px; border-left: 3px solid var(--accent);
  background: var(--bg); border-radius: 0 6px 6px 0; font-style: italic;
}
.links { margin-top: 10px; }
.links a { display: inline-block; margin: 2px 12px 2px 0; word-break: break-all; }
.review-note { margin-top: 10px; padding: 8px 12px; border-radius: 6px; background: var(--review-bg); color: var(--review); font-size: 13px; }
.empty { padding: 24px; text-align: center; color: var(--muted); }
footer { padding: 0 24px 24px; color: var(--muted); font-size: 12px; }
</style>
</head>
<body>
<header>
  <h1>AI Platform Governance Events</h1>
  <div class="sub" id="subtitle"></div>
</header>
<nav class="tabs">
  <button id="tab-events" class="active">Events</button>
  <button id="tab-sources">Sources</button>
</nav>
<main>
  <section id="panel-events">
    <div class="toolbar">
      <label>Group by
        <select id="groupby">
          <option value="none">None</option>
          <option value="company">Company</option>
          <option value="category">Category</option>
          <option value="importance">Importance</option>
          <option value="year">Year</option>
        </select>
      </label>
      <label>Sort by
        <select id="sortby">
          <option value="date_desc">Date ↓ (newest first)</option>
          <option value="date_asc">Date ↑ (oldest first)</option>
          <option value="company">Company</option>
          <option value="score">Safety score ↓</option>
        </select>
      </label>
      <label>Company
        <select id="f-company"><option value="">All</option></select>
      </label>
      <label>Importance
        <select id="f-importance"><option value="">All</option></select>
      </label>
      <label><input type="checkbox" id="f-review"> Needs review only</label>
      <label>Search <input type="search" id="f-search" placeholder="title, summary, quote…"></label>
      <span class="count" id="count"></span>
    </div>
    <div class="tablewrap">
      <table id="events-table">
        <thead>
          <tr>
            <th>Date</th><th>Company</th><th>Platform</th><th>Event</th>
            <th>Category</th><th>Importance</th><th>Score</th><th>Review</th><th>Source</th>
          </tr>
        </thead>
        <tbody id="events-body"></tbody>
      </table>
    </div>
  </section>
  <section id="panel-sources" hidden>
    <div class="tablewrap">
      <table>
        <thead>
          <tr><th>Source</th><th>Company</th><th>Status</th><th>Last checked</th><th>Last changed</th><th>Notes</th></tr>
        </thead>
        <tbody id="sources-body"></tbody>
      </table>
    </div>
  </section>
</main>
<footer>
  Click an event row to see its summary, quote, and verification links.
  Generated by <code>scripts/export.py</code> from the run JSON; see the run report for methodology.
</footer>
<script id="data" type="application/json">__DATA__</script>
<script>
"use strict";
const DATA = JSON.parse(document.getElementById("data").textContent);
const EVENTS = DATA.events;

const IMPORTANCE_LABEL = {
  major_safety_relevant_event: ["Major", "b-major"],
  minor_contextual_update: ["Minor", "b-minor"],
  baseline_policy_snapshot: ["Baseline", "b-baseline"],
  exclude: ["Excluded", "b-minor"],
};
function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
    else node.setAttribute(k, v);
  }
  for (const child of children) {
    if (child == null) continue;
    node.append(child.nodeType ? child : document.createTextNode(child));
  }
  return node;
}
function link(url, label) {
  return el("a", { href: url, target: "_blank", rel: "noopener noreferrer" }, label || url);
}
function catShort(code) { return code ? code.split("_")[0] : ""; }
function catLabel(code) {
  if (!code) return "";
  return code.split("_").slice(1).join(" ").toLowerCase();
}

document.getElementById("subtitle").textContent =
  `${EVENTS.length} records · ` +
  `${EVENTS.filter(e => e.event_importance === "major_safety_relevant_event").length} major safety-relevant · ` +
  `${EVENTS.filter(e => e.human_review_needed).length} need review · ` +
  `data updated ${DATA.updated_at}`;

// Populate filter options
const companies = [...new Set(EVENTS.map(e => e.company))].sort();
for (const c of companies) document.getElementById("f-company").append(el("option", { value: c }, c));
const importances = [...new Set(EVENTS.map(e => e.event_importance))];
for (const imp of importances) {
  document.getElementById("f-importance").append(
    el("option", { value: imp }, (IMPORTANCE_LABEL[imp] || [imp])[0]));
}

const state = { expanded: new Set() };

function filtered() {
  const company = document.getElementById("f-company").value;
  const importance = document.getElementById("f-importance").value;
  const reviewOnly = document.getElementById("f-review").checked;
  const q = document.getElementById("f-search").value.trim().toLowerCase();
  return EVENTS.filter(e => {
    if (company && e.company !== company) return false;
    if (importance && e.event_importance !== importance) return false;
    if (reviewOnly && !e.human_review_needed) return false;
    if (q) {
      const hay = [e.event_title, e.event_summary, e.relevant_quote, e.event_id,
        e.primary_category_code, e.primary_subcategory_code, e.platform, e.company]
        .join(" ").toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });
}

function sorted(list) {
  const mode = document.getElementById("sortby").value;
  const byDate = (a, b) => String(a.event_date).localeCompare(String(b.event_date));
  const copy = [...list];
  if (mode === "date_asc") copy.sort(byDate);
  else if (mode === "date_desc") copy.sort((a, b) => byDate(b, a));
  else if (mode === "company") copy.sort((a, b) => a.company.localeCompare(b.company) || byDate(b, a));
  else if (mode === "score") copy.sort((a, b) => (b.safety_relevance_score - a.safety_relevance_score) || byDate(b, a));
  return copy;
}

function groupKey(e) {
  const mode = document.getElementById("groupby").value;
  if (mode === "company") return e.company;
  if (mode === "category") return `${catShort(e.primary_category_code)} — ${catLabel(e.primary_category_code)}`;
  if (mode === "importance") return (IMPORTANCE_LABEL[e.event_importance] || [e.event_importance])[0];
  if (mode === "year") return String(e.event_date).slice(0, 4);
  return null;
}

function detailRow(e) {
  const td = el("td", { colspan: "9" });
  td.append(el("div", {}, e.event_summary));
  const grid = el("div", { class: "detail-grid" });
  const meta = [
    ["Event ID", e.event_id], ["Run", e.run_id], ["Type", e.event_type],
    ["Date basis", `${e.date_basis} (confidence: ${e.date_confidence})`],
    ["Subcategory", e.primary_subcategory_code],
    ["Expected direction", e.expected_direction],
    ["Affected group", e.affected_user_group],
    ["Analytic priority", e.analytic_priority],
    ["Survey mapping", e.survey_exposure_mapping],
    ["Classification confidence", e.classification_confidence],
  ];
  for (const [k, v] of meta) grid.append(el("div", {}, el("span", { class: "k" }, k + ": "), String(v)));
  td.append(grid);
  td.append(el("div", {}, el("span", { class: "k", style: "color:var(--muted);font-size:12px" }, "Mechanism: "), e.mechanism_summary));
  td.append(el("blockquote", {}, "“" + e.relevant_quote + "”"));
  const links = el("div", { class: "links" }, el("strong", {}, "Verify: "));
  links.append(link(e.source_url, e.source_name));
  for (const u of (e.supporting_source_urls || "").split("|").filter(Boolean)) links.append(link(u));
  td.append(links);
  if (e.human_review_needed) {
    td.append(el("div", { class: "review-note" },
      "⚑ Needs review — " + e.human_review_reason +
      (e.suggested_question_for_reviewer ? " Question: " + e.suggested_question_for_reviewer : "")));
  }
  return el("tr", { class: "detail" }, td);
}

function render() {
  const body = document.getElementById("events-body");
  body.replaceChildren();
  const list = sorted(filtered());
  document.getElementById("count").textContent = `${list.length} of ${EVENTS.length} records`;
  if (!list.length) {
    body.append(el("tr", {}, el("td", { colspan: "9", class: "empty" }, "No records match the current filters.")));
    return;
  }
  const grouping = document.getElementById("groupby").value !== "none";
  if (grouping) {
    // Cluster rows by group (groups ordered by first appearance in the sorted
    // list, so the sort mode still decides group order); the sort within each
    // group is preserved because Array.prototype.sort is stable.
    const order = new Map();
    for (const e of list) {
      const g = groupKey(e);
      if (!order.has(g)) order.set(g, order.size);
    }
    list.sort((a, b) => order.get(groupKey(a)) - order.get(groupKey(b)));
  }
  let lastGroup;
  for (const e of list) {
    if (grouping) {
      const g = groupKey(e);
      if (g !== lastGroup) {
        const n = list.filter(x => groupKey(x) === g).length;
        body.append(el("tr", { class: "grouphead" }, el("td", { colspan: "9" }, `${g} (${n})`)));
        lastGroup = g;
      }
    }
    const [impLabel, impClass] = IMPORTANCE_LABEL[e.event_importance] || [e.event_importance, "b-minor"];
    const row = el("tr", { class: "event", onclick: () => {
      state.expanded.has(e.event_id) ? state.expanded.delete(e.event_id) : state.expanded.add(e.event_id);
      render();
    }},
      el("td", { class: "date" }, e.event_date, el("span", { class: "basis" }, e.date_basis.replaceAll("_", " "))),
      el("td", {}, e.company),
      el("td", {}, e.platform),
      el("td", {}, e.event_title),
      el("td", {}, el("span", { class: "cat", title: e.primary_category_code + " / " + e.primary_subcategory_code },
        catShort(e.primary_subcategory_code) + " " + catLabel(e.primary_category_code))),
      el("td", {}, el("span", { class: "badge " + impClass }, impLabel)),
      el("td", {}, String(e.safety_relevance_score)),
      el("td", {}, e.human_review_needed ? el("span", { class: "badge b-review", title: e.human_review_reason }, "⚑ review") : ""),
      el("td", { onclick: ev => ev.stopPropagation() }, link(e.source_url, "source ↗")),
    );
    body.append(row);
    if (state.expanded.has(e.event_id)) body.append(detailRow(e));
  }
}

function renderSources() {
  const body = document.getElementById("sources-body");
  body.replaceChildren();
  for (const s of DATA.sources) {
    const cls = s.status.startsWith("success") ? "b-ok"
      : s.status.startsWith("failed") ? "b-fail" : "b-warn";
    body.append(el("tr", {},
      el("td", {}, link(s.source_url, s.source_name)),
      el("td", {}, s.company || ""),
      el("td", {}, el("span", { class: "badge " + cls, title: s.status }, s.status.split(":")[0])),
      el("td", {}, s.last_checked || ""),
      el("td", {}, s.last_changed || ""),
      el("td", {}, s.note || ""),
    ));
  }
}

for (const [btn, panel] of [["tab-events", "panel-events"], ["tab-sources", "panel-sources"]]) {
  document.getElementById(btn).addEventListener("click", () => {
    for (const b of document.querySelectorAll("nav.tabs button")) b.classList.remove("active");
    document.getElementById(btn).classList.add("active");
    document.getElementById("panel-events").hidden = panel !== "panel-events";
    document.getElementById("panel-sources").hidden = panel !== "panel-sources";
  });
}
for (const id of ["groupby", "sortby", "f-company", "f-importance", "f-review", "f-search"]) {
  document.getElementById(id).addEventListener("input", render);
}
render();
renderSources();
</script>
</body>
</html>
"""


def viewer_html(payload: dict) -> str:
    blob = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    return VIEWER_TEMPLATE.replace("__RUN_DATE__", payload["generated"]).replace("__DATA__", blob)


def write_viewer(payload: dict, out_dir: Path, date_tag: str, force: bool = False, index: bool = False) -> list[Path]:
    viewer_path = out_dir / f"events_viewer_{date_tag}.html"
    paths = [viewer_path]
    if index:
        paths.append(out_dir / "index.html")
    for path in paths:
        check_writable(path, force)
    html = viewer_html(payload)
    viewer_path.write_text(html)
    if index:
        paths[1].write_text(html)
    return paths


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export the event registry to a static HTML viewer, optionally with CSVs."
    )
    parser.add_argument("--csv", action="store_true", help="Also write event and source-state CSV files")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "output",
        help="Directory for generated outputs (default: output)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing outputs. Intended for clean CI/site publishing.",
    )
    parser.add_argument(
        "--index",
        action="store_true",
        help="Also write index.html with the same viewer HTML for hosted sites.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args(sys.argv[1:])
    payload = load_payload()
    date_tag = payload["generated"].replace("-", "")

    errors = qc(payload["events"])
    if errors:
        print("QC FAILED:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    print(f"QC passed ({len(payload['events'])} events checked)")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for path in write_viewer(payload, args.out_dir, date_tag, force=args.force, index=args.index):
        print(f"Wrote {path}")
    if args.csv:
        for path in write_csvs(payload, args.out_dir, date_tag, force=args.force):
            print(f"Wrote {path}")


if __name__ == "__main__":
    main()
