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
#
# Created by Jafar Hamin (Nokia) in March 2024


import threading
import os
from mylogging import get_logger
from alarm import get_alarms
from util import Util
from retriever import Retriever


ALARM_SYNCH_INTERVAL_SEC = int(os.environ.get('ALARM_SYNCH_INTERVAL_SEC', 10))

logger = get_logger()

class AlarmHandler:
    def periodically_update_alarms():
        logger.info('\n\n\n##################### Updating alarms ...')
        AlarmHandler.update_alarms()
        threading.Timer(ALARM_SYNCH_INTERVAL_SEC, AlarmHandler.periodically_update_alarms).start()

    def update_alarms():
        alarms = Retriever.retrieve_alarms()
        logger.debug('alarms')
        for alarm in alarms:
            logger.debug(alarm)
        AlarmHandler.update_devices_alarms(alarms)

    def update_devices_alarms(alarms):
        alarms_json = AlarmHandler.format_devices_alarms(alarms)
        get_alarms().set(alarms_json)

    def format_devices_alarms(alarms):
        return Util.documents_to_json(alarms, 'deviceRefId', multiple_value=True)

