# shared/memory.py
import os
import json
from datetime import datetime

SEEN_JOBS_FILE = "data/seen_jobs.json"


def load_seen_jobs() -> set[str]:
    """
    Load the set of already seen job URLs from disk.
    Returns an empty set if file doesn't exist yet.
    """
    if not os.path.exists(SEEN_JOBS_FILE):
        return set()

    with open(SEEN_JOBS_FILE, "r") as f:
        data = json.load(f)
        return set(data.get("urls", []))


def save_seen_jobs(seen_jobs: set[str]) -> None:
    """
    Save the updated set of seen job URLs to disk.
    Also records the last time the file was updated.
    """
    os.makedirs("data", exist_ok=True)

    with open(SEEN_JOBS_FILE, "w") as f:
        json.dump({
            "urls": list(seen_jobs),
            "last_updated": datetime.now().isoformat()
        }, f, indent=2)


def filter_new_jobs(job_listings: list[dict]) -> list[dict]:
    """
    Given a list of job listings, return only the ones
    not seen before. Also updates seen_jobs.json!
    """
    seen = load_seen_jobs()

    new_jobs = [
        job for job in job_listings
        if job.get("url") not in seen
    ]

    for job in new_jobs:
        url = job.get("url")
        if url:
            seen.add(str(url))
    save_seen_jobs(seen)

    return new_jobs


def clear_seen_jobs() -> None:
    """
    Utility function — clears all seen jobs.
    Useful for testing or resetting the system!
    """
    save_seen_jobs(set())
    print("Seen jobs cleared!")