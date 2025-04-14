# Copyright 2024 Broadband Forum
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


from fluent import handler
import os
import logging

GETTING_CUR_CONTAINER_ID_COMMAND = "head -n 1 /proc/1/cgroup | awk -F/ '{print $NF}'| sed 's/:/-/g'"
DEFAULT_FLUENTD_LOG_DIRECT_URL = 'localhost:24224'
DEFAULT_LOG_LEVEL = 'INFO'

def encode_exception(obj):
    """
    Encodes exceptions to a dictionary format.

    Args:
        obj: The object to encode.

    Returns:
        dict: Encoded exception in a dictionary format.
    """
    if isinstance(obj, Exception):
        return {"class": type(obj).__name__, "args": obj.args}
    return obj


class FluentdLogger:
    """
    Class for setting up a Fluentd logger.
    """
    def __init__(self):
        self.logger = None

    def install(self, application_name, category_log_levels_dict=None):
        """
        Installs the Fluentd logger.

        Args:
            application_name (str): The name of the application.
            category_log_levels_dict (dict, optional): Dictionary containing log levels for specific categories.

        """
        hostname = os.getenv('HOSTNAME')
        containerIdOutput = os.popen(GETTING_CUR_CONTAINER_ID_COMMAND).read().rstrip()
        self.containerName = os.getenv('FLUENTD_LOG_DIRECT_TAG', application_name)
        self.containerId = hostname if not containerIdOutput else containerIdOutput
        tagPrefix = 'docker.{}'.format(hostname)

        fluentdURL = os.getenv('FLUENTD_LOG_DIRECT_URL', DEFAULT_FLUENTD_LOG_DIRECT_URL)
        fluentdConfigArr = fluentdURL.split(':')
        logLevelAsString = os.getenv('LOG_LEVEL', DEFAULT_LOG_LEVEL)
        logLevel = logging.getLevelName(logLevelAsString)

        msgFormat = self.getLogFormat(application_name)

        logging.basicConfig(level=logLevel)
        hler = handler.FluentHandler(tagPrefix, host=fluentdConfigArr[0], port=int(fluentdConfigArr[1]), msgpack_kwargs={'default' : encode_exception}, verbose=False)

        formatter = handler.FluentRecordFormatter(msgFormat)
        hler.setFormatter(formatter)

        logging.getLogger().handlers = []
        logging.getLogger().addHandler(hler)

        wzlogger = logging.getLogger('werkzeug')
        wzlogger.handlers = []

        schedule_logger = logging.getLogger('schedule')
        if logLevelAsString == "DEBUG":
            schedule_logger.setLevel("INFO")
            wzlogger.setLevel("INFO")
        else:
            schedule_logger.setLevel("WARN")
            wzlogger.setLevel("WARN")

        self._set_category_loglevel(category_log_levels_dict)

        self.logging = logging.getLogger('application')

    def getLogFormat(self, application_name):
        """
        Get log format.

        Args:
            application_name (str): The name of the application.

        Returns:
            dict: The log format dictionary.
        """
        logMessageFormat = '%(message)s'
        logFormat = {
            'container_name': self.containerName,
            'container_id': self.containerId,
            'log': logMessageFormat,
            'application': application_name,
            'level': '%(levelname)s',
            'category': '%(name)s',
            'throwable': '%(exc_text)s',
            'thread': '%(threadName)s'
        }
        return logFormat

    def getLogger(self):
        """
        Get the logger object.

        Returns:
            logger: The logger object.
        """
        return self.logger

    def _set_category_loglevel(self, third_party_app_dict):
        """
        Set log levels for specific categories.

        Args:
            third_party_app_dict (dict): Dictionary containing log levels for specific categories.
        """
        if third_party_app_dict is not None:
            for app_name, log_level in third_party_app_dict.items():
                app_logs = logging.getLogger(app_name)
                app_logs.setLevel(log_level)