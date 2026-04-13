from shared.llm_client import client
from sar_system.config import (
    MODEL_SMART,
    MAX_TOKENS,
    MIN_RELEVANCE_SCORE,
    USER_BACKGROUND
)


AUDITOR_SYSTEM_PROMPT = f"""
You are the Auditor agent in a job search pipeline.

Your job is to evaluate each job listing and decide if it is
relevant for the user. You must score each job from 1 to 10.

{USER_BACKGROUND}

Scoring guide:
- 8-10: Excellent fit — strong Python + AI/ML focus, remote friendly
- 5-7:  Decent fit — some relevant skills, worth considering  
- 1-4:  Poor fit — wrong stack, wrong location, too much experience needed

You have one tool available: evaluate_jobs
Use it ONCE with ALL listings at the same time.
Return your evaluation as a JSON list — nothing else.
"""


def evaluate_jobs_tool_definition() -> dict:
    """
    Tool definition for the Auditor's evaluate_jobs tool.
    The LLM calls this to return its structured evaluation.
    """
    return {
        "name": "evaluate_jobs",
        "description": (
            "Submit your evaluation of all job listings. "
            "Call this once with all scored jobs."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "evaluations": {
                    "type": "array",
                    "description": "List of evaluated job listings",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Job title"
                            },
                            "url": {
                                "type": "string",
                                "description": "Job URL"
                            },
                            "score": {
                                "type": "integer",
                                "description": "Relevance score 1-10"
                            },
                            "reason": {
                                "type": "string",
                                "description": "One sentence why this score"
                            }
                        },
                        "required": ["title", "url", "score", "reason"]
                    }
                }
            },
            "required": ["evaluations"]
        }
    }


def run_auditor(raw_jobs: list[dict[str, str]]) -> list[dict]:
    """
    Auditor agent — evaluates and scores raw job listings.
    Returns only jobs scoring above MIN_RELEVANCE_SCORE.
    This is a TRUE autonomous agent — it makes its own LLM API call!
    """
    if not raw_jobs:
        print("   No jobs to evaluate!")
        return []

    print(f"\n⚖️  Auditor starting — evaluating {len(raw_jobs)} listings...")

    # Format job listings as readable text for the LLM
    jobs_text = "\n\n".join([
        f"Job {i+1}:\n"
        f"Title: {job.get('title', 'N/A')}\n"
        f"URL: {job.get('url', 'N/A')}\n"
        f"Description: {job.get('description', 'N/A')[:300]}..."
        for i, job in enumerate(raw_jobs)
    ])

    # Build the messages list — Auditor's context window starts here!
    messages = [
        {
            "role": "user",
            "content": f"Please evaluate these job listings:\n\n{jobs_text}"
        }
    ]

    # ─── THE AGENT LOOP ───────────────────────────────────────────
    while True:

        # THINK — LLM API call
        response = client.messages.create(
            model=MODEL_SMART,
            max_tokens=MAX_TOKENS,
            system=AUDITOR_SYSTEM_PROMPT,
            messages=messages,
            tools=[evaluate_jobs_tool_definition()]
        )

        # ACT — check what LLM decided
        if response.stop_reason == "end_turn":
            # LLM responded with text instead of tool call
            # This shouldn't happen — but handle it gracefully!
            print("   Auditor responded with text instead of tool call!")
            return []

        elif response.stop_reason == "tool_use":
            # LLM called the evaluate_jobs tool — extract results!
            tool_use_block = next(
                block for block in response.content
                if block.type == "tool_use"
            )

            evaluations = tool_use_block.input.get("evaluations", [])

            # Filter by minimum relevance score
            filtered = [
                job for job in evaluations
                if job.get("score", 0) >= MIN_RELEVANCE_SCORE
            ]

            print(f"   Evaluated {len(evaluations)} jobs")
            print(f"   {len(filtered)} passed minimum score ({MIN_RELEVANCE_SCORE}+)")
            print("✅ Auditor done!\n")

            return filtered

        # Safety — if neither end_turn nor tool_use, break
        break

    return []


# Temporary test — remove after confirming it works!
if __name__ == "__main__":
    fake_jobs = [
        {
            "title": "Python AI Engineer — Remote",
            "url": "https://linkedin.com/jobs/1",
            "description": "We are looking for a Python developer with ML experience to build AI pipelines. Remote friendly. Experience with LLMs a plus."
        },
        {
            "title": "Java Backend Developer — On-site Vienna",
            "url": "https://karriere.at/jobs/2",
            "description": "Senior Java developer needed for enterprise banking application. 5+ years Java required. On-site only."
        },
        {
            "title": "Data Scientist — Hybrid Graz",
            "url": "https://stepstone.at/jobs/3",
            "description": "Data scientist with Python and ML skills. Work on predictive models. Hybrid work possible from Graz."
        }
    ]

    results = run_auditor(fake_jobs)
    print(f"\nPassed jobs ({len(results)} total):")
    for job in results:
        print(f"  [{job['score']}/10] {job['title']}")
        print(f"   → {job['reason']}")
        print()