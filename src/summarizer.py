"""
Claude API를 사용해 NBA 뉴스를 요약합니다.
"""

import anthropic
import json
from dataclasses import dataclass


@dataclass
class DigestSections:
    breaking_news: str      # Headlines + Trades
    deep_dive: str          # CBA Insight + Trade Mechanics
    facts_and_stats: str    # Stats + Injuries + Games
    fun_stuff: str          # Trivia + Meme
    questions: str          # Questions to Ponder


SYSTEM_PROMPT = """You are an NBA expert analyst and CBA specialist writing a daily morning digest for a hardcore basketball fan.

The reader is deeply interested in:
- NBA statistics and advanced metrics
- CBA rules (salary cap, trade exceptions, Bird Rights, etc.)
- Trade mechanics and how deals get done

Follow these guidelines:
1. Write in English
2. Be detailed and thorough - the reader is a hardcore NBA fan who wants in-depth analysis
3. For trades, ALWAYS explain the mechanics: salary matching, trade exceptions used, cap implications
4. Include relevant statistics and historical comparisons
5. Explain any CBA rules that are relevant to the day's news
6. Use emojis to enhance readability
7. Don't hold back on length - comprehensive coverage is preferred

CRITICAL - DATA ACCURACY:
- ONLY use information explicitly stated in the provided Reddit posts
- If specific details (salary numbers, stats, dates) are not in the posts, DO NOT make them up
- When you're not 100% certain about a detail, either omit it or clearly state it's unconfirmed
- Never invent player stats, contract numbers, or trade details that aren't in the source data
- If there's not enough info to write a section, write what you can and note "Limited info available today"

IMPORTANT: You must respond in valid JSON format with exactly 5 sections."""

USER_PROMPT_TEMPLATE = """Here are the top posts from r/nba in the last 24 hours:

---
{posts}
---

Create a comprehensive NBA Morning Digest. Respond in this exact JSON format:

{{
  "breaking_news": "Your content for section 1 here",
  "deep_dive": "Your content for section 2 here",
  "facts_and_stats": "Your content for section 3 here",
  "fun_stuff": "Your content for section 4 here",
  "questions": "Your content for section 5 here"
}}

Section contents:

1. **breaking_news** (📰 BREAKING NEWS & TRADES):
   - Major headlines with detailed analysis
   - All trades & transactions with salary breakdowns
   - How each trade works under CBA rules

2. **deep_dive** (🧠 DEEP DIVE ANALYSIS):
   - CBA INSIGHT OF THE DAY: Explain one relevant CBA concept (salary matching, Bird Rights, TPE, MLE, aprons, etc.)
   - TRADE MECHANICS BREAKDOWN: For the biggest trade - how salaries matched, exceptions used, draft capital moved, trade kickers/protections

3. **facts_and_stats** (📊 FACTS & FIGURES):
   - STAT SPOTLIGHT: Interesting statistics, advanced metrics (PER, WS, VORP), historical comparisons
   - INJURY REPORT: Updates on injured players
   - GAME HIGHLIGHTS: Notable performances and results
   - NEWS & RUMORS: Other noteworthy items

4. **fun_stuff** (🎯 HOOPS NERD TIME):
   - TRADE TRIVIA OF THE DAY: One interesting historical NBA trade fact
   - MEME OF THE DAY: A humorous take on today's news - could be a witty observation, r/nba style joke, or a funny "what if" scenario. Reference NBA memes like "Kelvin Benjamin copypasta style", "He boomed me", "Least delusional [team] fan", etc. Be creative and funny!

5. **questions** (🤔 QUESTIONS TO PONDER):
   - 2-3 thought-provoking questions about today's news
   - Make these genuinely interesting discussion starters
   - Could be about team strategy, player fit, front office decisions, legacy implications, etc.
   - Encourage the reader to think critically about the news

Go deep on analysis. The reader wants the full picture with all the nerdy details.
Remember: Output ONLY valid JSON, no markdown code blocks."""


def summarize_news(posts_text: str, api_key: str) -> DigestSections:
    """
    게시물 목록을 받아 AI로 요약합니다.

    Args:
        posts_text: 포맷팅된 게시물 텍스트
        api_key: Anthropic API 키

    Returns:
        DigestSections 객체 (4개 섹션)
    """
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(posts=posts_text)
            }
        ]
    )

    response_text = message.content[0].text

    # JSON 파싱
    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        # JSON 파싱 실패 시 전체를 breaking_news에 넣음
        return DigestSections(
            breaking_news=response_text,
            deep_dive="",
            facts_and_stats="",
            fun_stuff="",
            questions=""
        )

    return DigestSections(
        breaking_news=data.get("breaking_news", ""),
        deep_dive=data.get("deep_dive", ""),
        facts_and_stats=data.get("facts_and_stats", ""),
        fun_stuff=data.get("fun_stuff", ""),
        questions=data.get("questions", "")
    )


if __name__ == "__main__":
    # 테스트 (API 키 필요)
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("ANTHROPIC_API_KEY not found in .env")
    else:
        test_posts = """1. [01:04 UTC] [Charania] BREAKING: James Harden traded to Cavaliers
2. [23:22 UTC] Gregg Popovich visits Spurs practice
3. [20:42 UTC] Vucevic traded to Celtics"""

        result = summarize_news(test_posts, api_key)
        print(result)
