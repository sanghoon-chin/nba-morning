"""
Reddit r/nba RSS 피드에서 뉴스를 수집합니다.
"""

import feedparser
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass


@dataclass
class Post:
    title: str
    author: str
    url: str
    published: datetime


def fetch_nba_news(hours: int = 24) -> list[Post]:
    """
    최근 N시간 동안의 r/nba 인기 게시물을 가져옵니다.

    Args:
        hours: 몇 시간 전까지의 게시물을 가져올지 (기본 24시간)

    Returns:
        Post 객체 리스트
    """
    feeds = [
        "https://www.reddit.com/r/nba/hot/.rss",
        "https://www.reddit.com/r/nba/top/.rss?t=day",
    ]

    posts: dict[str, Post] = {}  # URL을 키로 사용해 중복 제거
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)

    for feed_url in feeds:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            # 시간 파싱
            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

            # 시간 필터링
            if published and published < cutoff_time:
                continue

            url = entry.get('link', '')
            if url and url not in posts:
                posts[url] = Post(
                    title=entry.get('title', 'No title'),
                    author=entry.get('author', 'Unknown'),
                    url=url,
                    published=published or datetime.now(timezone.utc),
                )

    # 시간순 정렬 (최신순)
    sorted_posts = sorted(posts.values(), key=lambda p: p.published, reverse=True)

    return sorted_posts


def format_posts_for_summary(posts: list[Post], max_posts: int = 30) -> str:
    """
    AI 요약을 위해 게시물을 텍스트로 포맷팅합니다.
    """
    lines = []
    for i, post in enumerate(posts[:max_posts], 1):
        time_str = post.published.strftime('%H:%M UTC')
        lines.append(f"{i}. [{time_str}] {post.title}")

    return "\n".join(lines)


if __name__ == "__main__":
    # 테스트
    posts = fetch_nba_news(hours=24)
    print(f"Found {len(posts)} posts\n")
    print(format_posts_for_summary(posts))
