# TODO: Привести функции методов апи к одному виду - либо обработка кода ответа внутри,
#  либо возвращать наружу и код и дату для внешней обработки

import json
import requests

from tomato_api.core.settings import SETTINGS


def get_orders_per_status(count: int, status: str, token: str) -> list:
    """
    Возвращает список из count заказов со статусом status.
    Статусы:
    confirm - Подтверждён
    delivery - Доставляется
    complete - Доставлен
    :param count: Количество заказов
    :param status: Статус
    :param token: Токен
    :return:
    """
    print(f"Получение блюд") # TODO: Заменить на логирование
    url = SETTINGS.BASE_API_URL + '/orders'
    payload = {"token": token, "status": status, "per_page": count}
    r = requests.get(url, params=payload)
    code = r.status_code
    print(f"Получение блюд: код ответа - {code}") # TODO: Заменить на логирование
    if code == 200:
        data = json.loads(r.text)
        orders = data.get("orders")
        print(f"Получено {len(orders)} блюд со статусом {status}")
        return orders

    else:
        print(f"Блюда не получены, код ответа: {code}")  # TODO: Заменить на логирование

