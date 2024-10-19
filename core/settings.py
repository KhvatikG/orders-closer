from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv() # Загружаем переменные среды из .env

class Settings(BaseSettings):

    TOMATO_LOGIN: str
    TOMATO_PASSWORD: str

    COUNT_ORDERS_FOR_GET_ORDERS: int = 5

    BASE_API_URL: str = "http://smartomato.ru/api"


SETTINGS = Settings()
