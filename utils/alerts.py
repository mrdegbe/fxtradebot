import requests

BOT_TOKEN = "8455530486:AAFUH9qHMfsXpMEJ3z2rebBYS-qaVzha1oE"
CHAT_ID = "7569585318"


def send_telegram_alert(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram error:", e)
