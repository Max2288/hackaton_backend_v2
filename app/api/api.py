from fastapi import APIRouter

from app.api import minio, eltc, mail
from app.api.log_route import LogRoute

router = APIRouter(route_class=LogRoute)

router.include_router(minio.router, prefix="/minio", tags=["MINIO API"])
router.include_router(eltc.router, prefix="/eltc", tags=["ELTC API"])
router.include_router(mail.router, prefix="/mail", tags=["EMAIL API"])