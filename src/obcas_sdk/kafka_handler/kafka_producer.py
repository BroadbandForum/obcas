# Copyright 2025 Broadband Forum
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Created by Madhukar Shetty (Nokia) in January 2025


"""
This module provides a KafkaProducer class that allows you to publish messages to a Kafka topic using the aiokafka library.

The module also includes a Worker class that runs a thread with an asyncio event loop for asynchronous publishing of messages to Kafka.

The module uses the KafkaSslContext class from kafka_ssl_context.py module to get SSL context for Kafka producer.

The module contains the following classes:

    - Worker: A class that runs a thread with an asyncio event loop for asynchronous publishing of messages to Kafka.
    - KafkaProducer: A class that allows you to publish messages to a Kafka topic using the aiokafka library.
"""

import os
import logging
import asyncio
from threading import Thread
from functools import partial
from aiokafka import AIOKafkaProducer

KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER", "kafka:9092")
LOGGER = logging.getLogger('kafka_producer')

class Worker(Thread):

    def __init__(self, name=None):
        """
        Initializes a new instance of the class.

        Args:
            name (str, optional): A string representing the name of the instance. Defaults to None.

        """
        super().__init__(name=name)
        self.loop = asyncio.new_event_loop()

    async def _wrapper(self, task, *args):
        """This is a private function that runs the given coroutine function with the given arguments in an asyncio event loop.

            Args:
                task (coroutine function): A coroutine function to run in the event loop.
                args (Any): Arguments to pass to the coroutine function.

            Returns:
                None
        """
        await task(*args)

    def run(self) -> None:
        """This function starts the event loop in a separate thread.

            Returns:
                None
        """
        LOGGER.info(f"{self._name}: AIO Kafka Producer thread started")
        self.loop.run_forever()

    def post(self, task, *args):
        """This function posts a coroutine function to the event loop.

           Args:
               task (coroutine function): A coroutine function to run in the event loop.
               args (Any): Arguments to pass to the coroutine function.

           Returns:
               None
        """
        self.loop.call_soon_threadsafe(self.loop.create_task, self._wrapper(task, *args))

class KafkaProducer:

    def __init__(self, callback=None):
        """
        A Kafka producer that sends messages to a specified Kafka server.

        Attributes:
            producer (kafka.KafkaProducer): A Kafka producer instance used to send messages.
            wt (Worker): A worker thread that runs in the background and starts the producer.
            callback (function): A callback function to invoke after successfully starting the producer

        Raises:
            Exception: If the Kafka server is not defined.

        """
        LOGGER.info("Kafka Producer Configuration ")
        try:
            if KAFKA_SERVER is None:
                raise Exception('Kafka Server must be defined')
            self.producer = None
            self.wt = Worker()
            self.wt.daemon = True
            self.wt.start()
            self.wt.post(self._start_producer, callback)
            LOGGER.info('kafka producer initialized successfully')
        except Exception:
            LOGGER.error('Error initializing Kafka Producer', exc_info=True)

    async def _start_producer(self, callback=None):
        """This is a private function that starts the Kafka producer.

            Returns:
                None
        """
        LOGGER.info("Starting Kafka Producer")
        self.producer = AIOKafkaProducer(
                bootstrap_servers=KAFKA_SERVER,
                max_batch_size=163840,
                linger_ms=0)
        await self.producer.start()
        LOGGER.info('Kafka Producer is started')
        if callback is not None:
            self.invoke_callback("Success", callback)

    def publish_message(self, topic_name, value, success_call_back, error_call_back, key=None):
        LOGGER.info('publishing the message')
        """This function publishes a message to the specified Kafka topic.

           Args:
               topic_name (str): The name of the Kafka topic.
               value (str): The message to publish.
               success_call_back (callable): A callable object that will be called if the message is published successfully.
               error_call_back (callable): A callable object that will be called if an error occurs while publishing the message.
               key (str, optional): The key for the message. Defaults to None.

           Returns:
               None
        """
        self.wt.post(self.__send, topic_name, value, success_call_back, error_call_back, key)

    def invoke_callback(self, value, f, *args, **kwargs):
        """This function invokes a callback function with the specified arguments.

            Args:
                value (Any): The value to pass as the first argument to the callback function.
                f (callable): The callback function to invoke.
                args (Any): Additional arguments to pass to the callback function.
                kwargs (Any): Additional keyword arguments to pass to the callback function.

            Returns:
                None
        """
        if args or kwargs:
            f = partial(f, *args, **kwargs)
        f(value)

    async def __send(self, topic_name, value, success_call_back, error_call_back, key=None):
        """This is a private function that sends a message to the specified Kafka topic.

            Args:
                topic_name (str): The name of the Kafka topic.
                value (str): The message to send.
                success_call_back (callable): A callable object that will be called if the message is sent successfully.
                error_call_back (callable): A callable object that will be called if an error occurs while sending the message.
                key (str, optional): The key for the message. Defaults to None.

            Returns:
                None
        """

        key_bytes = None
        try:
            value_bytes = bytes(value, encoding='utf-8')
            if key:
                key_bytes = bytes(key, encoding='utf-8')
            res = await self.producer.send_and_wait(topic_name, value_bytes, key_bytes)
            LOGGER.info("__send result: %s", str(res))
            if success_call_back is not None:
                self.invoke_callback(res, success_call_back)
            return res
        except Exception as e:
            LOGGER.exception("Error occurred while publishing message to kafka:", exc_info=True)
            if error_call_back is not None:
                self.invoke_callback(e, error_call_back)
