# Demonstrations: alarm correlation 

## End-to-end set-up for alarm correlation demo


The following steps describe how to do the end-to-end setup to demo the alarm correlation application:


* Checkout the obcas code repository. docker-compose file is located in path ~/obcas/resources/examples/e2e_compose_data/obcas_end2end_docker_compose.yaml
* Update the public IP of BAA server & opensearch host for the obcas-persister-app & alarm corelation app in ~/obcas/resources/examples/e2e_compose_data/obcas_apps.yaml
* Build fluentd image using command 
  * Navigate to directory ~/obcas/src/obcas_sdk/base_logging/data/
  * Run command make docker-build this would build the fluentd image required for the obcas setup.
* Start the containers using command: docker-compose -f ~/obcas/resources/examples/e2e_compose_data/obcas_end2end_docker_compose.yaml up -d  
  * This will start OB-BAA and open search containers;  wait for all the containers to start properly
* Start OBCAS apps using command: docker-compose -f ~/obcas/resources/examples/e2e_compose_data/obcas_apps.yaml up -d
  * This will start all the required containers required for running the alarm correlation app
* Install the BBF-OLT-simulator-2.2.kar file from /obcas/resources/examples/polt-simulator-adapter/ by running the RPC request /obcas/resources/examples/common-requests/deploy-polt-simulator-VDA.xml
* Connect the ONU simulator and pOLT simulator using the REST request attached here
  * Request to be used: RX_Mode_OLT1_onuSim1 
    * Please adjust the IP address of the postman collection to actual pOLT simulator IP. 
    * Applicable only for vOMCI-based ONUs
* Configure OLT and ONT by using the sample configurations present in Browse OBBAA / obbaa - BBF Code (broadband-forum.org) 
  * Before configuring the 3-grpc-settings-olt.xml
    * Please update the public IP address of the machine where the obbaa-vproxy is running under the grpc-transport-parameters. 
      * Applicable only for vOMCI-based ONUs
  * Follow the same order while configuring the devices
    * Applicable only for vOMCI-based ONUs
* Now that while configuring the device, obcas-persister app will start adding the topology for the corresponding device as and when the device is added to OB-BAA.
  * To Raise different types of alarms, use the python script present in /obcas/test/Demo.py script. and provide options stated in the script.
    * Before running the script, please make the following changes:
      * Change host details in topology.json file. Update the IP address of the host where simulator is running.
      * Update OPENSEARCH_HOST IP in GetTopology.py. Update the IP address of the host where opensearch is running.
    * Run the script pyhton3 Demo.py
      * Script will generate/clear the given alarms/notifications per the selected scenario


## Integration tests

Prior to run the demo script, one should proceed with performing first some integration tests as described [here](./integration_tests/integration_tests.md)


## Demo script run

For more information on the scripts written to demo the alarm correlation app, please see [here](./demo_scripts/demo_scripts.md) 

When running the demo script, one can make a choice between the following simulations:


```
  madshett@host-100-120-11-168:~/obcas/test$ python3 Demo.py
      Fiber Cut
      F_R: Raise a Fiber Cut
      F_C: Clear a Fiber Cut
      Power Cut
      P_R: Raise a Power Cut
      P_C: Clear a Power Cut
      High Temperature
      T_R: Raise a High Temperature
      T_C: Clear a High Temperature
      Random Test
      R_R: Raise a Random Test
      R_C: Clear a Random Test


Insert the list of simulation, for example, type {FIBERCUT_LETTER}_{RAISE_LETTER} to simulate fiber cut alarms.
Simulate []:

```

## Testing without script

### Simulating alarms
To raise/clear alarm on ONU, one can connect to onu-simulator 
(docker attach onu-simulator) and send the following commands 
(this would raise eth-loss alarm on a particular ONU, and we could see that alarm is being persisted in OpenSearch as soon as it is raised.)

* alarm 11 1 80000000000000000000000000000000000000000000000000000000 1 --> raise
* alarm 11 1 00000000000000000000000000000000000000000000000000000000 2 --> clear

### ONU defect notifications

One can generate any notification with an identity derived from items-detected-at-olt-for-v-ani with below commands.
* Note: Change the "state" to "raised" to raise the alarm.

```

ONU Defect Notifications Collapse source
DGI
POST http://<simulator_ip>:3001/polt/polt_actions
Body:
{
"requests":
[
{
"v-ani": "vAni_ont1",
"action": "ONUALARM",
"type": "bbf-xpon-defects:dgi",
"state": "cleared"
}
]
}

LOBI
POST http://<simulator_ip>:3001/polt/polt_actions
Body:
{
"requests":
[
{
"v-ani": "vAni_ont1",
"action": "ONUALARM",
"type": "bbf-xpon-defects:lobi",
"state": "cleared"
}
]
}


```


[<--Back to the PON simulator](../../sdk/pon_simulator/index.md)

[<<--Introduction](../../index.md)