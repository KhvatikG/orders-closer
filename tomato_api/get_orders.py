# TODO: Привести функции методов апи к одному виду - либо обработка кода ответа внутри,
#  либо возвращать наружу и код и дату для внешней обработки

import json
import requests

from core.settings import SETTINGS


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

    url = SETTINGS.BASE_API_URL + '/orders'
    payload = {"token": token, "per_page": count, "status": status}
    r = requests.post(url, params=payload)
    code = r.status_code
    if code == 200:
        data = json.loads(r.json())
        orders = data.get("orders")
        return orders

    else:
        print(code) # TODO: Заменить на логирование

