.PHONY: install run test-rss test-telegram clean

# 의존성 설치
install:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

# 메인 실행
run:
	. .venv/bin/activate && python main.py

# RSS 피드 테스트
test-rss:
	. .venv/bin/activate && python test_rss.py

# 텔레그램 테스트 메시지 전송
test-telegram:
	. .venv/bin/activate && python -c "from src.telegram_bot import send_message; from dotenv import load_dotenv; import os; load_dotenv(); send_message('🏀 Test message!', os.getenv('TELEGRAM_BOT_TOKEN'), os.getenv('TELEGRAM_CHAT_ID'))"

# 캐시 정리
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
