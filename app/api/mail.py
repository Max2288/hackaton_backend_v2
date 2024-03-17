from fastapi import APIRouter, HTTPException, status
from loguru import logger

from app.api.log_route import LogRoute

router = APIRouter(route_class=LogRoute)

@router.post("/", status_code=status.HTTP_200_OK)
async def send_mail(email: str):
    try:
        pass
    except Exception as e:
        logger.error(f"Произошла ошибка во создания заказа: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")