"""
NBA Morning - 매일 아침 NBA 뉴스 요약을 텔레그램으로 전송합니다.
"""

import os
from dotenv import load_dotenv

from src.rss_fetcher import fetch_nba_news, format_posts_for_summary
from src.summarizer import summarize_news
from src.telegram_bot import send_digest


def main():
    # 환경변수 로드
    load_dotenv()

    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    # 환경변수 확인
    if not all([anthropic_key, telegram_token, telegram_chat_id]):
        print("Error: Missing environment variables. Check your .env file.")
        return

    print("🏀 NBA Morning - Starting...")

    # 1. RSS에서 뉴스 수집
    print("📡 Fetching news from r/nba...")
    posts = fetch_nba_news(hours=24)
    print(f"   Found {len(posts)} posts")

    if not posts:
        print("No posts found. Exiting.")
        return

    # 2. AI로 요약 (4개 섹션으로 구조화)
    print("🤖 Summarizing with Claude...")
    posts_text = format_posts_for_summary(posts)
    digest = summarize_news(posts_text, anthropic_key)
    print("   Summary generated!")

    # 3. 텔레그램으로 전송 (4개 메시지)
    print("📱 Sending to Telegram (4 messages)...")
    success = send_digest(digest, telegram_token, telegram_chat_id)

    if success:
        print("✅ Done! Check your Telegram.")
    else:
        print("❌ Failed to send message.")


if __name__ == "__main__":
    main()
