# APIs

## Netconf Client API

### send_nc_request

To send different netconf operations (get, edit-config, action and get-config) to BAA. 
Sample netconf requests can be found [here](../../src/obcas_sdk/nc_client)

```
send_nc_request(operation, template_name, *args)
Args:
operation (str): netconf operation to be performed(get,get-config,edit-config, action).
template_name (xml): rpc reqest body

Returns:
retruns netconf response from OB-BAA server
```

### create_subscription_and_take_notification

This creates the subscription to the provided notification stream and reads the notification from the stream.

```
create_subscription_and_take_notification(self)
Args:
stream (str): name of the stream on which we need to read the notification from(netconf, alarm, state-change)

Returns:
retruns netconf notification from given stream
```

## Opensearch API

The API enabless to establish a client connection to open-search database and can perform below operations


```
__init__(self)
Initialize opensearch_client that can be used for the future operations.
 
add_data_to_index(self, os_index, message, id=None)
    Adds the specified data to the specified index.
    Circuit breaker protects add the specified data to the specified index.
  
Args:
    os_index (str): The name of the index to add the data to.
    message (dict): The data to add.
  
Returns:
    dict: The response from Opensearch
  
Raises:
    CircuitBeakerError : If a circuit breaker error has occurred when trying to add the specified data to the Opensearch.
 
add_index(self, os_index, index_body)
    Adds the specified index into opensearch
    Circuit breaker protects add the specified data to the specified index.
  
Args:
    os_index (str): The name of the index
    index_body (dict): index mapping and details
  
Returns:
    dict: The response from Opensearch
  
Raises:
    CircuitBeakerError : If a circuit breaker error has occurred when trying to add the specified data to the Opensearch.
 
check_if_document_exists_in_index(self, index, document_id)
    Checks if the document exists in index
 
close_connection(self)
Disconnect to opensearch_handler server
 
delete_document_from_index(self, index, document_id)
    Deletes a given document from the index.
 
get_indexes(self, indexes)
 
search(self, os_index, search_body)
    Searches for data in the specified index using the provided search body.
    Circuit breaker protect to get data form Opensearch.
  
Args:
    os_index (str): The name of the index to search.
    search_body (dict): The search body.
  
Returns:
    dict: The search results.
  
Raises:
    CircuitBeakerError : If a circuit breaker error has occurred when trying to get data from Opensearch.
 
update_data_to_index(self, os_index, message, doc_id)
updates the specified data into opensearch index
Circuit breaker protects add the specified data to the specified index.
  
Args:
    os_index (str): The name of the index
    index_body (dict): index mapping and details
  
Returns:
    dict: The response from Opensearch
  
Raises:
    CircuitBeakerError : If a circuit breaker error has occurred when trying to add the specified data to the

```

## KAFKA API

###  KAFKA Producer

The module contains the following classes:

    - Worker: A class that runs a thread with an asyncio event loop for asynchronous publishing of messages to Kafka.
    - KafkaProducer: A class that allows you to publish messages to a Kafka topic using the aiokafka library.

#### classes

```
builtins.object

    KafkaProducer

threading.Thread(builtins.object)

    Worker


class KafkaProducer(builtins.object)
KafkaProducer(callback=None)

```

#### methods

```
__init__(self, callback=None)
    A Kafka producer that sends messages to a specified Kafka server.
      
    Attributes:
        producer (kafka.KafkaProducer): A Kafka producer instance used to send messages.
        wt (Worker): A worker thread that runs in the background and starts the producer.
        callback (function): A callback function to invoke after successfully starting the producer
      
    Raises:
        Exception: If the Kafka server is not defined.
 
invoke_callback(self, value, f, *args, **kwargs)
    This function invokes a callback function with the specified arguments.
      
    Args:
        value (Any): The value to pass as the first argument to the callback function.
        f (callable): The callback function to invoke.
        args (Any): Additional arguments to pass to the callback function.
        kwargs (Any): Additional keyword arguments to pass to the callback function.
      
    Returns:
        None
 
publish_message(self, topic_name, value, success_call_back, error_call_back, key=None)

```
```
__init__(self, name=None)
Initializes a new instance of the class.

    Args:
        name (str, optional): A string representing the name of the instance. Defaults to None.

post(self, task, *args)
This function posts a coroutine function to the event loop.

    Args:
        task (coroutine function): A coroutine function to run in the event loop.
        args (Any): Arguments to pass to the coroutine function.
      
    Returns:
        None

run(self) -> None
This function starts the event loop in a separate thread.

    Returns:
        None
```

###  KAFKA consumer

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

#### constants
```
KAFKA_SERVER: The server which hosts the Kafka broker.
KAFKA_SECURITY_PROTOCOL: The security protocol used to connect to Kafka
```

#### classes

```
               
builtins.object
 
    KafkaConsumer
 
  
class KafkaConsumer(builtins.object)
        KafkaConsumer(group, topic)


```
#### methods

```
__init__(self, group, topic)
    Initialize the Kafka Consumer with a specified consumer group, topic and event loop.
      
    Args:
        group (str): The Kafka consumer group to which this consumer belongs.
        topic (str): The Kafka topic from which messages will be consumed.
        loop (asyncio.AbstractEventLoop): The asyncio event loop instance.
      
    Raises:
        Exception: If KAFKA_SERVER environment variable is not defined.
      
    Returns:
        None
 
close(self)
    Stop the Kafka Consumer and close the connection to Kafka.
      
    Returns:
        None
 
get_many(self, partition)
    Get messages from multiple partitions of the Kafka topic.
      
    Args:
        partition (Union[int, Tuple[int]]): The partition(s) from which to consume messages.
      
    Returns:
        Dict[TopicPartition, List[ConsumerRecord]]: A dictionary of messages, keyed by partition number.
 
get_one(self)
    Get one message from the Kafka topic.
      
    Returns:
        ConsumerRecord: The message consumed from Kafka.
 
get_topics(self)
    Get the list of topics that are available to this Kafka Consumer.
      
    Returns:
        list: List of available topics.
 
start_consumer(self)
    Start the Kafka Consumer and begin consuming messages from Kafka.
      
    Returns:
        asyncio.Task: An asyncio.Task object representing the consumer task.
 
stop(self)
    Stop the Kafka Consumer from consuming messages.
      
    Returns:
        asyncio.Task: An asyncio.Task object representing the consumer task.
 
to_committed(self)
    Seek to the committed offsets for the assigned partitions.
      
    Returns:
        None

```
## FluentD API

This API forwards the container logs into fluendD.

#### data

```
install(self, application_name, category_log_levels_dict=None):
       Installs the Fluentd logger.
 
       Args:
           application_name (str): The name of the application.
           category_log_levels_dict (dict, optional): Dictionary containing log levels for specific categories.
 
   getLogFormat(self, application_name):
      Get log format.
 
       Args:
           application_name (str): The name of the application.
 
       Returns:
           dict: The log format dictionary.
 
   getLogger(self):
       Get the logger object.
       Returns:
           logger: The logger object.


```
#### usage
```
    if "fluentd" == os.getenv("LOG_OPT"):
        FluentdLogger().install('app_name')
```




An overview of the applications developed and currently available that make use of one or 
multiple of the above APIs can be found [here](../../apps/index.md)

 [<-- Overview](../overview/index.md)

 [Apps -->](../../apps/index.md)
