# OB-CAS Alarm Correlation App

## Functional Description

This application monitors the alarms (and other notifications) originated from devices (ONUs and OLTs), 
and aims to correlates these alarms based on some common properties (elements). 
Some examples of common properties include ONUs belonging to the same channel-termination, 
ONUs from the same vendor, ONUs managed by the same vOMCI function, OLTs connected to the same NT shelf. 
For example, if all ONUs belonging to the same channel-termination raise an alarm, these alarms can 
be correlated to the corresponding channel-termination.

The correlation rules are dynamically built based on the PON topology information. 
This information includes the list of ONUs and OLTs, which ONUs are connected to which OLTs 
through which channel-terminations and PON splitters, which ONUs are managed by which vOMCI functions, 
etc. The topology information, as well as the alarm information is periodically retrieved from 
the OpenSearch database through the OB-CAS SDK.

Before reporting the identified correlations, all the correlations whose correlated devices are 
subset of any other correlations will be suppressed. For example, the correlation corresponding
to a splitter will be suppressed when there is another correlation corresponding to the channel 
termination to which that splitter is connected. 
This way, reported correlations indicate a better view on the root causes of the issues.

When the engine detects an alarm correlation (or detects that an existing correlation disappears) 
it updates the state of the correlations in the OpenSearch database.






The figure below depicts high level how the alarm correlator functions.


<p align="center">
 <img width="600px" height="300px" src="Alarm%20Correlation%20Application%20Arch.png">
</p>

The figure below shows how the Alarm Correlation App integrates within the OB-CAS sandbox showing also the persister application.


<p align="center">
 <img width="600px" height="300px" src="Alarm%20Correlation%20Application.png">
</p>

### Alarm correlation output examples

The following alarm correlation would be persisted in the active alarm index in the OpenSearch when 
all ONUs connecting to the splitter "olt1.ct2.sp1" (consisting of onu1, onu2, ..., onu10) would all
raise the alarm "bbf-xpon-defects:los", which would indicate there might be a fiber cut issue with 
this splitter. Please note that this correlation also shows that some of these ONUs (not all of them) 
are raising the alarm
"bbf-obbaa-ethernet-alarm-types:loss-of-signal", which might not be related to the root cause issue.

#### A Raised Correlation Alarm, correlating ONUs of a splitter which suffers fiber cut

```
{
    "alarmTypeId": "obcas:alarm-correlation",
    "alarmResource": "splitter:olt1.ct2.sp1",
    "alarmStatus": "Raised",
    "correlatedDevices": ["onu1", "onu2", "onu3", "onu4", "onu5", "onu6", "onu7", "onu8", "onu9", "onu10"]
    "commonAlarmTypeIds": [
        "bbf-xpon-def:lobi",
    ],
    "allAlarmTypeIds": [
        "bbf-xpon-def:lobi",
        "bbf-obbaa-ethernet-alarm-types:loss-of-signal"
    ],
    "rootCause": "fiber cut",
    "time": "2024-05-10T09:27:39.433Z"
```
When the correlation above is cleared, it will be removed from the active alarms 
index and the following clear notification will be persisted in the history alarm index.

#### A Raised Correlation Alarm, correlating ONUs of a splitter which suffers fiber cut

```
{
    "alarmTypeId": "obcas:alarm-correlation",
    "alarmResource": "splitter:olt1.ct2.sp1",
    "alarmStatus": "Cleared",
    "time": "2024-05-10T09:27:44.433Z",
    "rootCause": "fiber cut",
    "Raisedtime": "2024-05-10T09:27:39.433Z"
}
```
The following correlation indicates that all ONUs located in the power distribution area "area1" 
are all raising two alarms "bbf-xpon-defects:los" and "obcas-notification-alarm:v-ani-defect", 
which indicates that there might be power cut issue in the whole area1.

#### A Raised Correlation Alarm, correlating ONUs of an area which suffers power cut

```
{
    "alarmTypeId": "obcas:alarm-correlation",
    "alarmResource": "powerDistributionArea:PDA1",
    "alarmStatus": "Raised",
    "correlatedDevices": ["onu1", "onu2", "onu3", "onu4", "onu9", "onu10"]
    "commonAlarmTypeIds": [
        "bbf-xpon-def:lobi"
        "bbf-xpon-def:dgi",
    ],
    "allAlarmTypeIds": [
        "bbf-xpon-def:lobi",
        "bbf-xpon-def:dgi",
        "bbf-obbaa-ethernet-alarm-types:loss-of-signal"
    ],
    "rootCause": "power cut",
    "time": "2024-05-10T09:27:39.433Z"
}
```
The following correlation indicates that all LTs in the cabinet "cabinet1" are all 
raising the alarm "bbf-hw-xcvr-alt:temperature-high", 
which indicates that the temperature of the cabinet 1 is higher than expected.

#### A Raised Correlation Alarm, correlating ONUs of a splitter which suffers high temperature

```
{
    "alarmTypeId": "obcas:alarm-correlation",
    "alarmResource": "cabinet:cabinet1",
    "alarmStatus": "Raised",
    "correlatedDevices": ["olt1", "olt2", "olt3"]
    "commonAlarmTypeIds": [
        "bbf-hw-xcvr-alt:temperature-high",
    ],
    "allAlarmTypeIds": [
        "bbf-hw-xcvr-alt:temperature-high"
    ],
    "rootCause": "power cut",
    "time": "2024-05-10T09:27:39.433Z"
}
```

### Suppressing Correlations
The application suppresses the correlations which overlaps with the other correlations. For example, having three following correlations, the first two ones are suppressed and only the third one is reported, since the third correlation indicates the root cause of the issue, which is olt1 (and not its channel terminations olt1.ct1 and olt1.ct2):

