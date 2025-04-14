# Applications Overview (OB-CAS release 1.0.0)


A number of sample applications are developed inside the OB-CAS project. 
Those sample applications demonstrate how business logic are wrapped leveraging OB-CAS APIs 
to interact with infra services (Message bus, DBs) and the underlying access controller platform.

## Alarm Correlation App


This application monitors the alarms (and other notifications) originated from devices (ONUs and OLTs), 
and aims to correlate these alarms based on some common properties (elements). 
Some examples of common properties include ONUs belonging to the same channel-termination, 
ONUs from the same vendor, ONUs managed by the same vOMCI function, OLTs connected to the same NT shelf.

Read more about [alarm correlation app](./alarm_correlation/alarm_correlation.md)


## Persistency App


This app perists data in databases, and is used in conjunction with other apps. For instance when deployed together with 
the alarm correlation app, it performs following persistency activities:

* ingest a file containing PON topology info, and persist this info in OpenSearch DB
* receive NC notifications and alarms raised by access controller platform (OB-BAA), and persist these in OpenSearch DB
* retrieve specific volatile information from access controller platform (OB-BAA) and update/persist 
this in OpenSearch DB (e.g. ONU-OLT topology information)

A later version of this app will also be integrated with KAFKA APIs (consumer) as well as able to persist time series data in OpenTSDB

Read more about [persister app](./persister/persister.md)

## Alarm Correlation Visualizer App


This web application allows to show the alarms correlations and the individual alarms in different tables 
with the possibility to select any of them and visualize on a map that contains the whole topology.

Read more about [alarm correlation visualizer app](./alarm_correlation_visualizer/alarm_correlation_visualizer.md)

## BAA Device Manager UI App


The BAA device manager UI App is custom defined specifically to show the devices under control of
the OB-BAA platform, using Streamlit Python Library and Netconf API.

Read more about [baa device manager app](./baa_device_manager/baa_device_manager.md)


# Planned in 2025 (OB-CAS release 2.0.0)


## Threshold Setting App


This app determines periodically on the basis of a ML mode or 
simple means and standard-deviation for a set of historical performance metric data 
the thresholds which, when exceeded, will result in an alarm creation. Historical data is retrieved from OpenTSDB, thresholds are stored in OpenTSDB.



## Metrics Processor App


The metrics processor app raises an alarm (over KAFKA) when
freshly received performance monitoring data (via KAFKA) are outside the 
ranges calculated by the threshold setting app.




<--[APIs ](../sdk/apis/index.md)

--> [PON Simulator ](../sdk/pon_simulator/index.md)