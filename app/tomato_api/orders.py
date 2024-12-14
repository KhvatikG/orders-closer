import json

import requests
from loguru import logger

from app.core.settings import SETTINGS
from app.tomato_api.exceptions.extentions import UpdateOrderError, NetworkError, GetOrdersError


def close_orders(orders: list, token: str) -> str:
    """
    Закрывает заказы
    :param orders: список заказов
    :param token: токен
    :return:
    """
    result = {
        "closed": 0,
        "total": len(orders),
        "problem_numbers": []
    }

    counter = 0

    for order in orders:
        counter += 1

        try:
            change_order_status(
                order=order,
                new_status='complete',
                token=token
            )
        except UpdateOrderError as e:
            logger.error(f"Не удалось закрыть заказ. Шаг {counter} из {result['total']}\nОшибка: {e}")
            result['problem_numbers'].append(order.get('number', 'не удалось получить номер'))
        else:
            result["closed"] += 1

    result_info = f"Удалось закрыть {result['closed']} заказов из {result['total']}"
    logger.info(result_info)

    if result["problem_numbers"]:
        result_info += f"\nНе удалось закрыть следующие заказы: {result.get('problem_numbers')}"
        logger.warning(f"Не удалось закрыть следующие заказы: {result.get('problem_numbers')}")

    return result_info


def cancel_new_orders(orders: list, token: str):
    """
    Отменяет заказы
    :param orders: список заказов
    :param token: токен
    :return:
    """
    result = {
        "canceled": 0,
        "total": len(orders),
        "problem_numbers": []
    }

    counter = 0

    for order in orders:
        counter += 1

        try:
            change_order_status(
                order=order,
                new_status='undo',
                token=token
            )
        except UpdateOrderError as e:
            logger.error(f"Не удалось отменить заказ. Шаг {counter} из {result['total']}\nОшибка: {e}")
            result['problem_numbers'].append(order.get('number', 'не удалось получить номер'))
        else:
            result["canceled"] += 1

    result_info = f"Удалось отменить {result['canceled']} заказов из {result['total']}"
    logger.info(result_info)

    if result["problem_numbers"]:
        result_info += f"\nНе удалось отменить следующие заказы: {result.get('problem_numbers')}"
        logger.warning(f"Не удалось отменить следующие заказы: {result.get('problem_numbers')}")

    return result_info


def get_orders_per_status(count: int, status: str, token: str, archive=False, **kwargs) -> list:
    """
    Возвращает список из count заказов со статусом status.
    Статусы:
    confirm - Подтверждён
    delivery - Доставляется
    complete - Доставлен
    :param count: Количество заказов
    :param status: Статус
    :param token: Токен
    :param archive: Если True то запрашиваются заказы за все время, если False, то не старше 2ух недель
    :return:
    """
    logger.info(f"Получение заказов")

    try:
        url = SETTINGS.BASE_API_URL + '/orders'
        payment_status = kwargs.get("payment_status")
        payload = {
            "token": token,
            "payment_status%5B%5D": payment_status,
            "status": status,
            "per_page": count,
            "archive": int(archive)
        }
        response = requests.get(url, params=payload)
        code = response.status_code
        success = code == 200

        response.raise_for_status()

        if success:
            data = json.loads(response.text)
            orders = data.get("orders")
            logger.info(f"Получено {len(orders)} заказов со статусом {status}")
            return orders

        else:
            logger.error(f"Неожиданный код ответа: {code}")
            raise GetOrdersError(f"Неожиданный код ответа: {code}\n{response.text}")

    except requests.RequestException as e:
        error_info = f"Заказы не получены, ошибка: {e}"
        logger.exception(error_info)
        raise NetworkError(error_info, e)

    except Exception as e:
        logger.exception(f"Неожиданная ошибка при получении заказов: {e}")
        raise GetOrdersError(f"Неожиданная ошибка", e)


def get_count_orders_per_status(status: str, token: str, archive=False, **kwargs) -> int:
    """
    Возвращает количество заказов со статусом status
    :param status: Статус
    :param token: Токен авторизации
    :param archive: Если True то запрашиваются заказы за все время, если False, то не старше 2ух недель
    :return: Количество заказов
    """
    logger.info(f"Получение количества заказов")
    try:
        url = SETTINGS.BASE_API_URL + '/orders'
        payment_status = kwargs.get("payment_status")
        payload = {
            "token": token,
            "payment_status%5B%5D": payment_status,
            "status": status,
            "per_page": 1,
            "archive": int(archive)
        }
        response = requests.get(url, params=payload)
        code = response.status_code
        success = code == 200

        response.raise_for_status()

        if success:
            data = json.loads(response.text)
            count_orders = data.get("meta").get("count")
            logger.info(f"Получено количество заказов со статусом {status} - {count_orders}")
            return count_orders

        else:
            logger.error(f"Неожиданный код ответа: {code}")
            raise GetOrdersError(f"Неожиданный код ответа: {code}\n{response.text}")

    except requests.RequestException as e:
        error_info = f"Количество заказов не получено, ошибка: {e}"
        logger.exception(error_info)
        raise NetworkError(error_info, e)

    except Exception as e:
        logger.exception(f"Неожиданная ошибка при получении количества заказов: {e}")
        raise GetOrdersError(f"Неожиданная ошибка при получении количества заказов", e)


def change_order_status(order: dict, new_status: str, token: str) -> None:
    """
    Изменяет статус заказа order на new_status

    :param order: Объект заказа
    :param new_status: Статус который необходимо установить заказу
    :param token: Токен авторизации
    :return:
    """
    logger.info(f"Устанавливаю заказу {order['number']} статус {new_status}")

    try:
        url = SETTINGS.BASE_API_URL + '/orders/' + str(order['id']) + '/status'
        logger.info(f"URL - {url}")
        payload = {"token": token, "status": new_status}
        response = requests.put(url, params=payload)
        success = response.status_code == 200

        response.raise_for_status()

        if success:
            logger.info(f"Заказ {order.get('number')} успешно переведен в статус {new_status}.")
        else:
            logger.error(f"Неожиданный код ответа: {order.get('number')}. Код: {response.status_code}")
            raise UpdateOrderError(
                f"Неожиданный код ответа: {order.get('number')}. Код: {response.status_code}"
            )

    except requests.RequestException as e:
        error_info = f"Ошибка изменения статуса заказа {order.get('number')}. Ошибка: {e}"
        logger.exception(error_info)
        raise NetworkError(error_info, e)

    except Exception as e:
        logger.exception(f"Неожиданная ошибка при изменении статуса заказа {order.get('number')}: {e}")
        raise UpdateOrderError(f"Неожиданная ошибка при изменении статуса заказа {order.get('number')}", e)
