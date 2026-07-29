import os
import json
from datetime import datetime
from sar_system.config import SEEN_JOBS_FILE
from content_monitoring.config import SEEN_ARTICLES_FILE, SEEN_VIDEOS_FILE


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


def load_seen_articles() -> set[str]:
    """
    Load the set of already seen article URLs from disk.
    Returns an empty set if file doesn't exist yet.
    """
    if not os.path.exists(SEEN_ARTICLES_FILE):
        return set()

    with open(SEEN_ARTICLES_FILE, "r") as f:
        data = json.load(f)
        return set(data.get("urls", []))


def save_seen_articles(seen_articles: set[str]) -> None:
    """
    Save the updated set of seen article URLs to disk.
    Also records the last time the file was updated.
    """
    os.makedirs(SEEN_ARTICLES_FILE.parent, exist_ok=True)

    with open(SEEN_ARTICLES_FILE, "w") as f:
        json.dump({
            "urls": list(seen_articles),
            "last_updated": datetime.now().isoformat()
        }, f, indent=2)


def filter_new_articles(articles: list[dict]) -> list[dict]:
    """
    Given a list of articles, return only the ones not seen before.
    Also updates seen_articles.json!
    """
    seen = load_seen_articles()

    new_articles = [
        article for article in articles
        if article.get("url") not in seen
    ]

    for article in new_articles:
        url = article.get("url")
        if url:
            seen.add(str(url))
    save_seen_articles(seen)

    return new_articles


def clear_seen_articles() -> None:
    """
    Utility function — clears all seen articles.
    Useful for testing or resetting the system!
    """
    save_seen_articles(set())
    print("Seen articles cleared!")


def load_seen_videos() -> set[str]:
    """
    Load the set of already seen video URLs from disk.
    Returns an empty set if file doesn't exist yet.
    """
    if not os.path.exists(SEEN_VIDEOS_FILE):
        return set()

    with open(SEEN_VIDEOS_FILE, "r") as f:
        data = json.load(f)
        return set(data.get("urls", []))


def save_seen_videos(seen_videos: set[str]) -> None:
    """
    Save the updated set of seen video URLs to disk.
    Also records the last time the file was updated.
    """
    os.makedirs(SEEN_VIDEOS_FILE.parent, exist_ok=True)

    with open(SEEN_VIDEOS_FILE, "w") as f:
        json.dump({
            "urls": list(seen_videos),
            "last_updated": datetime.now().isoformat()
        }, f, indent=2)


def filter_new_videos(videos: list[dict]) -> list[dict]:
    """
    Given a list of videos, return only the ones not seen before.
    Also updates seen_videos.json!
    """
    seen = load_seen_videos()

    new_videos = [
        video for video in videos
        if video.get("url") not in seen
    ]

    for video in new_videos:
        url = video.get("url")
        if url:
            seen.add(str(url))
    save_seen_videos(seen)

    return new_videos


def clear_seen_videos() -> None:
    """
    Utility function — clears all seen videos.
    Useful for testing or resetting the system!
    """
    save_seen_videos(set())
    print("Seen videos cleared!")