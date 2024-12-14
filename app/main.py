# TODO: Добавить проверку количества заказов в определенном статусе

from fastapi import FastAPI
from app.api import endpoints
from app.core.logger_settings import logger_setup

logger_setup()

app = FastAPI(title="OrderCloser API", version="1.0.0")

# Подключение маршрутов
app.include_router(endpoints.router)
