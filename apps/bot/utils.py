import requests


def bot_send_message(message):
    token = "6711417231:AAH4fBwj12FNyQ2i1VX2jA3atceH18qOfKY"
    channel_id = -1002025795462
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": channel_id, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=params)
