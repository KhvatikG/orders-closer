from tomato_api.core.settings import SETTINGS
from tomato_api.auth_method import get_tomato_auth_token
from tomato_api.get_orders import get_orders_per_status
from tomato_api.close_orders import close_orders

# Получаем токен авторизации
auth_data = get_tomato_auth_token()
token = auth_data.get("token")

# Получаем count_orders(кол-во) заказов со статусом "Подтвержден"
count_orders = SETTINGS.COUNT_ORDERS_FOR_GET_ORDERS
confirm_orders = get_orders_per_status(
    count = count_orders,
    status="confirm",
    token=token
)

# Закрываем полученные заказы
close_orders(
    orders=confirm_orders,
    token=token
)
