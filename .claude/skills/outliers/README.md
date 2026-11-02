# Claude Outliers

A Claude skill that finds a channel's outliers — the videos overperforming that
channel's own baseline. Paste a channel URL and it pulls the catalog, takes the
median view count, and flags everything at 3x median and up. Those are the videos
the audience voted for; everything else is the baseline they scroll past.

One command:

```bash
python3 scripts/outliers.py "https://www.youtube.com/@handle/videos" --limit 300
```

Output (illustrative):

```
# Outliers — youtube.com/@handle/videos

catalog: 287 videos with views (13 skipped) | median: 1.8K | max: 113K | threshold: 3.0x

| # | views | x median | title | url |
|---|-------|----------|-------|-----|
| 1 | 113K  | 62.8x    | ...   | ... |
| 2 | 41K   | 22.8x    | ...   | ... |
```

## Why the median

One viral video drags a mean baseline up and hides every other winner. The median
doesn't move, so a 3x flag means "3x what this channel normally does" — which is
the question you actually have. Videos with no view count (private, live,
upcoming) are excluded from the baseline, not zeroed.

The list is step one. The deliverable is the *pattern across the list* — what do
the outliers share that the baseline videos lack? Topic, format, hook shape,
title formula. As a Claude skill, that read is the part Claude does for you.

## Install

**Claude Code / Claude Desktop** — clone straight into your skills directory:

```bash
git clone https://github.com/chris-jk/claude-outliers.git ~/.claude/skills/outliers
brew install yt-dlp
```

Then just ask:

> what's popping off on this channel? https://www.youtube.com/@handle

The script also runs standalone with no Claude anywhere — it's plain Python 3,
stdlib only.

## Platform notes

**YouTube and TikTok** work directly — anything yt-dlp can list. Run `/videos`
and `/shorts` separately; long-form and Shorts are different games and mixing
them poisons the baseline.

**Instagram** can't be listed logged-out. Scrape the reels grid in a real browser
session (snippet in [`SKILL.md`](SKILL.md)), save it as JSON, and pass the file:

```bash
python3 scripts/outliers.py entries.json
```

**If a channel that used to work stops working**, upgrade yt-dlp before debugging
anything else — old versions silently omit view counts. Use the Homebrew CLI, not
`pip install` under macOS's system Python (it's 3.9, and pip quietly installs a
year-stale yt-dlp).

## Close the loop

Outliers tell you *which* videos work. To find out *why*, transcribe the top ones
and tear them down — the [bs-detector skill](https://github.com/chris-jk/claude-bs-detector)
bundles a local transcription script (yt-dlp + Whisper, no API key) and
fact-checks claims while it's at it.

Every run archives to `./research/` as JSON, so repeat pulls of the same channel
are diffable and you're not hammering anyone's servers for numbers that barely
moved.
