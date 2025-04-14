# OB-CAS Persister 

## Functional Description

This application is responsible to persist PON information including PON topology 
(OLTs, ONUs, channel terminations, etc.), alarms, and other notifications in the OpenSearch database, 
and keep this up to date.

The figure below shows how the Persister App  is integrated within the OB-CAS sandbox comprising 
the OB-BAA core.


<p align="center">
 <img width="600px" height="300px" src="Persister%20Application%20System%20Integration.png">
</p>



### Controller-provided PON Topology
The persister application subscribes to the configuration-change notifications in the OB-BAA, and it 
updates the PON topology indexes in the OpenSearch whenever it receives a configuration-change notification. 
Additionally, the application can occasionally send NETCONF GET requests toward OB-BAA to retrieve 
the existing devices and updates the topology indexes in the OpenSearch. This would be beneficial when 
the application misses some notifications, 
for example because of failures. Some examples of ONU and OLT documents are shown below:

#### An ONU document in the onus index

```
{
"deviceRefId": "onu1",
"serialNumber": "ABCD12345678",
"aniRefId": "an1",

    "olt": "olt1",
    "channelTermination": "olt1.ct1",
    "splitter1": "olt1.ct1.sp.sp1",
    "splitter2": "olt1.ct1.sp",
    "vendor": "alcl",
    "vomci": "vomci1",
    "powerDistributionArea": "area1"
}

```

#### An OLT document in the olts index

```
{
    "deviceRefId": "olt1",
    "cabinet": "server_room_1"
    "vendor": "bbf"
}
```
Some part of this information can be retrieved from the notifications coming from OB-BAA. For example, 
the information about the channelTermination through which an ONU is connect to an OLT can be retrieved from 
the "onu-presence-state-change" notification which is raised when ONU is ranged in the OLT.

### External PON Topology
Some other part of PON information cannot be retrieved from OB-BAA, but needs to be inserted 
explicitly by the operators. For example, the splitter through which an ONU is connected to the 
PON should be explicitly inserted into the document by the operator. 
Another example of such information is the location of devices.

There should be a REST API in the PON persistor application, namely "/external_pon_topology", 
that accepts external PON topology information and inserts this information in the
appropriate PON topology indexes in OpenSearch. An example of external PON topology and its 
graphical representation are shown below:

#### External PON topology example

```
{
    "onu": [
        {
            "deviceRefId": "onu1",
            "splitter1": "olt1.ct1.sp.sp1",
            "splitter2": "olt1.ct1.sp",
            "location": "building1",
            "powerDistributionArea": "area1"
        },
        {
            "deviceRefId": "onu2",
            "splitter1": "olt1.ct1.sp.sp1",
            "splitter2": "olt1.ct1.sp",
            "location": "building2",
            "powerDistributionArea": "area1"
        },
        {
            "deviceRefId": "onu3",
            "splitter1": "olt1.ct1.sp.sp2",
            "splitter2": "olt1.ct1.sp",
            "location": "building3",
            "powerDistributionArea": "area1"
        },
        {
            "deviceRefId": "onu4",
            "splitter1": "olt1.ct1.sp.sp3",
            "splitter2": "olt1.ct1.sp",
            "location": "building3",
            "powerDistributionArea": "area2"
        },
        {
            "deviceRefId": "onu5",
            "splitter1": "olt1.ct2.sp.sp1",
            "splitter2": "olt1.ct1.sp",
            "location": "building4",
            "powerDistributionArea": "area2"
        }     ],
    "olt": [
        {
            "deviceRefId": "olt1",
            "cabinet": "room1",
            "powerDistributionArea": "area3"
        },
        {
            "deviceRefId": "olt2",
            "cabinet": "room1",
            "powerDistributionArea": "area3"
        }
    ]
}
```

<p align="center">
 <img width="600px" height="300px" src="external topology.png">
</p>

### Alarms

