from pathlib import Path

# ─────────────────────────────────────────
# Paths
# ─────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent   # points to ai_agents/
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = DATA_DIR / "reports"
SEEN_JOBS_FILE = DATA_DIR / "seen_jobs.json"

# ─────────────────────────────────────────
# Models
# ─────────────────────────────────────────
MODEL_FAST = "claude-haiku-4-5-20251001"    # Scout + Reporter
MODEL_SMART = "claude-sonnet-4-6"           # Auditor
MAX_TOKENS_FAST = 1024
MAX_TOKENS_SMART = 4096

# ─────────────────────────────────────────
# Auditor settings
# ─────────────────────────────────────────
MIN_RELEVANCE_SCORE = 5    # Auditor filters anything below this

# ─────────────────────────────────────────
# Search settings and user background 
# ─────────────────────────────────────────
SEARCH_TIME_RANGE = "week"
MAX_RESULTS_PER_QUERY = 5

# Defaults — overridden by config.personal.py
USER_BACKGROUND = """ Senior software engineer looking for a new role with focus on AI engineering."""
SEARCH_QUERIES = ["AI Engineer"]
JOB_SITES = ["linkedin.com"]

# Import personal settings if exist
try:
    from sar_system.config_personal import (
        USER_BACKGROUND,
        SEARCH_QUERIES,
        JOB_SITES
    )
except ImportError:
    pass  