# CLAUDE.md — ai_agents monorepo

This is a personal AI engineering monorepo. Each subdirectory
is a standalone agent system. Shared infrastructure lives in
shared/ and is reused across all projects.

## Monorepo structure

ai_agents/
├── shared/                  # reusable across ALL projects
│   ├── llm_client.py        # single Anthropic client — always import, never reinstantiate
│   ├── memory.py            # flat-file JSON persistence for deduplication
│   └── tools/
│       └── search.py        # Tavily web search wrapper
├── sar_system/              # job search multi-agent pipeline
└── content_monitoring/      # YouTube and news monitoring agent

## Running projects

Always run from the repo root (ai_agents/) using the -m flag.
Never run files directly — it breaks absolute imports!

```bash
# correct ✅
python -m sar_system.main
python -m sar_system.telegram_bot
python -m content_monitor.main

# wrong ❌
python sar_system/main.py
```

## Coding conventions

- Type hints on all functions
- Use pathlib.Path for file paths — never plain strings
- try/except on all external API calls — never let the pipeline crash
- System prompts as module-level constants
- Tool definitions as separate functions

### Keep code simple and readable

Prioritise clarity over cleverness:

- Break complex operations into multiple lines with clear variable names
- Avoid one-liner list comprehensions when a simple for loop is clearer
- No nested list comprehensions
- No lambda functions — use a regular def instead
- Prefer explicit variable names over short cryptic ones

## Environment and secrets

- API keys in .env at repo root — never commit!
- Personal config in config_personal.py — never commit!
- data/ folder is gitignored — never commit reports or memory files
- conda environment: ai_agents (Python 3.11)

## Adding a new project

1. Create new folder alongside sar_system/
2. Add __init__.py where needed
3. Import from shared/ — never copy paste shared code!
4. Run /init to generate project-level CLAUDE.md
5. Refine the generated CLAUDE.md before starting to build

## Git conventions

- Commit messages in imperative form: "Add", "Fix", "Update"
- Never commit: .env, config_personal.py, data/, __pycache__/
- Always test before committing
- Each project has its own README.md