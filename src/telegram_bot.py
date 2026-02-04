"""
텔레그램으로 메시지를 전송합니다.
"""

import requests
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.summarizer import DigestSections

TELEGRAM_MAX_LENGTH = 4096

MESSAGE_TITLES = {
    "breaking_news": "📰 BREAKING NEWS & TRADES",
    "deep_dive": "🧠 DEEP DIVE ANALYSIS",
    "facts_and_stats": "📊 FACTS & FIGURES",
    "fun_stuff": "🎯 HOOPS NERD TIME",
    "questions": "🤔 QUESTIONS TO PONDER",
}


def send_single_message(text: str, bot_token: str, chat_id: str) -> bool:
    """단일 메시지 전송"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print(f"Telegram error: {response.status_code}")
        print(response.text)
        return False

    return True


def send_digest(digest: "DigestSections", bot_token: str, chat_id: str) -> bool:
    """
    DigestSections를 5개의 메시지로 나눠서 전송합니다.

    Args:
        digest: DigestSections 객체
        bot_token: 텔레그램 봇 토큰
        chat_id: 수신자 Chat ID

    Returns:
        성공 여부
    """
    sections = [
        ("breaking_news", digest.breaking_news),
        ("facts_and_stats", digest.facts_and_stats),
        ("deep_dive", digest.deep_dive),
        ("fun_stuff", digest.fun_stuff),
        ("questions", digest.questions),
    ]

    for i, (key, content) in enumerate(sections):
        if not content:
            continue

        title = MESSAGE_TITLES.get(key, "")

        # 내용이 이미 제목으로 시작하면 제목 추가 안 함
        if content.strip().startswith(title):
            message = content
        else:
            message = f"{title}\n\n{content}"

        if not send_single_message(message, bot_token, chat_id):
            return False

        # 메시지 사이 딜레이
        if i < len(sections) - 1:
            time.sleep(1)

    return True


# 하위 호환성을 위한 함수 (이전 코드와 호환)
def send_message(text: str, bot_token: str, chat_id: str) -> bool:
    """단순 텍스트 메시지 전송 (하위 호환용)"""
    return send_single_message(text, bot_token, chat_id)


if __name__ == "__main__":
    # 테스트
    import os
    from dotenv import load_dotenv

    load_dotenv()

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if bot_token and chat_id:
        success = send_message("🏀 NBA Morning 테스트 메시지입니다!", bot_token, chat_id)
        print("Sent!" if success else "Failed!")
    else:
        print("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
