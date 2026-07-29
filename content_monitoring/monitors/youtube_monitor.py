# content_monitoring/monitors/youtube_monitor.py
import os
import requests
from dotenv import load_dotenv
from shared.memory import filter_new_videos
from content_monitoring.config import YOUTUBE_CHANNELS, MAX_VIDEOS_PER_CHANNEL

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def search_channel_videos(channel_id: str, max_results: int = 5) -> list[dict]:
    """
    Fetch the most recent videos for a single YouTube channel
    using the YouTube Data API v3 search endpoint.
    Returns a list of results with title, url, description and channel.
    """
    try:
        response = requests.get(
            YOUTUBE_SEARCH_URL,
            params={
                "key": YOUTUBE_API_KEY,
                "channelId": channel_id,
                "part": "snippet",
                "order": "date",
                "type": "video",
                "maxResults": max_results
            }
        )
        response.raise_for_status()
        items = response.json().get("items", [])

        cleaned = []
        for item in items:
            video_id = item.get("id", {}).get("videoId", "")
            snippet = item.get("snippet", {})

            if not video_id:
                continue

            cleaned.append({
                "title":       snippet.get("title", ""),
                "url":         f"https://www.youtube.com/watch?v={video_id}",
                "description": snippet.get("description", ""),
                "channel":     snippet.get("channelTitle", "")
            })

        return cleaned

    except Exception as e:
        print(f"YouTube search error for channel {channel_id}: {e}")
        return []


def run_youtube_monitor() -> list[dict[str, str]]:
    """
    YouTube monitor — searches monitored channels for fresh videos.
    Returns a deduplicated list of unseen videos.
    """
    print("\n📺 YouTube monitor starting...")

    all_results: list[dict[str, str]] = []
    seen_urls: set[str] = set()

    for channel_id in YOUTUBE_CHANNELS:
        print(f"   Checking channel: '{channel_id}'...")

        results = search_channel_videos(
            channel_id=channel_id,
            max_results=MAX_VIDEOS_PER_CHANNEL
        )

        # Deduplicate within this run - unlikely but keeps the pattern consistent
        for video in results:
            url = video.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_results.append(video)

    print(f"   Found {len(all_results)} unique videos across all channels")

    # Filter out videos already seen in previous runs
    new_videos = filter_new_videos(all_results)

    print(f"   {len(new_videos)} new videos after filtering seen videos")
    print("✅ YouTube monitor done!\n")

    return new_videos
