# SAR — Scout Auditor Reporter

An automated job search multi-agent system that searches the web
for relevant job listings, evaluates them using AI and delivers
a formatted report directly to your Telegram.

## How it works

```
Scout → Auditor → Reporter → Telegram
```

- **Scout** — searches job sites via Tavily, filters seen listings
- **Auditor** — scores each listing 1-10 using Claude Sonnet
- **Reporter** — formats results and delivers via Telegram

## Tech stack
- Python 3.11, Anthropic API, Tavily, python-telegram-bot

## Setup

```bash
git clone https://github.com/amerdeli/ai_agents.git
cd ai_agents
conda create -n ai_agents python=3.11
conda activate ai_agents
pip install -r requirements.txt
```

Create `.env`:
```
ANTHROPIC_API_KEY=your_key
TAVILY_API_KEY=your_key
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

Create `sar_system/config_personal.py` with your `USER_BACKGROUND`,
`SEARCH_QUERIES` and `JOB_SITES` — see `config.py` for reference!

## Usage

```bash
# Run pipeline manually
python -m sar_system.main

# Start Telegram bot
python -m sar_system.telegram_bot
```

**Telegram commands:** `/search` `/status` `/clear` `/help`

## Concepts demonstrated
- Multi-agent pipeline architecture
- Anthropic tool use for structured LLM output
- External memory for cross-run deduplication
- Workflow vs autonomous agent patterns

## License
MIT