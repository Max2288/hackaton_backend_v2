import os
from asyncio import sleep

import aiohttp
from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter, HTTPException, status
from loguru import logger
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
                        response = await client.get_object(bucket_name=Config.BUCKET_NAME, object_name=file_path, session=session)
                        # На завтра await response, order_id = parsed_record["value"]["order_id"]
                        with open(f'{file}/tmp.mp3', 'wb') as f:
                            f.write(await response.read())
                            await sleep(1000000000000000000)
                await consumer.commit()
            except Exception as e:
                logger.error(e)

        await consumer.stop()
        return 200
    except Exception as e:
        logger.error(f"Произошла ошибка во создания заказа: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
