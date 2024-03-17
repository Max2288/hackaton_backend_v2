from fastapi import APIRouter, HTTPException, status
from loguru import logger
from app.api.log_route import LogRoute
from opensearchpy import OpenSearch

from app.core.config import Config

router = APIRouter(route_class=LogRoute)


async def load_index(document: dict, order_id: int):
    try:
        client = OpenSearch(
            hosts=[Config.SEARCH_ENGINE_HOST],
            http_compress=True,
            use_ssl=False,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False
        )

        response = client.index(
            index='orders',
            body=document,
            id=order_id,
            refresh=True
        )
        return response
    except Exception as e:
        logger.error(f"Произошла ошибка во создания заказа: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/read-from-index", status_code=status.HTTP_200_OK)
async def read_from_index(id: int):
    try:
        client = OpenSearch(
            hosts=[Config.SEARCH_ENGINE_HOST],
            http_compress=True,
            use_ssl=False,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False
        )
        response = client.get(
            index='orders',
            id=id
        )
        return response["_source"]

    except Exception as e:
        logger.error(f"Произошла ошибка при чтении данных из индекса: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.get("/search-in-index", status_code=status.HTTP_200_OK)
async def search_in_index(query: str):
    try:
        client = OpenSearch(
            hosts=[Config.SEARCH_ENGINE_HOST],
            http_compress=True,
            use_ssl=False,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False
        )

        body = {
            "query": {
                "match": {
                    "segments.text": {
                        "query": query
                    }
                }
            }
        }

        response = client.search(
            index='orders',
            body=body
        )

        return response['hits']['hits']

    except Exception as e:
        logger.error(f"Произошла ошибка при выполнении поиска в индексе: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")