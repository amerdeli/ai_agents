import os
from tavily import TavilyClient
from dotenv import load_dotenv
from sar_system.config import JOB_SITES

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_jobs(query: str, max_results: int = 10) -> list[dict]:
    """
    Search for job listings on defined job sites using Tavily.
    Returns a list of results with title, url and description.
    """
    try:
        response = tavily.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_domains=JOB_SITES,
            time_range='week'
        )

        results = response.get("results", [])

        cleaned = []
        for result in results:
            cleaned.append({
                "title":       result.get("title", ""),
                "url":         result.get("url", ""),
                "description": result.get("content", "")
            })

        return cleaned

    except Exception as e:
        print(f"Search error: {e}")
        return []

# Temporary test — remove after confirming it works!
if __name__ == "__main__":
    results = search_jobs("Python AI engineer remote", max_results=5)
    for r in results:
        print(r["title"])
        print(r["url"])
        print("---")