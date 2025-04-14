export const CORRELATIONS = [
    {
        "alarmTypeId": "obcas:alarm-correlation",
        "alarmResource": "splitter:OLT11.CT_1.SP1",
        "alarmStatus": "Raised",
        "correlatedDevices": ["ont1", "ont2", "ont3", "ont4", "ont5"],    
        "commonAlarmTypeIds": [
            "bbf-xpon-def:lobi",
        ],
        "allAlarmTypeIds": [
            "bbf-xpon-def:lobi",
            "bbf-obbaa-ethernet-alarm-types:loss-of-signal"
        ],
        "time": "2024-05-10T09:27:39.433Z"
    },

    {
        "alarmTypeId": "obcas:alarm-correlation",
        "alarmResource": "powerDistributionArea:PDA4",
        "alarmStatus": "Raised",
        "correlatedDevices": ["ont91", "ont92", "ont93", "ont94", "ont95", "ont96", "ont97", "ont98", "ont99", "ont100"],
        "commonAlarmTypeIds": [
            "bbf-xpon-def:lobi",
            "bbf-xpon-def:dgi"
    
        ],    
        "allAlarmTypeIds": [
            "bbf-xpon-def:lobi",
            "bbf-xpon-def:dgi",
            "bbf-obbaa-ethernet-alarm-types:loss-of-signal"
        ],
        "time": "2024-05-10T09:27:39.433Z"    
    },
    {
        "alarmTypeId": "obcas:alarm-correlation",    
        "alarmResource": "cabinet:cabinet1",    
        "alarmStatus": "Raised",    
        "correlatedDevices": ["OLT11", "OLT12", "OLT13", "OLT14", "OLT15"],    
        "commonAlarmTypeIds": [    
            "bbf-hw-xcvr-alt:temperature-high"    
        ],    
        "allAlarmTypeIds": [    
            "bbf-hw-xcvr-alt:temperature-high"    
        ],    
        "time": "2024-05-10T09:27:39.433Z"    
    },
    {
        "alarmTypeId": "obcas:alarm-correlation",    
        "alarmResource": "cabinet:cabinet2",    
        "alarmStatus": "Raised",    
        "correlatedDevices": ["OLT16", "OLT17", "OLT18", "OLT19", "OLT20"],    
        "commonAlarmTypeIds": [    
            "bbf-hw-xcvr-alt:temperature-high"    
        ],    
        "allAlarmTypeIds": [    
            "bbf-hw-xcvr-alt:temperature-high"    
        ],    
        "time": "2024-05-10T09:27:39.433Z"    
    }
];