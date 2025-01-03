from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

from app.services.order_service import cancel_unpaid_orders_service, close_confirmed_orders_service
from loguru import logger

router = APIRouter()


class TokenBody(BaseModel):
    """
    Тело запроса для получения токена
    """
    token: str


@router.get("/health")
async def health_check():
    return {"status": "healthy"}


@router.post("/orders/cancel-unpaid")
async def cancel_unpaid_orders_endpoint(token: str):
    """
    Эндпоинт для отмены новых неоплаченных заказов.
    """
    ...


@router.post("/orders/close-confirmed")
async def close_confirmed_orders_endpoint(body: TokenBody = Body(...)):
    """
    Эндпоинт для закрытия подтвержденных заказов.
    """
    try:
        token = body.token
        result_info = await close_confirmed_orders_service(token)
        return {"message": result_info}
    except HTTPException as e:
        raise e  # Передаем HTTPException дальше
    except Exception as e:
        logger.exception(f"Непредвиденная ошибка в эндпоинте")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера") from e


@router.get("/orders/count")
async def count_orders_endpoint(token: str, status: str):
    """
    Эндпоинт для получения количества заказов.
    """
    return
