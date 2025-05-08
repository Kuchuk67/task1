import requests
from requests import RequestException

from config.settings import BOT_TOKEN


def send_telegram_message(message, chat_id):
    """
    Отправка сообщения в телеграм
    """
    params = {"text": message, "chat_id": chat_id}  # chat_id=1385214291
    try:
        response = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params=params,
        )
        response.raise_for_status()
    except RequestException as e:
        print(f"Ошибка отправки: {e}")
