# content_monitoring/monitors/news_monitor.py
from shared.tools.search import search_news
from shared.memory import filter_new_articles
from content_monitoring.config import NEWS_QUERIES, MAX_RESULTS_PER_QUERY


def run_news_monitor() -> list[dict[str, str]]:
    """
    News monitor — searches for fresh articles.
    Returns a deduplicated list of unseen articles.
    """
    print("\n📰 News monitor starting...")

    all_results: list[dict[str, str]] = []
    seen_urls: set[str] = set()

    for query in NEWS_QUERIES:
        print(f"   Searching: '{query}'...")

        results = search_news(
            query=query,
            max_results=MAX_RESULTS_PER_QUERY
        )

        # Deduplicate within this run - same article can appear in multiple queries
        for article in results:
            url = article.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_results.append(article)

    print(f"   Found {len(all_results)} unique articles across all queries")

    # Filter out articles already seen in previous runs
    new_articles = filter_new_articles(all_results)

    print(f"   {len(new_articles)} new articles after filtering seen articles")
    print("✅ News monitor done!\n")

    return new_articles
