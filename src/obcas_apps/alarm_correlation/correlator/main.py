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
# Created by Jafar Hamin (Nokia) in April 2024


from topology_handler import *
from alarm_handler import *
from database import get_database
from opensearch_database import OsDatabase
from suppress import SuppressReport
from base_logging.fluentd_logger import FluentdLogger
import os


def main():
    if "fluentd" == os.getenv("LOG_OPT"):
        FluentdLogger().install('alarm_correlation_app')
    get_database(OsDatabase)
    TopologyHandler.periodically_update_topology()
    AlarmHandler.periodically_update_alarms()
    SuppressReport.periodically_report_correlations()


if __name__ == "__main__":
    main()