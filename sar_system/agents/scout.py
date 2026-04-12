# sar_system/agents/scout.py
from shared.tools.search import search_jobs
from shared.memory import filter_new_jobs
from sar_system.config import SEARCH_QUERIES, MAX_RESULTS_PER_QUERY


def run_scout() -> list[dict[str, str]]:
    """
    Scout agent — searches for fresh job listings.
    Returns a deduplicated list of unseen job listings.
    """
    print("\n🔍 Scout starting...")

    all_results: list[dict[str, str]] = []
    seen_urls: set[str] = set()

    for query in SEARCH_QUERIES:
        print(f"   Searching: '{query}'...")

        results = search_jobs(
            query=query,
            max_results=MAX_RESULTS_PER_QUERY
        )

        # Deduplicate within this run — same job can appear in multiple queries
        for job in results:
            url = job.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_results.append(job)

    print(f"   Found {len(all_results)} unique listings across all queries")

    # Filter out jobs already seen in previous runs
    new_jobs = filter_new_jobs(all_results)

    print(f"   {len(new_jobs)} new listings after filtering seen jobs")
    print("✅ Scout done!\n")

    return new_jobs


if __name__ == "__main__":
    jobs = run_scout()
    print(f"\nSample results ({len(jobs)} total):")
    for job in jobs[:3]:
        print(f"  - {job['title']}")
        print(f"    {job['url']}")
        print()