The persister application subscribes to the alarms notifications in the OB-BAA, and it 
updates the alarm indexes in the OpenSearch whenever it receives an alarm notification. 
Additionally, the application can occasionally send NETCONF GET requests toward OB-BAA 
to retrieve the existing alarms and updates the alarm indexes in the OpenSearch. 
This would be beneficial when the application misses some notifications, for example because of failures.

When an alarm is raised the persister application stores it in the active_alarms index. 
Later, when the alarm is cleared the alarm will be moved into the history_alarms index. 
Some examples of alarms documents are shown below:

#### An alarm document in active_alarms index

```
{
     "alarmResource": "baa-network-manager:network-manager/baa-network-manager:managed-devices/baa-network-manager:device[baa-network-manager:name='ont1']/baa-network-manager:root/if:interfaces/if:interface[if:name='enet_uni_ont1_1_1']",
     "alarmTypeId": "bbf-baa-ethalt:loss-of-signal",
     "alarmTypeQualifier": null,
     "perceivedSeverity": "major",
     "alarmText": "Loss of signal detected",
     "alarmStatus": "Raised",
     "raisedTime": "2024-05-27T06:17:08.000Z",
     "deviceRefId": "ont1"
 }
```
#### An alarm document in history_alarms index

```
{
     "alarmResource": "baa-network-manager:network-manager/baa-network-manager:managed-devices/baa-network-manager:device[baa-network-manager:name='ont1']/baa-network-manager:root/if:interfaces/if:interface[if:name='enet_uni_ont1_1_1']",
     "alarmTypeId": "bbf-baa-ethalt:loss-of-signal",
     "alarmTypeQualifier": null,
     "perceivedSeverity": "cleared",
     "alarmText": "Loss of signal cleared",
     "alarmStatus": "Cleared",
     "clearedTime": "2024-05-27T06:21:56.000Z",
     "deviceRefId": "ont1",
     "raisedTime": "2024-05-27T06:17:08.000Z"
 }
 ```

### Other notifications
Persistor application also subscribes to the other notifications coming from OB-BAA. 
The application needs to categorize these notifications into two category: 1) active (undesired state) 
notifications, the ones that need attention, for example an onu-presence-state-change notification that 
reports onu-not-present, and 2) history (desired state) notifications, the ones that do not need 
attention, for example an onu-presence-state-change notification that reports 
onu-present-and-on-intended-channel-termination. Accordingly, 
there are two indexes for storing the notifications: active_notifications and history_notifications.

#### A defect-state-change (undesired state) notification received by the persister application
```
<notification xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0">
  <if:interfaces-state xmlns:if="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <if:interface>
      <if:name>van1</if:name>
      <bbf-xponvani:v-ani xmlns:bbf-xponvani="urn:bbf:yang:bbf-xponvani">
        <bbf-xponvani:defect-state-change>
          <bbf-xponvani:defect>
            <bbf-xponvani:type>bbf-xpon-def:dgi</bbf-xponvani:type>
            <bbf-xponvani:state>raised</bbf-xponvani:state>
            <bbf-xponvani:last-change>2024-02-01T02:02:00Z</bbf-xponvani:last-change>
          </bbf-xponvani:defect>
        </bbf-xponvani:defect-state-change>
      </bbf-xponvani:v-ani>
    </if:interface>
  </if:interfaces-state>
</notification>
```

