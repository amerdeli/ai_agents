from datetime import datetime
from content_monitoring.monitors.news_monitor import run_news_monitor
from content_monitoring.monitors.youtube_monitor import run_youtube_monitor
from content_monitoring.agents.summariser import run_summariser
from content_monitoring.agents.reporter import run_reporter


def run_pipeline() -> str | None:
    """
    Main orchestrator — runs the full content monitoring pipeline:
    News monitor + YouTube monitor -> Summariser -> Reporter
    """
    print("\n" + "="*50)
    print("🚀 Content Monitoring Pipeline starting...")
    print(f"   {datetime.now().strftime('%B %d, %Y — %H:%M')}")
    print("="*50 + "\n")

    # ─── STEP 1: MONITORS ─────────────────────────────
    new_articles = run_news_monitor()
    new_videos = run_youtube_monitor()

    # Tag each item with its source so the Summariser and Reporter
    # can tell news apart from YouTube after they're combined
    for article in new_articles:
        article["source_type"] = "news"
    for video in new_videos:
        video["source_type"] = "youtube"

    new_items = new_articles + new_videos

    if not new_items:
        print("⚠️  No new content found today. Exiting.")
        return None

    # ─── STEP 2: SUMMARISER ───────────────────────────
    summarised_items = run_summariser(new_items)

    if not summarised_items:
        print("⚠️  Summariser produced no items today. Exiting.")
        return None

    # ─── STEP 3: REPORTER ─────────────────────────────
    digest_path = run_reporter(summarised_items)

    # ─── DONE ─────────────────────────────────────────
    print("="*50)
    print("✅ Content Monitoring Pipeline completed successfully!")
    print(f"   📊 Digest saved to: {digest_path}")
    print(f"   📰 {len(new_articles)} new articles found")
    print(f"   📺 {len(new_videos)} new videos found")
    print(f"   ✍️  {len(summarised_items)} items summarised")
    print("="*50 + "\n")

    return digest_path

if __name__ == "__main__":
    run_pipeline()
