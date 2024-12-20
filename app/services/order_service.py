from fastapi import HTTPException
from loguru import logger

from app.core.settings import SETTINGS
from app.tomato_api.exceptions.extentions import GetOrdersError, NetworkError, UpdateOrderError
from app.tomato_api.orders import get_orders_per_status, cancel_new_orders, close_orders


def cancel_unpaid_orders_service(token: str, archive: bool = True) -> None:
    """
    Отменяет заказы со статусом новый. Только неоплаченные
    :param token: Токен аутентификации смартомато
    :param archive: Если True - отменяем и архивные заказы(старше 2ух недель).
    """
    logger.info("Начало отмены новых заказов")

    count_orders = SETTINGS.COUNT_ORDERS_FOR_GET_ORDERS

    try:
        new_orders = get_orders_per_status(
            count=count_orders,
            status="pending",  # pending стоит у заказов со статусом новый
            payment_status="unpaid",  # Собираем только неоплаченные
            token=token,
            archive=archive
        )

        # Закрываем полученные заказы
        result_info = cancel_new_orders(orders=new_orders, token=token)
        logger.info(f"Отмена заказов завершена: {result_info}")

    except (GetOrdersError, NetworkError, UpdateOrderError) as e:
        logger.exception("Ошибка при отмене новых заказов")
        raise HTTPException(
            status_code=500, detail=f"Ошибка при отмене заказов: {e}"
        ) from e

    except Exception as e:
        logger.exception("Непредвиденная ошибка при отмене новых заказов")
        raise HTTPException(
            status_code=500, detail=f"Внутрення ошибка сервера: {e}"
        ) from e


async def close_confirmed_orders_service(token: str, archive: bool = True) -> str:
    """
    Закрывает заказы со статусом подтвержден.
    :param token: Токен аутентификации смартомато
    :param archive: Если True - закрываем и архивные заказы(старше 2ух недель).
    """
    logger.info("Начало закрытия подтвержденных заказов")

    count_orders = SETTINGS.COUNT_ORDERS_FOR_GET_ORDERS
    try:
        confirm_orders = get_orders_per_status(
            count=count_orders,
            status="confirm",
            token=token,
            archive=archive
        )

        # Закрываем полученные заказы
        result_info = await close_orders(orders=confirm_orders, token=token)
        logger.info(f"Закрытие заказов завершено: {result_info}")

        return result_info

    except (GetOrdersError, NetworkError, UpdateOrderError) as e:
        logger.exception("Ошибка при закрытии подтвержденных заказов")
        raise HTTPException(
            status_code=500, detail=f"Ошибка при закрытии заказов: {e}"
        ) from e

    except Exception as e:
        logger.exception("Непредвиденная ошибка при закрытии подтвержденных заказов")
        raise HTTPException(
            status_code=500, detail=f"Внутрення ошибка сервера: {e}"
        ) from e