#### A (defect-state change) notification document in the active_notifications index
```
{
     "vAniRefId": "van1",
     "deviceRefId": "ont1",
     "alarmTypeId": "obcas-notification-alarm:v-ani-defect",
     "alarmResource": "baa-network-manager:network-manager/baa-network-manager:managed-devices/baa-network-manager:device[baa-network-manager:name='olt1']/baa-network-manager:root/if:interfaces-state/if:interface[if:name='van1']",
     "time": "2024-01-01T00:00:00Z"
}
 
##Implemented format:
 
{
          "vAniRefId": "ontAni_ont1",
          "alarmTypeId": "obcas-notification-alarm:v-ani-defect",
          "alarmStatus": "raised",         
          "deviceRefId": "ont1",
          "alarmResource": "baa-network-manager:network-manager/baa-network-manager:managed-devices/baa-network-manager:device[baa-network-manager:name='OLT1']/baa-network-manager:root/if:interfaces-state/if:interface[if:name='ontAni_ont1']",
          "raisedTime": "2024-02-01T02:02:00Z"
        }
```
#### A defect-state-change (desired state) notification received by the persister application
```
<notification xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0">
  <if:interfaces-state xmlns:if="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <if:interface>
      <if:name>van1</if:name>
      <bbf-xponvani:v-ani xmlns:bbf-xponvani="urn:bbf:yang:bbf-xponvani">
        <bbf-xponvani:defect-state-change>
          <bbf-xponvani:defect>
            <bbf-xponvani:type>bbf-xpon-def:dgi</bbf-xponvani:type>
            <bbf-xponvani:state>cleared</bbf-xponvani:state>
            <bbf-xponvani:last-change>2024-02-01T03:02:00Z</bbf-xponvani:last-change>
          </bbf-xponvani:defect>
        </bbf-xponvani:defect-state-change>
      </bbf-xponvani:v-ani>
    </if:interface>
  </if:interfaces-state>
</notification>

```
#### A (defect-state change) notification document in the history_notifications index
```
{
     "vAniRefId": "van1",
     "deviceRefId": "ont1",
     "alarmTypeId": "obcas-notification-alarm:v-ani-defect",
     "alarmResource": "baa-network-manager:network-manager/baa-network-manager:managed-devices/baa-network-manager:device[baa-network-manager:name='olt']/baa-network-manager:root/if:interfaces-state/if:interface[if:name='van1']",
     "time": "2024-01-01T00:00:00Z",
     "clearedTime": "2024-01-01T00:00:33Z"
}
 
## Implemented format
 
{
          "vAniRefId": "ontAni_ont1",
          "alarmTypeId": "obcas-notification-alarm:v-ani-defect",
          "alarmStatus": "cleared",
          "clearedTime": "2024-02-01T03:02:00Z",
          "deviceRefId": "ont1",
          "alarmResource": "baa-network-manager:network-manager/baa-network-manager:managed-devices/baa-network-manager:device[baa-network-manager:name='OLT1']/baa-network-manager:root/if:interfaces-state/if:interface[if:name='ontAni_ont1']",
          "raisedTime": "2024-02-01T02:02:00Z"
        }
```


<a id="env" />

## Setting up OB-CAS Persister Application

Prior to building docker image for the OB-CAS Persister Application, make sure OB-CAS App environment is setup based on the instructions detailed [here](../obcas_app_environment.md)


### Build OB-CAS SDK Docker Image
~~~
	cd obcas/src/obcas_sdk
	make docker-build
~~~

### Build OB-CAS Persister App Docker Image
~~~  
    cd obcas/src/obcas_apps/persister_app/
	make docker-build
~~~

### Start OB-CAS Persister App using Docker-Compose

- **Pre-Requisites**

     * OB-BAA must be up and running
  
     * Opensearch and opensearch dashboard applications must be up and running ~/obcas/src/obcas_sdk/opensearch_handler/data/docker-compose.yml
  
     * Update the Env variable OPENSEARCH_HOST, BAA_SERVER_IP in ~/obcas/src/obcas_apps/persister_app/docker-compose.yaml
     
     * **Note: Update the correct IP address of OB-BAA, OPENSEARCH containers**


- **Starting OB-CAS Persister App**
    * Navigate to the directory **cd obcas/src/obcas_apps/persister_app**
    * Start docker container by running command **docker-compose up -d**
    * **Note: As soon as the container is started, it will subscribe to ALARM stream. Whenever an alarm is received Persister app parses the alarm and push it to opensearch DB.**


[<--Back to the Applications Overview](../index.md)