* correlation1, where "correlatedDevices" = ["onu1", "onu2", "onu3"] , and "alarmResource" = "channelTermination:olt1.ct1"
* correlation2, where "correlatedDevices" = ["onu4", "onu5"] , and "alarmResource" = "channelTermination:olt1.ct2"
* correlation3, where "correlatedDevices" = ["onu1", "onu2", "onu3", "onu4", "onu5"] , and "alarmResource" = "olt:olt1"

### Correlation Settings
The application accepts the following advanced settings (see the example JSON below):

* Ignoring specific common elements: There might be some attributes which are not interesting to be correlated, such as devices' serial numbers, their locations, etc. These attributes cab be specified to the application and then the application does not make any correlation based on these attributes.
* Hierarchy of common elements: This is useful when there are two correlation with exactly the same devices correlated ("correlatedDevices" field in the correlation message) but with different common elements ("alarmResource" field in the correlation message). The correlation with the common element in the higher level in the hierarchy will be suppressed. For example, having two following correlations, the first one will be suppressed (and will not be reported), since in the hierarchy the "olt" is placed higher than the "channelTermination":

  * correlation1, where "correlatedDevices" = ["onu1", "onu2", "onu3"] , and "alarmResource" = "olt:olt1"
   *  correlation2, where "correlatedDevices" = ["onu1", "onu2", "onu3"] , and "alarmResource" = "channelTermination:olt1.ct1"
* Root cause of the correlation: It is possible to provide some extra information about the possible root causes of the correlations, their corresponding alarms, and common attributes. This would help to identify the root cause of the correlations and suppress other unrelated correlations.
    For example, having the following correlation, the root cause of this correlation is identified as "Power cut" (and not "Fiber cut"):

    * where "commonAlarmTypeIds" = ["bbf-xpon-def:lobi", "bbf-xpon-def:dgi", "bbf-obbaa-ethernet-alarm-types:loss-of-signal"]

    As another example, having the following correlation, 
the root cause of this correlation is identified as "Fiber cut":

    * where "commonAlarmTypeIds" = ["bbf-xpon-def:lobi", "bbf-obbaa-ethernet-alarm-types:loss-of-signal"]

  As another example, having two following correlations, the first one will be suppressed (and will not be reported). The root cause of both correlations is identified as "Power cut", whose preferred common element is "PDA" (and not "olt").
    * correlation1, where "correlatedDevices" = ["onu1", "onu2", "onu3"] , and "commonAlarmTypeIds" = ["bbf-xpon-def:lobi", "bbf-xpon-def:dgi"] , and "alarmResource" = "olt:olt1"
    * correlation2, where "correlatedDevices" = ["onu1", "onu2", "onu3"] , and "commonAlarmTypeIds" = ["bbf-xpon-def:lobi", "bbf-xpon-def:dgi"] , and "alarmResource" = "powerDistributionArea:PDA1"




#### Correlation Settings Example

```
{
    "commonElementsIgnored": [
        "location"
    ],
    "commonElementsHierarchy": {
        "ponElements": [
            "olt",
            "channelTermination",
            "splitter2",
            "splitter1"
        ]
    },
    "rootCauses": [
        {
            "name": "power cut",
            "alarmTypeIds": [
                "bbf-xpon-def:lobi",
                "bbf-xpon-def:dgi"
            ],
            "preferredCommonElements": [
                   "powerDistributionArea"
            ]
        },
        {
            "name": "fiber cut",
            "alarmTypeIds": [
                "bbf-xpon-def:lobi"
            ],
            "preferredCommonElements": [
                "olt",
                "channelTermination",
                "splitter2",
                "splitter1"
            ]
        }
    ]
}
```

### Further Features
* Label hierarchy: to suppress correlations which have been covered by other correlations in higher levels. For example, dying gasps ONUs of a channel termination can be suppressed by dying gasps ONUs of the OLT (to which the channel termination belongs).
(covered by release 1.0.0)

* Correlation sensitivity: to report the category correlations even if some members of the category are not raising alarms. For example, if 95 percent of the ONUs of a channel termination raise dying gasp alarm, this will be reported.
* Correlating alarms with categories: Each label can be corresponded to a set of alarms, and the correlation will be reported only if the corresponding alarm is raised for the members of that category. For example, to correspond channel-termination label to the dying gasp alarm.


<a id="env" />

## Setting up OB-CAS Alarm Correlation Application
Prior to building docker image for the OB-CAS Alarm Correlation Application, make sure OB-CAS App environment is setup based on the instructions detailed [here](../obcas_app_environment.md)



### Build OB-CAS SDK Docker Image
~~~
	cd obcas/src/obcas_sdk
	make docker-build
~~~

### Build OB-CAS Alarm Correlation App Docker Image
~~~  
    cd obcas/src/obcas_apps/alarm_correlation/
	make docker-build
~~~

### Start OB-CAS Alarm Correlation App using Docker-Compose

- **Pre-Requisites**

  * OB-BAA must be up and running
  
  * Opensearch and opensearch dashboard applications must be up and running ~/obcas/src/obcas_sdk/opensearch_handler/data/docker-compose.yml
  
  * OB-CAS Persister App must be up and running as well  ~/obcas/src/obcas_apps/persister/docker-compose.yaml
  
  * Update the Env variable OPENSEARCH_HOST, BAA_SERVER_IP in ~/obcas/src/obcas_apps/alarm_correlation/docker-compose.yaml
  
  * **Note: Update the correct IP address of OB-BAA, OPENSEARCH containers**


- **Starting OB-CAS Alarm Correlation App**

    * Navigate to the directory **cd obcas/src/obcas_apps/alarm_correlation**
  
    * Execute the command to start docker container **docker-compose up -d**

[<--Back to the Applications Overview](../index.md)

