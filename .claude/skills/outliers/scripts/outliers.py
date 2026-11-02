#!/usr/bin/env python3
"""Find a channel's outliers: videos overperforming the channel's own baseline.

Usage:
  python3 outliers.py <channel-url> [options]     # YouTube/TikTok/anything yt-dlp lists
  python3 outliers.py <entries.json> [options]    # pre-scraped [{url, views, title?}, ...]

Options:
  --threshold N   flag videos at >= N x the channel median (default 3.0)
  --limit N       max catalog entries to pull (default 300)
  --out DIR       where the JSON archive lands (default ./research)

The baseline is the MEDIAN of the catalog's view counts, not the mean — one viral
video would drag a mean baseline up and hide every other winner. Videos with no
view count (private, live, upcoming) are excluded from the baseline, not zeroed.

The JSON entry path exists because Instagram profiles can't be listed logged-out:
scrape the grid in a real browser session (see SKILL.md for the snippet), save
[{"url": "...", "views": "22.4K"}, ...] and pass the file. "22.4K"/"1.2M" strings
are parsed.
"""

import json
import re
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_views(v):
    """Accept 22400, '22,400', '22.4K', '1.2M'. Return int or None."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return int(v)
    s = str(v).strip().replace(",", "")
    m = re.fullmatch(r"([\d.]+)\s*([KkMmBb]?)", s)
    if not m:
        return None
    n = float(m.group(1))
    mult = {"": 1, "k": 1_000, "m": 1_000_000, "b": 1_000_000_000}[m.group(2).lower()]
    return int(n * mult)


def entries_from_json(path):
    raw = json.loads(Path(path).read_text())
    if isinstance(raw, dict):  # tolerate {"links": [...]} / {"reels": [...]} wrappers
        for key in ("entries", "reels", "links", "videos", "items"):
            if key in raw:
                raw = raw[key]
                break
    out = []
    for e in raw:
        out.append({
            "url": e.get("url") or e.get("href") or "",
            "title": (e.get("title") or e.get("label") or e.get("caption") or "")[:90],
            "views": parse_views(e.get("views") or e.get("label")),
        })
    return out


def entries_from_url(url, limit):
    # The yt-dlp CLI, not the python module: system-python yt_dlp installs go stale
    # (old versions omit view_count from flat entries) while brew keeps the CLI current.
    import shutil
    import subprocess
    if not shutil.which("yt-dlp"):
        sys.exit("yt-dlp CLI not found: brew install yt-dlp")

    def flat(u):
        r = subprocess.run(
            ["yt-dlp", "-J", "--flat-playlist", "--playlist-end", str(limit), u],
            capture_output=True, text=True, timeout=300,
        )
        if r.returncode != 0:
            sys.exit(f"yt-dlp failed on {u}: {r.stderr.strip().splitlines()[-1] if r.stderr else 'unknown error'}")
        return json.loads(r.stdout)

    info = flat(url)
    entries = list(info.get("entries") or [])

    # A bare @handle returns the channel's tab playlists (Videos / Shorts / Live)
    # instead of videos. Descend one level into tabs that themselves are playlists.
    if entries and all(e.get("view_count") is None for e in entries):
        tabs = [e for e in entries if (e.get("url") or "").rstrip("/").endswith(("/videos", "/shorts"))]
        if tabs:
            entries = []
            for tab in tabs:
                sub = flat(tab["url"])
                for e in sub.get("entries") or []:
                    e["_tab"] = tab["url"].rsplit("/", 1)[-1]
                    entries.append(e)

    out = []
    for e in entries:
        if not e:
            continue
        out.append({
            "url": e.get("url") or e.get("webpage_url") or "",
            "title": (e.get("title") or "")[:90],
            "views": e.get("view_count"),
            "duration": e.get("duration"),
            "tab": e.get("_tab"),
        })
    return out


def fmt(n):
    if n is None:
        return "—"
    for cut, suf in ((1_000_000_000, "B"), (1_000_000, "M"), (1_000, "K")):
        if n >= cut:
            return f"{n / cut:.1f}{suf}"
    return str(n)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    src = args[0]

    def opt(name, default):
        for i, a in enumerate(sys.argv):
            if a == f"--{name}" and i + 1 < len(sys.argv):
                return sys.argv[i + 1]
        return default

    threshold = float(opt("threshold", 3.0))
    limit = int(opt("limit", 300))
    outdir = Path(opt("out", "./research"))

    if src.endswith(".json") and Path(src).exists():
        entries, source = entries_from_json(src), src
    else:
        entries, source = entries_from_url(src, limit), src

    counted = [e for e in entries if e.get("views")]
    skipped = len(entries) - len(counted)
    if len(counted) < 5:
        sys.exit(f"only {len(counted)} entries with view counts — not enough for a baseline "
                 f"({skipped} entries had none). For Instagram, scrape the grid per SKILL.md.")

    median = statistics.median(e["views"] for e in counted)
    for e in counted:
        e["ratio"] = round(e["views"] / median, 2) if median else None
    counted.sort(key=lambda e: e["ratio"], reverse=True)
    outliers = [e for e in counted if e["ratio"] >= threshold]

    print(f"\n# Outliers — {source}")
    print(f"\ncatalog: {len(counted)} videos with views ({skipped} skipped) | "
          f"median: {fmt(median)} | max: {fmt(counted[0]['views'])} | "
          f"threshold: {threshold}x\n")
    print(f"| # | views | x median | title | url |")
    print(f"|---|-------|----------|-------|-----|")
    show = outliers if outliers else counted[:10]
    for i, e in enumerate(show, 1):
        print(f"| {i} | {fmt(e['views'])} | {e['ratio']}x | {e['title']} | {e['url']} |")
    if not outliers:
        print(f"\nNo videos at >= {threshold}x median — flat channel. Top 10 shown instead.")
    else:
        floor = [e for e in counted if e["ratio"] <= 0.2]
        if floor:
            print(f"\n{len(floor)} videos at <= 0.2x median (the floor — worth knowing "
                  f"what this channel's audience ignores).")

    outdir.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", source.lower())[-60:].strip("-")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    dest = outdir / f"outliers-{slug}-{stamp}.json"
    dest.write_text(json.dumps({
        "source": source, "fetched_at": stamp, "median": median,
        "threshold": threshold, "count": len(counted),
        "entries": counted,
    }, indent=1))
    print(f"\narchive: {dest}")


if __name__ == "__main__":
    main()
