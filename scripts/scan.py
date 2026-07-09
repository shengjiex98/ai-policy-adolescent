# /// script
# requires-python = ">=3.11"
# ///
"""Deterministic source scanner (stage 1 of the tracking pipeline).

For every enabled source in data/sources.csv: fetch the page (live, or via
Wayback Machine for sources whose live pages block automated fetching),
normalize to text, and hash. If the hash differs from data/state.json, save a
full-text capture to data/snapshots/<slug>/<date>.txt plus a unified diff
against the previous capture, and update state.

No LLM involved: this stage only detects *that* something changed. Classifying
a change into governance events (per rules/CLAUDE_platform_governance_events.md)
is the agent-driven stage, which should read the printed CHANGED lines and the
new .diff files.

Usage:
    uv run scripts/scan.py             # scan all enabled sources
    uv run scripts/scan.py --dry-run   # report changes without writing
"""

import csv
import datetime as dt
import difflib
import gzip
import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
UA = {"User-Agent": "ai-policy-adolescent research scanner (contact: shengjiex98@gmail.com)",
      "Accept-Encoding": "identity"}
WAYBACK_BANNER = re.compile(
    r"^(The Wayback Machine - .*|success|fail|donate .*|About this capture.*"
    r"|\d[\d,]* captures?|\d{1,2} [A-Z][a-z]{2} \d{4} - \d{1,2} [A-Z][a-z]{2} \d{4}"
    r"|\d{10,})$",  # bare long numbers: session/request ids embedded by some pages
    re.IGNORECASE,
)


class TextExtractor(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "nav", "footer", "header"}

    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0
        self.wm_depth = 0  # inside the Wayback Machine toolbar (id="wm-ipp*")

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip_depth += 1
        if self.wm_depth:
            if tag == "div":
                self.wm_depth += 1
        elif tag == "div" and any(k == "id" and str(v).startswith("wm-") for k, v in attrs):
            self.wm_depth = 1

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip_depth:
            self.skip_depth -= 1
        if tag == "div" and self.wm_depth:
            self.wm_depth -= 1

    def handle_data(self, data):
        if not self.skip_depth and not self.wm_depth and data.strip():
            self.parts.append(data.strip())


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", errors="replace")


def extract_text(html: str) -> str:
    parser = TextExtractor()
    parser.feed(html)
    lines = [ln for ln in parser.parts if not WAYBACK_BANNER.match(ln)]
    return "\n".join(lines)


def normalized_hash(text: str) -> str:
    return hashlib.sha256(re.sub(r"\s+", " ", text).strip().encode()).hexdigest()


def wayback_latest(url: str) -> tuple[str, str] | None:
    """Return (snapshot_url, timestamp) of the newest Wayback capture, if any."""
    api = ("https://archive.org/wayback/available?url="
           + urllib.parse.quote(url, safe="") + "&timestamp=" + dt.date.today().strftime("%Y%m%d"))
    info = json.loads(fetch(api))
    snap = info.get("archived_snapshots", {}).get("closest")
    if snap:
        return snap["url"].replace("http://", "https://"), snap["timestamp"]
    # The availability API is flaky; fall back to following the redirect that
    # web.archive.org/web/<url> issues to the newest capture.
    probe = f"https://web.archive.org/web/{url}"
    req = urllib.request.Request(probe, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            final = resp.geturl()
    except urllib.error.HTTPError:
        return None
    match = re.search(r"/web/(\d{14})", final)
    if not match:
        return None
    return final, match.group(1)


def snapshot_body(path: Path) -> str:
    text = path.read_text()
    return text.split("---\n", 1)[1] if "---\n" in text else text


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    today = dt.date.today().isoformat()
    now = dt.datetime.now().astimezone().isoformat(timespec="seconds")

    with (DATA / "sources.csv").open() as f:
        sources = [row for row in csv.DictReader(f)
                   if row.get("enabled", "TRUE").upper() not in ("FALSE", "0", "NO")]
    state = json.loads((DATA / "state.json").read_text())

    changed, unchanged, failed = [], [], []
    for src in sources:
        slug, url = src["source_slug"], src["source_url"]
        entry = state.setdefault(slug, {"source_name": src["source_name"], "source_url": url})
        use_wayback = "wayback" in src.get("notes", "").lower()
        via = "live"
        try:
            if use_wayback:
                snap = wayback_latest(url)
                if snap is None:
                    raise RuntimeError("no Wayback snapshot available")
                html, via = fetch(snap[0]), f"wayback:{snap[0]}"
            else:
                try:
                    html = fetch(url)
                except urllib.error.HTTPError as err:
                    if err.code != 403:
                        raise
                    snap = wayback_latest(url)
                    if snap is None:
                        raise RuntimeError("live page 403 and no Wayback snapshot") from err
                    html, via = fetch(snap[0]), f"wayback:{snap[0]}"
        except Exception as exc:
            entry.update(last_checked=today, last_status=f"failed: {exc}")
            failed.append((slug, str(exc)))
            print(f"FAILED  {slug}: {exc}")
            continue

        text = extract_text(html)
        digest = normalized_hash(text)
        if digest == entry.get("text_hash"):
            entry.update(last_checked=today, last_status="success")
            unchanged.append(slug)
            print(f"ok      {slug}")
        else:
            first = entry.get("text_hash") is None
            changed.append(slug)
            print(f"CHANGED {slug}" + (" (first capture)" if first else ""))
            if not dry_run:
                snap_dir = DATA / "snapshots" / slug
                snap_dir.mkdir(parents=True, exist_ok=True)
                prev = entry.get("last_snapshot")
                if prev and not (DATA / prev).exists():
                    prev = None
                # Read the previous body before writing: re-scans on the same
                # day overwrite today's file, which would clobber the diff base.
                prev_body = snapshot_body(DATA / prev) if prev else None
                new_path = snap_dir / f"{today}.txt"
                new_path.write_text(
                    f"SOURCE: {src['source_name']}\nURL: {url}\nFETCHED: {now}\nVIA: {via}\n---\n{text}")
                if prev_body is not None:
                    diff = "\n".join(difflib.unified_diff(
                        prev_body.splitlines(), text.splitlines(),
                        fromfile=prev, tofile=f"snapshots/{slug}/{today}.txt", lineterm=""))
                    (snap_dir / f"{today}.diff").write_text(diff + "\n")
                entry.update(
                    text_hash=digest, last_checked=today, last_changed=today,
                    last_snapshot=f"snapshots/{slug}/{today}.txt",
                    last_status="success", note=f"fetched via {via.split(':')[0]}")
        time.sleep(1)

    if not dry_run:
        (DATA / "state.json").write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    print(f"\nScan complete: {len(changed)} changed, {len(unchanged)} unchanged, {len(failed)} failed"
          + (" (dry run, nothing written)" if dry_run else ""))
    if changed:
        print("Changed sources need agent classification: " + ", ".join(changed))


if __name__ == "__main__":
    main()
