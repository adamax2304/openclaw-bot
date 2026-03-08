#!/usr/bin/env python3
import os
import time
import json
import requests

# Simple long-polling Telegram bot runner that reads token from secret GEORGE_BOT_TOKEN
# It uses Telegram getUpdates method. Replace with real webhook handler if needed.

TOKEN = os.environ.get('GEORGE_BOT_TOKEN') or None
if not TOKEN:
    raise SystemExit('GEORGE_BOT_TOKEN not found in environment')

API = f"https://api.telegram.org/bot{TOKEN}"
OFFSET = 0

LOG_DIR = '/root/.openclaw/workspace/memory'
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, 'george_bot.log')

def log(line):
    with open(LOG_PATH, 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {line}\n")

def send_message(chat_id, text):
    url = f"{API}/sendMessage"
    data = {'chat_id': chat_id, 'text': text}
    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        log(f"SEND_ERR {e}")

log('START george_bot_runner')

while True:
    try:
        resp = requests.get(f"{API}/getUpdates", params={'offset': OFFSET, 'timeout': 20}, timeout=60)
        data = resp.json()
        for item in data.get('result', []):
            update_id = item.get('update_id')
            OFFSET = max(OFFSET, update_id + 1)
            msg = item.get('message') or item.get('edited_message')
            if not msg:
                continue
            chat = msg.get('chat', {})
            chat_id = chat.get('id')
            text = msg.get('text', '')
            if text.startswith('/start'):
                send_message(chat_id, 'Hello! I am George bot. Use /help to see commands.')
            elif text.startswith('/help'):
                send_message(chat_id, 'Available commands: /start, /help')
            else:
                send_message(chat_id, 'Unknown command. Use /help')
            log(f"MSG {chat_id} {text}")
    except Exception as e:
        log(f"ERR {e}")
        time.sleep(5)
    # small delay to prevent tight loop in case of errors
    time.sleep(1)
