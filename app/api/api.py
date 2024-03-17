from fastapi import APIRouter

from app.api import minio
from app.api.log_route import LogRoute

router = APIRouter(route_class=LogRoute)

router.include_router(minio.router, prefix="/minio", tags=["MINIO API"])
