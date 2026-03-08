import requests
import json
import time

# Берем токен, который ты скинул выше
TOKEN = '8521127551:AAGlcgYxz8EF3xhlqfvOz-oOubnaThTdwFU'
CHANNEL = '@Georgead1'

def get_crypto_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Ошибка получения цен: {e}")
        return {}

def send_telegram_post(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHANNEL,
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    response = requests.post(url, json=payload)
    return response.json()

def generate_expert_post():
    prices = get_crypto_prices()
    btc = prices.get('bitcoin', {}).get('usd', 'Н/Д')
    eth = prices.get('ethereum', {}).get('usd', 'Н/Д')
    sol = prices.get('solana', {}).get('usd', 'Н/Д')
    
    # Экспертный пост от имени George (George_ad)
    post = (
        f"📊 <b>Обзор рынка | George_ad</b>\n\n"
        f"Текущие котировки:\n"
        f"🟠 BTC: ${btc}\n"
        f"🔵 ETH: ${eth}\n"
        f"🟣 SOL: ${sol}\n\n"
        f"💡 <b>Мое мнение:</b>\n"
        f"Я считаю, что текущая проторговка по биткоину — это классическое накопление крупным игроком. Рынок замер в ожидании макроэкономических данных. Если фондовые индексы и золото покажут рост, крипта пойдет следом в качестве высокорискового актива с бета-коэффициентом. Ожидаем импульс после закрепления над ключевым локальным уровнем сопротивления.\n\n"
        f"Не суетимся и ждем подтверждения тренда.\n\n"
        f"🤝 <i>Торгую здесь (забирайте бонусы при регистрации):</i>\n"
        f"👉 <a href='https://t.me/Georgead1'>Твоя реферальная ссылка</a>"
    )
    return post

if __name__ == '__main__':
    print("Генерация поста...")
    post_text = generate_expert_post()
    print("Отправка в канал...")
    result = send_telegram_post(post_text)
    
    if result.get('ok'):
        print("✅ Пост успешно отправлен в канал!")
    else:
        print(f"❌ Ошибка отправки: {result}")
