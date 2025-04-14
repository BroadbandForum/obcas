# Script for Alarm Correlation Demo

## Input

The script takes in the topology information from the open search DB, which gives for each ONU i

* the OLT ID (==channel termination)
* the cabinet-ID associated with the OLT
* the splitter i2 (stage 2, closest to the ONUi) -- splitter i1  (stage 1, closest to the OLT)
* the power distribution area
* information such as vani id, ani id and ct are added by the persistency app as the ONUs are detected by the OLT and OB BAA

## Dimensioning

To limit the required K8s resources , but to yet still provide a realistic or convincing demo, we have the following quantities

* 10 x OLTs
* 10 x ONUs per OLT
* per OLT: 1  x stage-1  (1:8) splitters and 4 x stage-2  (1:8) splitters , total of 10 x 5 =50 splitters  (some stage-2 splitters will have no ONUs attached!)
* 3 x power distribution areas
  * ONUs of OLT-1 through OLT-3  are assigned to PDA 1 
  * ONUs of OLT-4 through OLT-7 are assigned to PDA 2 
  * ONUs of OLT-8 through OLT-10 are assigned to PDA 3
* 2 x cabinets 
  * OLT-1 through OLT-5  are hosted in cabinet 1 
  * OLT-6 through OLT-10  are hosted in cabinet 2


## Script scenarios

### Fiber cut /raise simulation script (F_R)
* first a fiber cut-impacted area is chosen by selecting one, two or three stage 1-splitters , and then all stage-2 splitters associated with these stage-1 splitters 
  * with every run, a different fiber cut-impacted area is randomly selected 
  * NC Notif  API on associated POLT sim (OLT-IDs) and for all connected ONTs (v-ani's) is triggered (state=raised) for LOBi for all ONUs connected via the selected stage 1/stage 2  splitters:

~~~ 
<notification xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0">

<if:interfaces-state xmlns:if="urn:ietf:params:xml:ns:yang:ietf-interfaces">

    <if:interface>

      <if:name>van1</if:name>

      <bbf-xponvani:v-ani xmlns:bbf-xponvani="urn:bbf:yang:bbf-xponvani">

        <bbf-xponvani:defect-state-change>

          <bbf-xponvani:defect>

            <bbf-xponvani:type>bbf-xpon-def:lobi</bbf-xponvani:type>

            <bbf-xponvani:state>raised</bbf-xponvani:state>

            <bbf-xponvani:last-change>2024-01-01T00:00:00Z</bbf-xponvani:last-change>

          </bbf-xponvani:defect>

        </bbf-xponvani:defect-state-change>

      </bbf-xponvani:v-ani>

    </if:interface>

</if:interfaces-state>

</notification>
~~~ 




### Fiber cut /clear simulation script (F_C)

*  NC Notif  API on associated POLT sim (OLT-IDs) and for all connected ONTs (v-ani's) is triggered with  (state=cleared) for LOBi


### Power cut /raise simulation script (P_R)
* first a power distribution area is randomly chosen 
* for all ONUs belonging to the selected power distribution area
  * NC Notif  API on associated POLT sim (OLT-IDs)  and for all defined v-ani's on that pOLT are  triggered (state=raised) twice and consecutively : first with DGI and then with LOBi


### Power cut /clear simulation script (P_C)
* for all ONUs belonging to the previously selected power distr. area:
  * NC Notif API on associated POLT sim (OLT-IDs)  and for all defined v-ani's on that pOLT are  triggered (state=cleared) twice and consecutively : first with DGI and then with LOBi


    
### OLT cabinet (temperature) /raise  and / clear simulation scripts (T_R / T-C)
* randomly select an OLT cabinet 
  * IETF (temperature) alarm API on associated POLT sim (OLT-IDs) are raised or cleared



### Random NC Notif / raise and / clear simulation scripts (R_R / R_C)
* randomly select 5 ONUs 
  * for each ONU randomly select fiber cut trigger (raise/clear) or power cut trigger (raise/clear)
  * in general no correlation will be detected by the alarm correlation app
    * unless - by co-incidence-  the script triggered a fiber cut NC Notif  for all ONUs connected to the same splitter (stage 1 or stage 2).



    

## Demonstration

For the demo we can run sequentially different scripts, with at minimum 2 x P seconds in between, 
where P = the periodicity through which the correlation app check in open search for new alarms/notifications  (P == e.g.  10 seconds)

* Example:   F_R / F_C / R_R / R_C / P_R / P_C     ... and we show respectively a fiber cut , a random alarm  and a
power cut simulation, where at the end all ONUs/OLTs are back in normal (healthy) operational mode




## Visualization

* The PON topology is projected on a map
  * lat/long for OLT/ONU/splitters are populated in separate document

* Alarm correlation result is visualized by coloring the impacted ONUs and the root cause (splitter, power-cut, cabinet), using a different color for each root cause


See the [alarm correlation visualizer app](../../../apps/alarm_correlation_visualizer/alarm_correlation_visualizer.md) for more info







[<--Back to the Demonstrations](../index.md)

