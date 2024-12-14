from typing import Optional

from .base_exception import SmartomatoAPIError


class NetworkError(SmartomatoAPIError):
    """Исключение для сетевых ошибок при работе с API"""
    def __init__(
            self,
            message: str = "Сетевая ошибка при работе с Smartomato API",
            original_error: Optional[Exception] = None
    ):
        super().__init__(message, original_error)


class UpdateOrderError(SmartomatoAPIError):
    """Исключение для ошибок при обновлении заказа"""
    def __init__(self, message: str = "Ошибка при обновлении заказа", original_error: Optional[Exception] = None):
        super().__init__(message, original_error)


class GetOrdersError(SmartomatoAPIError):
    """Исключение для ошибок при получении списка заказов"""
    def __init__(self, message: str = "Ошибка при получении списка заказов", original_error: Optional[Exception] = None):
        super().__init__(message, original_error)
