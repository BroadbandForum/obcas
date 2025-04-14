# Integration tests

The purpose of these tests is to integrate all the necessary components, run some test scenarios, and verify that the expected results are observed.

## Components
The necessary components can be deployed through the following docker-compose files:

* PON_simulator_docker_compose.yaml: Running OLT/ONU simulators, as well as, the PON simulator
* OBBAA_docker_compose.yaml: Running the OB-BAA
* infra_docker_compose.yaml: Running the infrastructure components, including OpenSearch and Kafka
* persister_app_docker_compose.yaml: Running the persister application, having the OBCAS SDK as its base image
* alarm_correlation_app_docker_compose.yaml: Running the alarm correlation application, having the OBCAS SDK as its base image

## Test Scenarios
* Start a number of devices (ONU and OLT simulators) through PON simulator
* Create and configure devices in OB-BAA
* Verify PON (OLTs/ONUs) topology is persisted in OpenSearch through the persister application
* Extra PON topology  information is also added into open search, for example ONTs associated with which splitter(s), etc..   
* Ask PON simulator to make devices raise alarms
* Verify alarms are persisted in OpenSearch through the persister application
* Verify alarms are correlated and persisted in the OpenSearch through the alarm correlation application
* Verify alarm correlation notifications are produced on Kafka through the alarm correlation application
* Ask PON simulator to make devices clear some of the previously raised alarms
* Verify the cleared alarms are removed from active alarms and persisted in history alarms
* Verify correlations for the cleared alarms are cleared. The cleared correlations should be removed from active correlations and be persisted in history correlations
* Ask PON simulator to start new devices and raise some alarms for these devices
* Remove some existing devices in OB-BAA and create and configure new devices in OB-BAA
* Verify new PON topology and new alarms are persisted in OpenSearch
* Verify alarm correlations are updated based on the new PON topology and new alarms


[<--Back to the Demonstrations](../index.md)