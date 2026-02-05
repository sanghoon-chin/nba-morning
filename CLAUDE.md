# NBA Morning - Project Context

## 프로젝트 개요
매일 아침 NBA 뉴스를 요약해서 텔레그램으로 받아보는 자동화 봇.

## 사용자 프로필
- NBA 덕후 (hardcore fan)
- Mamba Mentality (코비 브라이언트) 광팬
- 르브론 제임스, 디트로이트 피스톤스 좋아함
- CBA 규칙, 트레이드 메카닉스, 통계에 관심 많음

## 아키텍처
```
[Reddit r/nba RSS] → [Claude API 요약] → [Telegram 전송]
```

## 기술 스택
- Python 3.12
- feedparser (RSS 수집)
- anthropic (Claude API)
- requests (Telegram API)
- GitHub Actions (스케줄링)

## 핵심 파일
- `main.py` - 메인 실행
- `src/rss_fetcher.py` - Reddit RSS 수집
- `src/summarizer.py` - Claude API로 요약 (5개 섹션, JSON 응답)
- `src/telegram_bot.py` - 텔레그램 전송 (5개 메시지)
- `Makefile` - 로컬 실행 편의

## 브리핑 5개 섹션
1. 📰 **BREAKING NEWS & TRADES** - 속보 + 트레이드
2. 📊 **FACTS & FIGURES** - 통계 + 부상 + 경기
3. 🧠 **DEEP DIVE ANALYSIS** - CBA + 트레이드 메카닉스
4. 🎯 **HOOPS NERD TIME** - 트리비아 + 밈 (유머)
5. 🤔 **QUESTIONS TO PONDER** - 생각해볼 질문들

## 환경변수 (.env)
```
ANTHROPIC_API_KEY=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

## 실행 방법
```bash
make install  # 첫 세팅
make run      # 실행
```

## GitHub Actions
- 매일 한국시간 낮 12시 자동 실행 (UTC 03:00)
- `.github/workflows/morning-briefing.yml`
- Secrets 설정 필요: ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

## 텔레그램 봇
- 이름: `@nba_morning_bot`
- 현재 개인 chat_id로만 전송

## 카카오 채널 (미완성)
- 채널명: Mamba Hoops
- 설명: 8x24 Mamba Mentality, Always
- 사업자 등록 없이는 다른 사람에게 메시지 발송 불가
- 텔레그램 채널로 대체 고려 중

## 향후 계획
- 텔레그램 채널로 다른 사람들에게도 공유
- 시간대별 알림 추가 (아침 외에도)
- 실시간 속보 알림 기능

## 주의사항
- Reddit API는 2025년 11월부터 수동 승인제로 변경됨 → RSS 사용
- 텔레그램 메시지 길이 제한 4096자 → 5개로 분할 전송
- AI 응답에 제목 중복 방지 로직 있음
