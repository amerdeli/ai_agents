# CLAUDE.md

## What this is

Content Monitoring: a multi-agent pipeline that checks news sites and YouTube channels for
fresh content, summarises new items with Claude, formats a digest, and delivers it via Telegram.
Sibling project to `sar_system/` in this monorepo — see the root `CLAUDE.md` for repo-wide
conventions (this file only covers what's specific to this project).

## Setup and commands

Required `.env` additions (repo root, alongside sar_system's keys):
```
YOUTUBE_API_KEY=your_key
CONTENT_MONITOR_BOT_TOKEN=your_token
```
Reuses `TAVILY_API_KEY`, `ANTHROPIC_API_KEY` and `TELEGRAM_CHAT_ID` from the existing `.env` —
this bot posts to the same Telegram chat as sar_system, just under a second bot token.

`content_monitoring/config_personal.py` holds personal `NEWS_SITES`, `NEWS_QUERIES`,
`YOUTUBE_CHANNELS` and overrides the defaults in `content_monitoring/config.py` via a
try/except import at the bottom of that file. It is gitignored — see `config.py` for the
shape to replicate.

Run from the **repo root** (`ai_agents/`):

```bash
python -m content_monitoring.main            # run the pipeline once
python -m content_monitoring.telegram_bot    # start the Telegram bot (long-polling)
```

Telegram commands: `/check` (run pipeline), `/status` (last digest), `/clear` (reset seen
articles + seen videos), `/help`.

There is no test suite, linter, or build step configured for this project.

## Architecture

Four steps run in a fixed pipeline, orchestrated by `content_monitoring/main.py:run_pipeline()`:

```
News monitor (content_monitoring/monitors/news_monitor.py)
  -> searches NEWS_SITES for NEWS_QUERIES via shared/tools/search.py:search_news() (Tavily API)
  -> dedupes within the run, then filters out URLs already in
     data/content_monitoring/seen_articles.json via shared/memory.py:filter_new_articles()
  -> plain function, no LLM call

YouTube monitor (content_monitoring/monitors/youtube_monitor.py)
  -> queries the YouTube Data API v3 search endpoint directly via requests (no client library)
     for each channel in YOUTUBE_CHANNELS
  -> dedupes within the run, then filters out URLs already in
     data/content_monitoring/seen_videos.json via shared/memory.py:filter_new_videos()
  -> plain function, no LLM call

main.py tags each monitor's output with source_type ("news" / "youtube") before combining them —
this is the only place that happens, since the monitors don't know about each other.

Summariser (content_monitoring/agents/summariser.py)
  -> the only "true" autonomous agent: makes its own Claude API call with a single
     summarise_items tool, forcing structured JSON output (title, url, source_type, summary
     per item). The LLM must echo back source_type since it's the tool call's only output.
  -> does not filter anything (unlike sar_system's Auditor) — every new item gets summarised
  -> uses MODEL_SMART (claude-sonnet-5)

Reporter (content_monitoring/agents/reporter.py)
  -> single Claude completion (no tools) that formats summarised items into a markdown digest,
     grouped by source_type
  -> writes data/content_monitoring/digests/digest_YYYY_MM_DD.md
  -> uses MODEL_FAST (claude-haiku-4-5-20251001)
```

`content_monitoring/telegram_bot.py` is a separate entry point wrapping `run_pipeline()` behind
Telegram command handlers, gated by `is_authorised()` checking `TELEGRAM_CHAT_ID`.

### Shared layer usage

This project extends (rather than genericizes) the existing `shared/` modules, so they stay
directly comparable to their sar_system counterparts:
- `shared/tools/search.py` — `search_news()` sits alongside `search_jobs()`, same Tavily client,
  scoped to `NEWS_SITES` / `SEARCH_TIME_RANGE` from `content_monitoring.config`.
- `shared/memory.py` — `load_seen_articles` / `save_seen_articles` / `filter_new_articles` /
  `clear_seen_articles`, and the equivalent `*_videos` functions, sit alongside the existing
  `*_jobs` functions. Each set is hardcoded to its own file path/config import — none of these
  functions take a file path as a parameter. If a third project needs the same pattern, add
  another parallel set rather than trying to generalize the existing ones.
- `shared/llm_client.py` — same single `Anthropic` client instance as sar_system.

### Config

`content_monitoring/config.py` defines paths (`DATA_DIR = BASE_DIR / "data" / "content_monitoring"`,
namespaced so it can't collide with sar_system's `data/seen_jobs.json` or `data/reports/`), model
IDs, and default `NEWS_SITES` / `NEWS_QUERIES` / `YOUTUBE_CHANNELS`, then attempts to import
`content_monitoring/config_personal.py` to override those three lists.

### Data flow

Items flow through the pipeline with an evolving shape: `news_monitor` produces
`{title, url, description}`, `youtube_monitor` produces `{title, url, description, channel}`.
`main.py` adds `source_type` to both before combining. The Summariser's tool output restates
`title`, `url` and `source_type` (plus adds `summary`), so `reporter.py` reads everything off the
Summariser's output, not the original monitor dicts. Digests are plain markdown files in
`data/content_monitoring/digests/`, one per day, overwritten if the pipeline runs more than once
on the same date.

### Not yet implemented

YouTube dedup, config and monitor code all exist and are wired into `main.py`, but no channel IDs
are set by default — add real channel IDs to `YOUTUBE_CHANNELS` in `config_personal.py` to
actually pull videos.
