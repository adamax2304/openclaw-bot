import requests
import time
import json

TOKEN = '8521127551:AAHgkdEpaIcuPBYDzWLTZlMZIZKTgkkDLEU'
CHANNEL = '@Georgead1'

def get_crypto_data():
    try:
        resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd')
        return resp.json()
    except:
        return {'bitcoin': {'usd': 0}, 'ethereum': {'usd': 0}, 'solana': {'usd': 0}}

def post_to_telegram():
    prices = get_crypto_data()
    btc = prices.get('bitcoin', {}).get('usd', 'N/A')
    eth = prices.get('ethereum', {}).get('usd', 'N/A')
    sol = prices.get('solana', {}).get('usd', 'N/A')
    
    post_text = f"""🔥 **Рынок прямо сейчас** 🔥

🟠 BTC: ${btc}
🔵 ETH: ${eth}
🟣 SOL: ${sol}

Индекс страха и жадности скачет, а значит — самое время для скальпинга и поиска ТВХ (точек входа). Крупные игроки уже расставляют лимитки. 

Внимательно следим за объемами. Скоро выкачу подробный сетап по одной интересной альте, которая готовится к пробою. 📈

🤝 *Торгую и забираю бонусы здесь:*
👉 [ТВОЯ_РЕФЕРАЛЬНАЯ_ССЫЛКА]

#Crypto #Trading #Bitcoin"""

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHANNEL,
        'text': post_text,
        'parse_mode': 'Markdown'
    }
    
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == '__main__':
    print("Отправка первого тестового поста...")
    result = post_to_telegram()
    print("Результат:", json.dumps(result, indent=2, ensure_ascii=False))
