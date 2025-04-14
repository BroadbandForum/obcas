import { useConfig } from "@condor/utils";
import { linesToDraw } from "../model/mapLines.js";
import circlesToDraw from "../model/mapCircles.js";
import {
    oltIcon,
    ontIcon,
    splitterIcon
} from "../components/maps/icons.js";
import { GetOltTopolgy, GetOntTopolgy } from "./opensearch-service.js";

//Guardo los elementos que deberan dibujarse como markers y como circles
const elementTypes = {
    markers: ['OLT', 'SPLITTER', 'ONU'],
    circles: ['PDA', 'CABINET']
};


export const GetLinesToDrawFromElements = (elements) => {
    const config = useConfig();

    var lines = [];

    elements.forEach(element => {
        const connectedDevice = elements.find(
          el => el.device === element.connectedTo
        );
              
        if (connectedDevice) {
          var newLine;

          newLine=[
            [element.lat, element.lon],
            [connectedDevice.lat, connectedDevice.lon],
          ];

          lines.push(newLine);
        }
      });

    return lines;
}

//Recibe los elementos que deberán dibujarse como círculos
export const GetCirclesToDrawFromElements = (elements) => {
    const config = useConfig();

    const pdaColor = config.REACT_APP_PDA_DEFAULT_COLOR;
    const cabinetColor = config.REACT_APP_CABINET_DEFAULT_COLOR;    
  
    //Array de arrays de arrays para las lineas del mapa
    var circles = [];

    //Recorro los elementos para ir generando el array de lineas
    elements.forEach((element) => {
        
        if (elementTypes.circles.includes(element.elementType)) {

            var circleColor;
            if(element.elementType==='PDA'){
                circleColor=pdaColor;
            }else if(element.elementType==='CABINET'){
                circleColor=cabinetColor;
            }
            
            circles.push({
                id: element.device,
                latLng: [element.lat, element.lon],
                radius: element.radio,
                color: circleColor,
                show: true,
                hasAlarm: false,
                additional_data: {
                    elementType: element.elementType,
                    id: element.device,
                }
            });
        }
    });
    return circles;
}

export const GetMarkersToDrawFromElements = (elements) => {
    const config = useConfig();

    //Color default para los markers del mapa
    const defaultColor = config.REACT_APP_MARKER_DEFAULT_COLOR;

    const onts = GetOntTopolgy(config.REACT_APP_ONU_TOPOLOGY_INDEX);
    const olts = GetOltTopolgy(config.REACT_APP_OLT_TOPOLOGY_INDEX);

    

    //Iconos para los markers
    const icons = {
        OLT: oltIcon,
        ONU: ontIcon,
        SPLITTER: splitterIcon
    };

    var markers = [];
    elements.forEach((cto) => {
        if (elementTypes.markers.includes(cto.elementType)) {
            markers.push({
                id: cto.device,
                latLng: [cto.lat, cto.lon],
                radius: cto.radio,
                icon: icons[cto.elementType](defaultColor),
                color: defaultColor,
                hasSingleAlarm: false,
                hasCorrelativeAlarm: false,
                show: true,
                hasAlarm: false,
                additional_data: {
                    elementType: cto.elementType,
                    device: cto.device,
                }
            });
        }
    });

    return markers;
}

export default GetLinesToDrawFromElements;