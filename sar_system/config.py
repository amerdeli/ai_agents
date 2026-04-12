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
MAX_TOKENS = 1024

# ─────────────────────────────────────────
# Search settings
# ─────────────────────────────────────────
SEARCH_TIME_RANGE = "week"
MAX_RESULTS_PER_QUERY = 5

JOB_SITES = [
    "linkedin.com",
    "at.indeed.com",
    "stepstone.at",
    "karriere.at",
    "jobs.at",
    #"weworkremotely.com",
    #"remoteok.com"
    "welcometothejungle.com",
]

SEARCH_QUERIES = [
    #"Python AI engineer",
    "AI engineer",
    "Machine learning engineer",
    "Data Scientist",
    #"Data Engineer",
    #"Data Analyst",
    #"AI developer Python",
    #"AI developer"
]

# ─────────────────────────────────────────
# Auditor settings
# ─────────────────────────────────────────
MIN_RELEVANCE_SCORE = 5    # Auditor filters anything below this

# ─────────────────────────────────────────
# User background (fed into agent prompts)
# ─────────────────────────────────────────
USER_BACKGROUND = """
The user is a mid-level software engineer transitioning into AI/data engineering. The user has a master's degree in 
Electrical Engineering and is currently completing master's extension programme in Artificial Intelligence Engineering.

Current skills:
- Embedded software development
- Automotive software development using Matlab/Simulink (model-based development)
- Python (intermediate level)
- Machine learning fundamentals (regression, classification, clustering)
- Deep learning (CNNs, classical NNs, GPT project)
- Reinforcement learning
- Git

Looking for:
- Part-time and/or full-time AI/ML/data engineering roles
- Preferably Python-focused roles
- Remote or Austria/Germany based

Strong fit indicators:
- Python required
- AI, ML, data engineering, LLMs, agents, agentic AI
- Remote friendly
- Junior to mid level

Poor fit indicators:
- On-site only outside Austria/Germany
- Requires 3+ years AI/ML experience
- Primarily Java, C++, or other non-Python languages
- Pure frontend development
"""