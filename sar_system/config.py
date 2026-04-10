# config.py — all your settings in one place
ANTHROPIC_MODEL_FAST = "claude-haiku-4-5-20251001"   # Scout + Reporter
ANTHROPIC_MODEL_SMART = "claude-sonnet-4-6"           # Auditor
TAVILY_MAX_RESULTS = 10
MIN_RELEVANCE_SCORE = 5    # Auditor filters below this
DATA_DIR = "data/"
SEEN_JOBS_FILE = "data/seen_jobs.json"
REPORTS_DIR = "data/reports/"
USE_BATCH_API = False

SEARCH_CRITERIA = {
    "keywords": ["Python AI engineer", "data scientist remote",
                 "ML engineer", "AI developer"],
    "locations": ["remote", "Austria", "Germany"],
    "languages": ["English", "German"]
}