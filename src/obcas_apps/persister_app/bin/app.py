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

from threading import Thread

import alarm_utils as alarm_utils
import persister_app_constants as pa_const
import persister_app_utils as pa_utils
import topology_utils as tp_utils
import defect_notification_utils as df_utils
from base_logging.fluentd_logger import FluentdLogger
import os


def main():

    if "fluentd" == os.getenv("LOG_OPT"):
        FluentdLogger().install('persister_app')

    #pre-requisites create indexes required for persister app
    pa_utils.create_opensearch_indexes()

    # subscribe to alarm stream and persist
    # the alarm-notifications into opensearch DB
    alarm_persister_thread = Thread(target=alarm_utils.fetch_and_persist_alarm, daemon=True,
                                    name=pa_const.ALARM_PERSISTER_THREAD)
    alarm_persister_thread.start()

    # subscribe to config change notification stream and update device topology based on
    # the onu-presence-state-change/netconf config change notification
    topology_persister_notification_thread = Thread(target=tp_utils.fetch_topology_based_on_notification,
                                                    name=pa_const.TOPOLOGY_PERSISTER_NOTIFICATION_THREAD)
    topology_persister_notification_thread.start()

    # get device details every 24 hours and update the topology for all devices
    topology_persister_timer_thread = Thread(target=tp_utils.fetch_and_persist_topology,
                                             name=pa_const.TOPOLOGY_PERSISTER_TIMER_THREAD)
    topology_persister_timer_thread.start()

    # subscribe to NETCONF stream and persists ONU defect notifications
    defect_notification_persister_thread = Thread(target=df_utils.fetch_and_persist_defect_notification,
                                             name=pa_const.DEFECT_NOTIFICATION_PERSISTER_THREAD)
    defect_notification_persister_thread.start()

    # start REST server to fetch external topology
    rest_server_thread_for_external_topology = Thread(target=tp_utils.start_rest_server,
                                                  name=pa_const.START_REST_SERVER_FOR_EXTERNAL_TOPOLOGY)
    rest_server_thread_for_external_topology.start()


if __name__ == '__main__':
    main()
