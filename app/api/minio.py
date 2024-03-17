
import aiohttp
import requests

from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from loguru import logger

from app.api.eltc import load_index
from app.api.log_route import LogRoute
from miniopy_async import Minio

from app.core.config import Config

from app.record.parser import parse_consumer_record

from app.services.temprorary_files import tmp_image_folder

router = APIRouter(route_class=LogRoute)


client = Minio("host.docker.internal:9000", access_key="minioadmin", secret_key="minioadmin", secure=False)
consumer = AIOKafkaConsumer(
    Config.KAFKA_TOPIC,
    bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
    group_id=Config.KAFKA_CONSUMER_GROUP,
    enable_auto_commit=False,
)


@router.post("/get", status_code=status.HTTP_200_OK)
async def get_kafka():
    try:
        await consumer.start()
        async for record in consumer:
            try:
                parsed_record = parse_consumer_record(record)
                file_path = parsed_record["value"]["file_path"]
                with tmp_image_folder() as file:
                    async with aiohttp.ClientSession() as session:
                        response = await client.get_object(bucket_name=Config.BUCKET_NAME, object_name=file_path,
                                                           session=session)
                        files = {'file': ('tmp.mp3', await response.read(), 'audio/mpeg')}
                        res = await send_file_request(files, parsed_record["value"]["order_id"])
                        response = await load_index(res, res['order_id'])
                        logger.info(response)

                        await send_status_reuest(1, response['order_id'])
                await consumer.commit()
            except Exception as e:
                logger.error(e)

        await consumer.stop()
        return 200
    except Exception as e:
        logger.error(f"Произошла ошибка во создания заказа: {e}")
        await consumer.stop()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


async def send_file_request(files, order_id):
    headers = {
        'accept': 'application/json',
    }

    params = {
        'order_id': order_id,
    }

    response = requests.post('http://158.160.17.242:8003/transcribe_file/', params=params, headers=headers, files=files)
    if response.status_code == 200:
        pass
    return response.json()


async def send_status_reuest(user_id, order_name):
    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    params = {
        'user_id': user_id,
        'status_name': 'success',
        'order_id': order_name,
    }

    response = requests.post('http://158.160.17.242:8011/stenagrafist/api/v1/minio/change', params=params,
                             headers=headers)