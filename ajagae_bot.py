import tweepy
import os
import json
import random
from datetime import datetime
from collections import Counter

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

GAG_FILE = "gag_list.txt"
STATUS_FILE = "status.json"
LOG_FILE = "reaction_log.json"

now = datetime.now()

with open(GAG_FILE, encoding='utf-8') as f:
    gags = [line.strip() for line in f if line.strip()]

if os.path.exists(LOG_FILE):
    try:
        with open(LOG_FILE, encoding='utf-8') as f:
            logs = json.load(f)
    except json.JSONDecodeError:
        logs = []
else:
    logs = []

counter = Counter([log['text'] for log in logs])
top_5 = [text for text, _ in counter.most_common(5)]
already_sent = set([log['text'] for log in logs])

candidates = [g for g in gags if g not in already_sent or g in top_5]

if not candidates:
    print("⚠️ 전송할 수 있는 새로운 개그가 없습니다.")
    exit()

hashtags = "#아재개그 #개그봇 #트윗봇"
gag = f"{random.choice(candidates)}\n\n{hashtags}"

try:
    response = client.create_tweet(text=gag)
    print(f"✅ 트윗 완료: {gag}")
except Exception as e:
    print(f"❌ 트윗 실패: {e}")
    exit()

reaction = {
    "id": response.data['id'],
    "text": gag,
    "datetime": now.strftime("%Y-%m-%d %H:%M:%S")
}

logs.append(reaction)

with open(LOG_FILE, 'w', encoding='utf-8') as f:
    json.dump(logs, f, ensure_ascii=False, indent=2)

with open(STATUS_FILE, 'w', encoding='utf-8') as f:
    json.dump({"last_run": now.strftime("%Y-%m-%d %H:%M:%S")}, f)
