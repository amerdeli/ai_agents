# content_monitoring/agents/summariser.py
from shared.llm_client import client
from content_monitoring.config import MODEL_SMART, MAX_TOKENS_SMART


SUMMARISER_SYSTEM_PROMPT = """
You are the Summariser agent in a content monitoring pipeline.

Your job is to read new articles and YouTube videos and write a
short, clear summary of each one — what it's about and why it
might be worth reading or watching.

Rules:
- One to two sentences per item, no more
- Focus on the new information, not generic descriptions
- Neutral, informative tone

You have one tool available: summarise_items
Use it ONCE with ALL items at the same time.
Return your evaluation as a JSON list — nothing else.
"""


def summarise_items_tool_definition() -> dict:
    """
    Tool definition for the Summariser's summarise_items tool.
    The LLM calls this to return its structured summaries.
    """
    return {
        "name": "summarise_items",
        "description": (
            "Submit your summary of all content items. "
            "Call this once with all summarised items."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "summaries": {
                    "type": "array",
                    "description": "List of summarised content items",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Item title"
                            },
                            "url": {
                                "type": "string",
                                "description": "Item URL"
                            },
                            "source_type": {
                                "type": "string",
                                "description": "Either 'news' or 'youtube'"
                            },
                            "summary": {
                                "type": "string",
                                "description": "One to two sentence summary"
                            }
                        },
                        "required": ["title", "url", "source_type", "summary"]
                    }
                }
            },
            "required": ["summaries"]
        }
    }


def run_summariser(raw_items: list[dict]) -> list[dict]:
    """
    Summariser agent — writes a short summary for each new item.
    raw_items must already carry a "source_type" key ("news" or "youtube"),
    set by main.py when it combines the monitors' output.
    This is a TRUE autonomous agent — it makes its own LLM API call!
    """
    if not raw_items:
        print("   No items to summarise!")
        return []

    print(f"\n✍️  Summariser starting — summarising {len(raw_items)} items...")

    # Format items as readable text for the LLM
    items_text = "\n\n".join([
        f"Item {i+1}:\n"
        f"Source: {item.get('source_type', 'N/A')}\n"
        f"Title: {item.get('title', 'N/A')}\n"
        f"URL: {item.get('url', 'N/A')}\n"
        f"Description: {item.get('description', 'N/A')[:300]}..."
        for i, item in enumerate(raw_items)
    ])

    # Build the Summariser's context window
    messages = [
        {
            "role": "user",
            "content": f"Please summarise these content items:\n\n{items_text}"
        }
    ]

    # ─── THE AGENT LOOP ───────────────────────────────────────────
    while True:

        # THINK — LLM API call
        response = client.messages.create(
            model=MODEL_SMART,
            max_tokens=MAX_TOKENS_SMART,
            system=SUMMARISER_SYSTEM_PROMPT,
            messages=messages,
            tools=[summarise_items_tool_definition()]
        )

        # ACT — check what LLM decided
        if response.stop_reason == "end_turn":
            # LLM responded with text instead of tool call
            print("   Summariser responded with text instead of tool call!")
            return []

        elif response.stop_reason == "tool_use":
            # LLM called the summarise_items tool —> extract results
            tool_use_block = next(
                block for block in response.content
                if block.type == "tool_use"
            )

            summaries = tool_use_block.input.get("summaries", [])

            print(f"   Summarised {len(summaries)} items")
            print("✅ Summariser done!\n")

            return summaries

        # Safety — if neither end_turn nor tool_use, break
        break

    return []
