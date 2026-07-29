from pathlib import Path

# ─────────────────────────────────────────
# Paths
# ─────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent   # points to ai_agents/
DATA_DIR = BASE_DIR / "data" / "content_monitoring"
DIGESTS_DIR = DATA_DIR / "digests"
SEEN_ARTICLES_FILE = DATA_DIR / "seen_articles.json"
SEEN_VIDEOS_FILE = DATA_DIR / "seen_videos.json"

# ─────────────────────────────────────────
# Models
# ─────────────────────────────────────────
MODEL_FAST = "claude-haiku-4-5-20251001"    # Reporter
MODEL_SMART = "claude-sonnet-5"             # Summariser
MAX_TOKENS_FAST = 1024
MAX_TOKENS_SMART = 4096

# ─────────────────────────────────────────
# News monitor settings
# ─────────────────────────────────────────
SEARCH_TIME_RANGE = "week"
MAX_RESULTS_PER_QUERY = 5

# ─────────────────────────────────────────
# YouTube monitor settings
# ─────────────────────────────────────────
MAX_VIDEOS_PER_CHANNEL = 5

# Defaults — overridden by config_personal.py
NEWS_SITES = ["techcrunch.com"]
NEWS_QUERIES = ["AI engineering"]
YOUTUBE_CHANNELS = []   # list of YouTube channel IDs, e.g. "UC_x5XG1OV2P6uZZ5FSM9Ttw"

# Import personal settings if they exist
try:
    from content_monitoring.config_personal import (
        NEWS_SITES,
        NEWS_QUERIES,
        YOUTUBE_CHANNELS
    )
except ImportError:
    pass
