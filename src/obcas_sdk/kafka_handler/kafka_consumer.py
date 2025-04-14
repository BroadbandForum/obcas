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
This module is responsible for creating a Kafka Consumer which can receive messages from a Kafka topic.

KafkaConsumer: Class which creates a Kafka Consumer and has functions to interact with it.

    - __init__: Initializes the Kafka Consumer with a given group and topic.
    - close: Closes the Kafka Consumer.
    - get_topics: Returns the topics being consumed by the Kafka Consumer.
    - start_consumer: Starts the Kafka Consumer.
    - get_many: Returns many messages from the Kafka Consumer for a given partition.
    - stop: Stops the Kafka Consumer.
    - get_one: Returns a single message from the Kafka Consumer.
    - to_committed: Seeks to the committed offset of the Kafka Consumer.

Constants:

KAFKA_SERVER: The server which hosts the Kafka broker.
KAFKA_SECURITY_PROTOCOL: The security protocol used to connect to Kafka.
"""

import asyncio
import os
import logging
from aiokafka import AIOKafkaConsumer

KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER", "kafka:9092")
LOGGER = logging.getLogger('kafka_consumer')

class KafkaConsumer:

    def __init__(self, group, topic):
        """Initialize the Kafka Consumer with a specified consumer group, topic and event loop.

        Args:
            group (str): The Kafka consumer group to which this consumer belongs.
            topic (str): The Kafka topic from which messages will be consumed.
            loop (asyncio.AbstractEventLoop): The asyncio event loop instance.

        Raises:
            Exception: If KAFKA_SERVER environment variable is not defined.

        Returns:
            None
        """

        try:
            if KAFKA_SERVER is None:
                raise Exception('Kafka Server must be defined')
            self.group = group
            self.closed = False
            LOGGER.info("Starting Kafka Consumer %s ", KAFKA_SERVER)
            self.consumer = AIOKafkaConsumer(
                topic,
                bootstrap_servers=KAFKA_SERVER)
            LOGGER.info("Starting consumer %s ", KAFKA_SERVER)
        except Exception:
            LOGGER.error('Error initializing Kafka Consumer', exc_info=True)

    def close(self):
        """Stop the Kafka Consumer and close the connection to Kafka.

        Returns:
            None
        """

        self.closed = True
        self.consumer.stop()
        LOGGER.info('Kafka connection closed')

    def get_topics(self):
        """Get the list of topics that are available to this Kafka Consumer.

        Returns:
            list: List of available topics.
        """

        return self.consumer.topics()

    def start_consumer(self):
        """Start the Kafka Consumer and begin consuming messages from Kafka.

        Returns:
            asyncio.Task: An asyncio.Task object representing the consumer task.
        """

        return self.consumer.start()

    def get_many(self, partition):
        """Get messages from multiple partitions of the Kafka topic.

        Args:
            partition (Union[int, Tuple[int]]): The partition(s) from which to consume messages.

        Returns:
            Dict[TopicPartition, List[ConsumerRecord]]: A dictionary of messages, keyed by partition number.
        """

        return self.consumer.getmany(partition, timeout_ms=0, max_records=0)

    def stop(self):
        """Stop the Kafka Consumer from consuming messages.

        Returns:
            asyncio.Task: An asyncio.Task object representing the consumer task.
        """

        return self.consumer.stop()

    def get_one(self):
        """Get one message from the Kafka topic.

        Returns:
            ConsumerRecord: The message consumed from Kafka.
        """

        return self.consumer.getone()

    def to_committed(self):
        """Seek to the committed offsets for the assigned partitions.

        Returns:
            None
        """

        return self.consumer.seek_to_committed()