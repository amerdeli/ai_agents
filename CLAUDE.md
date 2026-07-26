# CLAUDE.md

## What this is

SAR (Scout — Auditor — Reporter): a multi-agent job search pipeline. It searches job sites via Tavily,
scores listings with Claude, formats a markdown report, and delivers it via Telegram. 

## Setup and commands

```bash
conda create -n ai_agents python=3.11
conda activate ai_agents
pip install -r requirements.txt
```

Required `.env` (repo root):
```
ANTHROPIC_API_KEY=your_key
TAVILY_API_KEY=your_key
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

`sar_system/config_personal.py` holds personal `USER_BACKGROUND`, `SEARCH_QUERIES`, `JOB_SITES` and
overrides the defaults in `sar_system/config.py` via a try/except import at the bottom of that file.
It is gitignored — see `config.py` for the shape to replicate.

Run from the **repo root** (`ai_agents/`), not from `sar_system/`, since everything uses absolute
imports rooted at the repo (`from sar_system...`, `from shared...`):

```bash
python -m sar_system.main            # run the Scout -> Auditor -> Reporter pipeline once
python -m sar_system.telegram_bot    # start the Telegram bot (long-polling)
```

Telegram commands: `/search` (run pipeline), `/status` (last report), `/clear` (reset seen-jobs
memory), `/help`.

There is no test suite, linter, or build step configured in this repo.

## Architecture

Three agents run in a fixed pipeline, orchestrated by `sar_system/main.py:run_pipeline()`:

```
Scout (sar_system/agents/scout.py)
  -> searches JOB_SITES for SEARCH_QUERIES via shared/tools/search.py (Tavily API)
  -> dedupes within the run, then filters out URLs already in data/seen_jobs.json
     via shared/memory.py:filter_new_jobs() (which also updates that file as a side effect)
  -> plain function, no LLM call

Auditor (sar_system/agents/auditor.py)
  -> the only "true" autonomous agent: makes its own Claude API call with a single
     evaluate_jobs tool, forcing structured JSON output (score 1-10 + reason per job)
  -> filters out anything below MIN_RELEVANCE_SCORE (config.py)
  -> uses MODEL_SMART

Reporter (sar_system/agents/reporter.py)
  -> single Claude completion (no tools) that formats scored jobs into markdown
  -> writes data/reports/report_YYYY_MM_DD.md
  -> uses MODEL_FAST
```

`sar_system/telegram_bot.py` is a separate entry point wrapping `run_pipeline()` behind Telegram
command handlers, gated by `is_authorised()` checking `TELEGRAM_CHAT_ID`.

### Shared layer (`shared/`)

Cross-agent infrastructure, imported by both `sar_system` and any future agent systems in this repo:
- `shared/llm_client.py` — single module-level `Anthropic` client instance (`client`), imported by
  every agent that calls the LLM. Don't instantiate a second client.
- `shared/memory.py` — flat-file JSON persistence (`data/seen_jobs.json`) for cross-run job
  deduplication. Not a database; read/modify/write of the whole file on every call.
- `shared/tools/search.py` — Tavily wrapper (`search_jobs`), scoped to `JOB_SITES` from config.

### Config

`sar_system/config.py` defines paths (all derived from `BASE_DIR = repo root`), model IDs
(`MODEL_FAST` / `MODEL_SMART`), token limits, and default search settings, then attempts to import
`sar_system/config_personal.py` to override `USER_BACKGROUND` / `SEARCH_QUERIES` / `JOB_SITES`.
`USER_BACKGROUND` is interpolated directly into the Auditor's system prompt, so it drives scoring
behavior — treat it as prompt content, not just metadata.

### Data flow

Job listing dicts flow through the pipeline with an evolving shape: Scout/search produce
`{title, url, description}`; the Auditor adds `score` and `reason` (and the LLM restates
`title`/`url`, so downstream code reads them off the Auditor's tool output, not the original Scout
dict). Reports are plain markdown files in `data/reports/`, one per day, overwritten if the
pipeline runs more than once on the same date.
