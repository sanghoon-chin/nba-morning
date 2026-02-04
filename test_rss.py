"""
RSS 피드 테스트 스크립트
Reddit r/nba의 RSS 피드가 정상 작동하는지 확인합니다.
"""

import feedparser
from datetime import datetime

RSS_FEEDS = {
    "hot": "https://www.reddit.com/r/nba/hot/.rss",
    "new": "https://www.reddit.com/r/nba/new/.rss",
    "top_day": "https://www.reddit.com/r/nba/top/.rss?t=day",
}


def test_feed(name: str, url: str) -> None:
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print("=" * 60)

    feed = feedparser.parse(url)

    if feed.bozo:
        print(f"Error: {feed.bozo_exception}")
        return

    print(f"Feed Title: {feed.feed.get('title', 'N/A')}")
    print(f"Total Entries: {len(feed.entries)}")
    print(f"\nTop 5 posts:")
    print("-" * 40)

    for i, entry in enumerate(feed.entries[:5], 1):
        title = entry.get("title", "No title")
        author = entry.get("author", "Unknown")
        published = entry.get("published", "Unknown")
        print(f"\n{i}. {title}")
        print(f"   Author: {author}")
        print(f"   Published: {published}")


def main():
    print("NBA Morning - RSS Feed Test")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    for name, url in RSS_FEEDS.items():
        test_feed(name, url)

    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
