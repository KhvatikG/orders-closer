# TODO: Заменить принты на логирование
import requests

from tomato_api.core.settings import SETTINGS


def change_order_status(order: dict, new_status: str, token: str):
    """
    Изменяет статус заказа order на new_status
    :param order: Объект заказа
    :param new_status: Статус который необходимо установить заказу
    :param token: Токен авторизации
    :return:
    """
    print(f"Устанавливаю заказу {order['number']} статус {new_status}")
    url = SETTINGS.BASE_API_URL + '/orders/' + str(order['id']) + '/status'
    print(f"URL - {url}")
    payload = {"token": token, "status": new_status}
    r = requests.put(url, params=payload)
    code = r.status_code
    if code == 200:
        print(f"Заказ {order['number']} переведен в статус {new_status}")
        return True