import json
import pika
from logzero import logger

import settings


class RabbitMQClient(object):
    _conn = None
    _channel = None

    def __init__(self):
        self.configs = settings.load_config()

        self.host = self.configs.RABBIT_HOST
        self.port = self.configs.RABBIT_PORT
        self.username = self.configs.RABBIT_USER
        self.password = self.configs.RABBIT_PASSWORD
        self.vhost = self.configs.RABBIT_VHOST
        self.exchange = self.configs.EXCHANGE_NAME

    @property
    def credentials(self) -> pika.PlainCredentials:
        return pika.PlainCredentials(self.username, self.password)

    @property
    def connection_parameters(self) -> pika.ConnectionParameters:
        return pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.vhost,
            credentials=self.credentials,
            heartbeat=180,
        )

    def _get_connection(self, params):
        try:
            if RabbitMQClient._conn:
                self._conn = RabbitMQClient._conn
            else:
                self._conn = RabbitMQClient._conn = pika.BlockingConnection(
                    params)
                logger.info(
                    f"RabbitMQ --->> New connection in {self.host}:{self.port}")
        except Exception as ex:
            logger.warning(f"RabbitMQ --->> Failed connection {ex}")

    @property
    def conn(self) -> pika.BlockingConnection:
        if self._conn is None:
            self._get_connection(self.connection_parameters)

        return self._conn

    def _get_channel(self):
        if RabbitMQClient._channel:
            self._channel = RabbitMQClient._channel
        else:
            self._channel = RabbitMQClient._channel = self.conn.channel()

    @property
    def channel(self):
        if self._channel is None:
            self._get_channel()

        return self._channel

    def _stop_channel(self):
        self.channel.stop_consuming()
        RabbitMQClient._channel = None
        logger.info(
            "RabbitMQ --->> Sending a basic.cancel rpc command to rabbitmq")

    def _stop_connection(self):
        self.conn.close()
        RabbitMQClient._conn = None
        logger.info("RabbitMQ --->> Connection closed")

    def stop(self):
        self._stop_channel()
        self._stop_connection()

    def on_search_fail(self, properties, data):
        try:
            properties.headers[settings.RETRY_COUNTER_HEADER_NAME] += 1
            if properties.headers[settings.RETRY_COUNTER_HEADER_NAME] < settings.MESSAGE_PROCESSING_MAX_ATTEMPTS:
                self.publish(exchange=settings.EXCHANGE_NAME, routing_key=settings.CONSUME_ROUTING_KEY, message=data,
                             properties=properties)
        except TypeError:
            properties.headers = {settings.RETRY_COUNTER_HEADER_NAME: 1}
            self.publish(exchange=settings.EXCHANGE_NAME, routing_key=settings.CONSUME_ROUTING_KEY, message=data,
                         properties=properties)

        except KeyError:
            properties.headers[settings.RETRY_COUNTER_HEADER_NAME] = 1
            self.publish(exchange=settings.EXCHANGE_NAME, routing_key=settings.CONSUME_ROUTING_KEY, message=data,
                         properties=properties)

    def publish(self, exchange: str, routing_key: str, message: dict, properties=None):
        logger.info(f"TO QUEUE --->> {routing_key} | PACKAGE SENDED --->> {message}")
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(message),
                                   properties=properties)