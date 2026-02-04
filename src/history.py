"""
브리핑 히스토리를 파일로 저장합니다.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.summarizer import DigestSections

HISTORY_DIR = Path(__file__).parent.parent / "history"


def save_digest(digest: "DigestSections", posts_count: int = 0) -> str:
    """
    DigestSections를 JSON 파일로 저장합니다.

    Args:
        digest: DigestSections 객체
        posts_count: 수집된 포스트 수

    Returns:
        저장된 파일 경로
    """
    # 히스토리 디렉토리 생성
    HISTORY_DIR.mkdir(exist_ok=True)

    # 파일명: YYYY-MM-DD_HHMMSS.json
    timestamp = datetime.now()
    filename = timestamp.strftime("%Y-%m-%d_%H%M%S") + ".json"
    filepath = HISTORY_DIR / filename

    data = {
        "timestamp": timestamp.isoformat(),
        "posts_count": posts_count,
        "sections": {
            "breaking_news": digest.breaking_news,
            "deep_dive": digest.deep_dive,
            "facts_and_stats": digest.facts_and_stats,
            "fun_stuff": digest.fun_stuff,
            "questions": digest.questions,
        }
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return str(filepath)


def list_history(limit: int = 10) -> list[dict]:
    """
    최근 히스토리 목록을 반환합니다.

    Args:
        limit: 반환할 최대 개수

    Returns:
        히스토리 목록 (최신순)
    """
    if not HISTORY_DIR.exists():
        return []

    files = sorted(HISTORY_DIR.glob("*.json"), reverse=True)[:limit]

    history = []
    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            data = json.load(file)
            data["filename"] = f.name
            history.append(data)

    return history
