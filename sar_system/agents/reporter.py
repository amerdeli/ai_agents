import json
from datetime import datetime
from pathlib import Path
from shared.llm_client import client
from sar_system.config import (
    MODEL_FAST,
    MAX_TOKENS_FAST,
    REPORTS_DIR
)


REPORTER_SYSTEM_PROMPT = """
You are the Reporter agent in a job search pipeline.

Your job is to take a list of evaluated job listings and format
them into a clean, readable daily report in markdown format.

Rules:
- Group jobs by score: Top Matches (8-10), Good Fits (5-7)
- For each job write: title, company if available, score, URL and reason
- Keep descriptions concise — one sentence per job maximum
- Use encouraging but professional tone
- If no jobs are provided, write a short friendly message saying
  no new relevant jobs were found today

Output format:
Return ONLY the markdown content — no extra explanation!
"""


def run_reporter(scored_jobs: list[dict]) -> str:
    """
    Reporter agent — formats scored job listings into a
    clean markdown report and saves it to disk.
    Returns the path to the saved report file.
    """
    print("\n📊 Reporter starting...")

    # Generate today's report filename
    today = datetime.now().strftime("%Y_%m_%d")
    report_filename = f"report_{today}.md"

    # Make sure reports directory exists
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / report_filename

    # Format jobs as clean text for the LLM
    if scored_jobs:
        jobs_text = json.dumps(scored_jobs, indent=2)
    else:
        jobs_text = "No jobs to report today."

    # Build Reporter's context window
    messages = [
        {
            "role": "user",
            "content": (
                f"Please format these evaluated job listings "
                f"into a daily report:\n\n{jobs_text}"
            )
        }
    ]

    # ─ LLM API CALL
    response = client.messages.create(
        model=MODEL_FAST,
        max_tokens=MAX_TOKENS_FAST,
        system=REPORTER_SYSTEM_PROMPT,
        messages=messages
    )

    # Extract the markdown content from response
    report_content = response.content[0].text

    # Add a header with date and stats
    header = (
        f"# Daily Job Report — {datetime.now().strftime('%B %d, %Y')}\n"
        f"*Generated at {datetime.now().strftime('%H:%M')} | "
        f"{len(scored_jobs)} relevant listings found*\n\n"
        f"---\n\n"
    )

    full_report = header + report_content

    # Save report to disk
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(full_report)

    print(f"   Report saved to: {report_path}")
    print("✅ Reporter done!\n")

    return str(report_path)
