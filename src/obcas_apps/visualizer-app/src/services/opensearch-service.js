import { useConfig } from "@condor/utils";
import { ALARMS } from "../model/alarms.js"
import { CORRELATIONS } from "../model/correlations.js"


export const GetActiveAlarms = async (url) => {
   
   const authHeader = GetAuthHeaderValue();
   const config = useConfig();

   if(config.REACT_APP_DUMMY_DATA==='true'){ 
      return ALARMS;

   }else{
      let response = await fetch(url, {
       method: 'POST',
       headers: {
          'Authorization': authHeader,
          'Content-Type': 'application/json; charset=UTF-8',
          'Accept': "*/*",
       },
       body: JSON.stringify({size: 1000})
    });

    var data = await response.json();
    var activeAlarms = [];
    data?.hits?.hits?.forEach(hit => {
      if(hit._source){         
         var alarmType = hit._source.alarmTypeId;
         if(alarmType!=='obcas:alarm-correlation'){            
            activeAlarms.push(hit._source);
         }
      }
   });
    return activeAlarms;
   }
  };

 export const GetActiveCorrelatedAlarms = async (url) => {

   const config = useConfig();
   if(config.REACT_APP_DUMMY_DATA==='true'){
     
      return CORRELATIONS;
      
   }else{
   const authHeader = GetAuthHeaderValue();

    let response = await fetch(url, {
       method: 'POST',
       headers: {
          'Authorization': authHeader,
          'Content-Type': 'application/json; charset=UTF-8',
          'Accept': "*/*",
       },
       body: JSON.stringify({size: 1000})
    });

    var data = await response.json();
    var activeAlarms = [];
    data?.hits?.hits?.forEach(hit => {
      if(hit._source){         
         var alarmType = hit._source.alarmTypeId;
         if(alarmType==='obcas:alarm-correlation'){            
            activeAlarms.push(hit._source);
         }
      }
   });
    return activeAlarms;
   }
  };  

  export const GetOntTopolgy = async (url) => {
   const authHeader = GetAuthHeaderValue();

    let response = await fetch(url, {
       method: 'POST',
       headers: {
          'Authorization': authHeader,
          'Content-Type': 'application/json; charset=UTF-8',
          'Accept': "*/*",
       },
       body: JSON.stringify({size: 1000})
    });

    var data = await response.json();
    var onts = [];
    data?.hits?.hits?.forEach(hit => {
      if(hit._source){         
         onts.push(hit._source);
      }
   });
    return onts;
  };  

  export const GetOltTopolgy = async (url) => {
   const authHeader = GetAuthHeaderValue();

    let response = await fetch(url, {
       method: 'POST',
       headers: {
          'Authorization': authHeader,
          'Content-Type': 'application/json; charset=UTF-8',
          'Accept': "*/*",
       },
       body: JSON.stringify({size: 1000})
    });

    var data = await response.json();
    var olts = [];
    data?.hits?.hits?.forEach(hit => {
      if(hit._source){         
         olts.push(hit._source);
      }
   });
    return olts;
  };  

function GetAuthHeaderValue(){
   const config = useConfig();
   const username = config.REACT_APP_OPENSEARCH_USER;
   const password = config.REACT_APP_OPENSEARCH_PASSWORD;
   const authHeader = 'Basic '+window.btoa(username+':'+password);
   return authHeader;
}
