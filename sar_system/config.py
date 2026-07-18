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
# Search settings
# ─────────────────────────────────────────
SEARCH_TIME_RANGE = "week"
MAX_RESULTS_PER_QUERY = 5

JOB_SITES = [
    #"linkedin.com",
    "devjobs.at",
    "at.indeed.com",
    #"stepstone.at",
    "karriere.at",
    #"jobs.at",
    #"weworkremotely.com",
    #"remoteok.com"
    "welcometothejungle.com",
]

SEARCH_QUERIES = [
    #"Software",
    #"AI",
    #"Data",
    "Software Engineer",
    "AI engineer",
    "Data Engineer"
    #"Machine learning",
]

# ─────────────────────────────────────────
# Auditor settings
# ─────────────────────────────────────────
MIN_RELEVANCE_SCORE = 5    # Auditor filters anything below this

# ─────────────────────────────────────────
# User background (fed into agent prompts)
# ─────────────────────────────────────────
USER_BACKGROUND = """
The user is a mid-level software engineer actively looking for a
new role with focus on software development and testing.
Transitioning into AI/data engineering is strongly desired.

Education:
- Master's degree in Electrical Engineering
- Two-semester AI Engineering certificate programme
  (currently completing — covers ML, deep learning, LLMs, agents)

Current skills:
- Embedded software development
- Python (intermediate level)
- C and Matlab/Simulink
- Machine learning fundamentals (regression, classification, clustering)
- Deep learning (CNNs, classical NNs, GPT project)
- Reinforcement learning
- Git

Looking for:
- Part-time and/or full-time software engineering roles
- Preferably Python-focused roles
- Remote or Austria/Germany based

Strong fit indicators:
- Python required
- AI, ML, data engineering, LLMs, agents, agentic AI
- Remote friendly
- Junior to mid level (also senior if good fit)

Poor fit indicators:
- On-site only outside Austria/Germany
- Requires 5+ years experience in a specific domain
- Primarily Java, C++, or other non-Python languages
- Pure frontend development
- Purely managerial with no technical component
"""