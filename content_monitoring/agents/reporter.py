# content_monitoring/agents/reporter.py
import json
from datetime import datetime
from shared.llm_client import client
from content_monitoring.config import (
    MODEL_FAST,
    MAX_TOKENS_FAST,
    DIGESTS_DIR
)


REPORTER_SYSTEM_PROMPT = """
You are the Reporter agent in a content monitoring pipeline.

Your job is to take a list of summarised news articles and YouTube
videos and format them into a clean, readable daily digest in
markdown format.

Rules:
- Group items by source_type: News and YouTube
- For each item write: title, one-line summary and URL
- Keep it scannable — this digest gets sent as a Telegram message
- Use a neutral, informative tone
- If no items are provided, write a short friendly message saying
  no new content was found today

Output format:
Return ONLY the markdown content — no extra explanation!
"""


def run_reporter(summarised_items: list[dict]) -> str:
    """
    Reporter agent — formats summarised content items into a
    clean markdown digest and saves it to disk.
    Returns the path to the saved digest file.
    """
    print("\n📋 Reporter starting...")

    # Generate today's digest filename
    today = datetime.now().strftime("%Y_%m_%d")
    digest_filename = f"digest_{today}.md"

    # Make sure digests directory exists
    DIGESTS_DIR.mkdir(parents=True, exist_ok=True)
    digest_path = DIGESTS_DIR / digest_filename

    # Format items as clean text for the LLM
    if summarised_items:
        items_text = json.dumps(summarised_items, indent=2)
    else:
        items_text = "No items to report today."

    # Build Reporter's context window
    messages = [
        {
            "role": "user",
            "content": (
                f"Please format these summarised content items "
                f"into a daily digest:\n\n{items_text}"
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
    digest_content = response.content[0].text

    # Add a header with date and stats
    header = (
        f"# Content Digest — {datetime.now().strftime('%B %d, %Y')}\n"
        f"*Generated at {datetime.now().strftime('%H:%M')} | "
        f"{len(summarised_items)} new items found*\n\n"
        f"---\n\n"
    )

    full_digest = header + digest_content

    # Save digest to disk
    with open(digest_path, "w", encoding="utf-8") as f:
        f.write(full_digest)

    print(f"   Digest saved to: {digest_path}")
    print("✅ Reporter done!\n")

    return str(digest_path)
