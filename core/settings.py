from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv() # Загружаем переменные среды из .env

class Settings(BaseSettings):

    TOMATO_LOGIN: str
    TOMATO_PASSWORD: str

    BASE_API_URL: str = "http://smartomato.ru/api"


SETTINGS = Settings()
