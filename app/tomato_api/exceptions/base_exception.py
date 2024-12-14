import traceback
from typing import Optional, List


class SmartomatoAPIError(Exception):
    """Базовый класс исключений для работы с API Smartomato"""

    def __init__(self, message: str, original_error: Optional[Exception] = None):
        # Используем typing для явного указания опционального типа
        super().__init__(message)
        self.original_error = original_error

        # Добавляем информацию об оригинальной ошибке более явно
        if original_error:
            # Используем f-строку для форматирования
            original_error_info = f"\nОригинальная ошибка: {type(original_error).__name__}: {str(original_error)}"
            self.args += (original_error_info,)

    def get_traceback(self) -> List[str]:
        """
        Возвращает трассировку ошибки.

        :return: Список строк с трассировкой
        """
        try:
            if self.original_error:
                # Используем оригинальную ошибку, если она есть
                return traceback.format_exception(
                    type(self.original_error),
                    self.original_error,
                    self.original_error.__traceback__
                )
            else:
                # Используем текущую трассировку, если нет оригинальной
                return traceback.format_tb(self.__traceback__)
        except Exception as e:
            # Защита от возможных ошибок при получении трассировки
            return [f"Ошибка при получении трассировки: {e}"]

    def __str__(self) -> str:
        """
        Переопределяем строковое представление для более информативного вывода
        """
        base_message = super().__str__()

        if self.original_error:
            return f"{base_message}\nОригинальная ошибка: {type(self.original_error).__name__}: {str(self.original_error)}"

        return base_message

