---
name: outliers
description: Find a channel's outliers — the videos overperforming that channel's own baseline — then feed the winners into transcription and teardown. Use when the user asks "what's popping off on this channel", "find the outliers", "which videos overperform", "research this creator/niche", or pastes a channel/profile URL wanting to know what works there. Works on YouTube/TikTok directly (yt-dlp) and Instagram via a browser scrape. This is the research loop tools like Poppy AI charge for: catalog → baseline → outliers → why.
---

# Outliers

A channel's median view count is its baseline; anything at 3x+ median is an outlier —
the audience told you what it wants. The interesting output isn't the list, it's the
*pattern across the list* (e.g. AppSumo's channel: every top outlier is a founder
income story; every product demo sits at baseline).

## YouTube / TikTok (direct)

```bash
python3 <skill-dir>/scripts/outliers.py "https://www.youtube.com/@handle/videos" --limit 300
```

- Needs the yt-dlp **CLI** (`brew install yt-dlp`). The python module rots — old
  versions silently omit view counts; if counts come back empty, `brew upgrade yt-dlp`.
- Long-form and Shorts are different games: run `/videos` and `/shorts` separately
  rather than mixing baselines. A bare `@handle` URL auto-descends into both tabs —
  fine for a first look, but call that out when reporting.
- `--threshold 3.0` default; `--out DIR` writes a JSON archive (default `./research/`).

## Instagram (browser scrape → JSON)

Profiles need a logged-in session, so scrape the reels grid with the Chrome DevTools
MCP, then pass the file:

```js
// on https://www.instagram.com/<user>/reels/ — scroll first, then collect
async () => {
  let prev = 0;
  for (let i = 0; i < 20; i++) {
    window.scrollTo(0, document.body.scrollHeight);
    await new Promise(r => setTimeout(r, 1200));
    const n = document.querySelectorAll('a[href*="/reel/"]').length;
    if (n === prev && i > 3) break;
    prev = n;
  }
  return [...document.querySelectorAll('a[href*="/reel/"]')].map(a => ({
    url: a.href,
    views: a.innerText.trim().split('\n')[0]   // grid overlay = view count
  }));
}
```

Save as `entries.json`, then `python3 <skill-dir>/scripts/outliers.py entries.json`.

**Sanity-check the scrape before trusting the output.** Grid tiles that haven't
loaded show junk labels (like-counts, empty strings) that parse as tiny numbers and
poison the median. Rules: drop entries whose views are absurd for the account size
(a 100K-follower account does not have 8-view reels on its grid); if the computed
median looks like nonsense vs follower count, re-scroll and re-scrape. Report how
many entries you dropped and why.

## Then: close the loop

The list is step one. Offer to:
1. **Transcribe the top 3-5 outliers** — the
   [bs-detector skill](https://github.com/chris-jk/claude-bs-detector)'s bundled
   script does it locally.
2. **Name the pattern** — what do the outliers share that baseline videos lack?
   Topic, format, hook shape, title formula. That one sentence is the deliverable.
3. Feed the pattern into the user's own content plan.

Archives land in `./research/` — check for an existing pull of the same channel
before re-fetching; view counts don't move fast enough to justify hammering.
