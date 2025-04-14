import {
  Accordion,
  AccordionDetails,
  Alert,
  Box,
  Card,
  CardContent,
  CardHeader,
  Checkbox,
  Collapse,
  Divider,
  Fab,
  FormControl,
  FormControlLabel,
  FormGroup,
  IconButton,
  LinearProgress,
  Paper,
  Stack,
  Typography,
  Zoom,
  useMediaQuery,
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import { useEffect, useRef, useState } from "react";
import Layout from "../components/Layout.jsx";
import { FormattedMessage } from "react-intl";
import AlarmsTable from "../components/AlarmsTable.jsx";
import CorrelationsTable from "../components/CorrelationsTable.jsx";
import CorrelationsMap from "../components/CorrelationsMap.jsx";
import { readRemoteFile } from "react-papaparse";
import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";
import ArrowUpwardIcon from "@mui/icons-material/ArrowUpward";
import AccordionSummary from "@mui/material/AccordionSummary";
import { oltIcon, ontIcon, splitterIcon } from "../components/maps/icons.js";
import { linesToDraw } from "../model/mapLines.js";
import executePost from "../services/opensearch-service.js";
import { useConfig } from "@condor/utils";
import {
  GetLinesToDrawFromElements,
  GetCirclesToDrawFromElements,
  GetMarkersToDrawFromElements,
} from "../services/mapUtils.js";
import MapIcon from "@mui/icons-material/Map";
import condorLogoGrey from "../assets/logo_condor_gray.png";

const Alarms = () => {
  //Hook para leer las configuraciones del archivo env
  const config = useConfig();

  //Mostrar el boton para volver al mapa cuando se va de pantalla
  const [showMapFab, setShowMapFab] = useState(false);
  const mapRef = useRef(null);
  const mapAccordionRef = useRef(null);

  window.onscroll = () => {
    if (
      document.documentElement.scrollTop >
      mapRef.current.clientTop + mapRef.current.clientHeight
    ) {
      setShowMapFab(true);
    } else {
      setShowMapFab(false);
    }
  };

  const containerRef = useRef(null);
  const [locationInfo, setLocationInfo] = useState();
  const [expanded, setExpanded] = useState(true);
  const [topologyExpanded, setTopologyExpanded] = useState(true);

  const handleTopologyExpansion = () => {
    setTopologyExpanded((prevExpanded) => !prevExpanded);
  };

  const handleExpansion = () => {
    setExpanded((prevExpanded) => !prevExpanded);
  };

  //Colores usados para identificar las alarm correlations con los markers del mapa
  const powerareaCutColor = config.REACT_APP_PDA_ALARM_COLOR;
  const fiberCutColor = config.REACT_APP_FIBERCUT_ALARM_COLOR;
  const temperatureColor = config.REACT_APP_TEMPERATURE_ALARM_COLOR;
  const unknownColor = config.REACT_APP_UNKNOWN_ALARM_COLOR;

  const singleAlarmColor = config.REACT_APP_SINGLE_ALARM_COLOR;

  //Color default para los markers del mapa
  const defaultColor = config.REACT_APP_MARKER_DEFAULT_COLOR;

  //Iconos para los markers
  const icons = {
    OLT: oltIcon,
    ONU: ontIcon,
    SPLITTER: splitterIcon,
  };

  //URL donde ir a buscar las coordenadas de todos los elementos
  const LOCATION_DATA_URL = config.REACT_APP_LOCATION_DATA_URL;

  //Voy a buscar los datos de coordenadas de los elementos a la
  //url LOCATION_DATA_URL configurada
  const getLocationData = () => {
    return new Promise((resolve, reject) => {
      readRemoteFile(LOCATION_DATA_URL, {
        header: true,
        download: true,
        complete: (results) => resolve(results.data),
        error: (error) => {
          reject(error);
        },
      });
    });
  };

  function drawTopology() {
    getLocationData()
      .then((result) => {
        setLocationInfo(result);
        setSites(GetMarkersToDrawFromElements(result));
        setCircles(GetCirclesToDrawFromElements(result));
        setLines(GetLinesToDrawFromElements(result));
      })
      .catch((error) => {
        console.log(error);
      })
      .finally(() => {});
  }

  function handleCheckboxChange(event) {
    if ("lines" === event.target.id) {
      showLines(event.target.checked);
    }
    if ("splitter" === event.target.id) {
      showMarkers(event.target.checked, "SPLITTER");
    }
    if ("ONU" === event.target.id) {
      showMarkers(event.target.checked, "ONU");
    }
    if ("OLT" === event.target.id) {
      showMarkers(event.target.checked, "OLT");
    }
    if ("PDA" === event.target.id) {
      showPDAs(event.target.checked);
    }
    if ("cabinet" === event.target.id) {
      showCabinets(event.target.checked);
    }
  }

  function showLines(show) {
    if (show) {
      setLines(GetLinesToDrawFromElements(locationInfo));
    } else {
      setLines([]);
    }
  }

  function showMarkers(show, elementType) {
    //Recorro todos los markers para cambiar el color del que corresponda
    //y volver a default color los demas
    setSites((prevState) => {
      var newSites = [];
      prevState.map((prevDevice) => {
        if (prevDevice.additional_data.elementType.includes(elementType)) {
          prevDevice.show = show;
        }
        newSites.push(prevDevice);
      });

      return newSites;
    });
  }

  function showPDAs(show) {
    setCircles((prevState) => {
      var newCircles = [];
      prevState.map((prevCircle) => {
        if (prevCircle.additional_data.elementType.includes("PDA")) {
          prevCircle.show = show;
        }
        newCircles.push(prevCircle);
      });

      return newCircles;
    });
  }

  function showCabinets(show) {
    setCircles((prevState) => {
      var newCircles = [];
      prevState.map((prevCircle) => {
        if (prevCircle.additional_data.elementType.includes("CABINET")) {
          prevCircle.show = show;
        }
        newCircles.push(prevCircle);
      });

      return newCircles;
    });
  }

  //Esta funcion permite pintar una sola alarma seleccionada de la tabla
  //de alarmas y marcarla volviendo los demas elementos al color default
  function showSingleAlarmInMap(alarmData, disable) {
    setFlyToOtherPlace(false);
    //Recorro todos los markers para cambiar el color del que corresponda
    //y volver a default color los demas
    setSites((prevState) => {
      var newSites = [];
      prevState.map((prevDevice) => {

        if(!disable){
          if (
            prevDevice.id === alarmData?.deviceRefId &&
            !prevDevice.hasCorrelativeAlarm &&
            !prevDevice.hasSingleAlarm
          ) {
            prevDevice.icon =
              icons[prevDevice.additional_data.elementType](singleAlarmColor);
            prevDevice.color = singleAlarmColor;
            prevDevice.hasSingleAlarm = true;
          } else if (
            prevDevice.id === alarmData?.deviceRefId &&
            prevDevice.hasCorrelativeAlarm
          ) {
            prevDevice.hasSingleAlarm = true;
          } else if (
            !prevDevice.hasCorrelativeAlarm &&
            !prevDevice.hasSingleAlarm
          ) {
            prevDevice.icon =
              icons[prevDevice.additional_data.elementType](defaultColor);
            prevDevice.color = defaultColor;
            prevDevice.hasSingleAlarm = false;
          }
        }else{
          if (
            prevDevice.id === alarmData?.deviceRefId &&
            !prevDevice.hasCorrelativeAlarm
          ) {
            prevDevice.icon =
              icons[prevDevice.additional_data.elementType](defaultColor);
            prevDevice.color = defaultColor;
            prevDevice.hasSingleAlarm = false;
          } else if (
            prevDevice.id === alarmData?.deviceRefId &&
            prevDevice.hasCorrelativeAlarm
          ) {
            prevDevice.hasSingleAlarm = false;
          }        
        }


        newSites.push(prevDevice);
      });

      return newSites;
    });
  }

  function resetSingleAlarmsMarkers() {
    setSites((prevState) => {
      var newSites = [];
      prevState.map((prevDevice) => {
        if (prevDevice.hasSingleAlarm) {
          prevDevice.hasSingleAlarm = false;
        }

        if (!prevDevice.hasCorrelativeAlarm) {
          prevDevice.icon =
            icons[prevDevice.additional_data.elementType](defaultColor);
        }

        newSites.push(prevDevice);
      });

      return newSites;
    });
  }

  function resetCorrelatedAlarmsMarkers() {
    setSites((prevState) => {
      var newSites = [];
      prevState.map((prevDevice) => {
        if (prevDevice.hasCorrelativeAlarm) {
          prevDevice.hasCorrelativeAlarm = false;
        }

        if (!prevDevice.hasSingleAlarm) {
          prevDevice.icon =
            icons[prevDevice.additional_data.elementType](defaultColor);
        }

        if (prevDevice.hasSingleAlarm) {
          prevDevice.icon =
            icons[prevDevice.additional_data.elementType](singleAlarmColor);
        }

        newSites.push(prevDevice);
      });

      return newSites;
    });

    const pdaColor = config.REACT_APP_PDA_DEFAULT_COLOR;
    const cabinetColor = config.REACT_APP_CABINET_DEFAULT_COLOR;

    setCircles((prevState) => {
      var newCircles = [];
      prevState.map((prevCircle) => {
        if (prevCircle.additional_data.elementType.includes("CABINET")) {
          prevCircle.color = cabinetColor;
        } else {
          prevCircle.color = pdaColor;
        }
        newCircles.push(prevCircle);
      });

      return newCircles;
    });
  }

  function markAllTheSingleAlarmsInMap(singleAlarms){
    const deviceRefIds = singleAlarms.map(alarm => alarm.deviceRefId);

    setSites((prevState) => {
      var newSites = [];
      prevState.map((prevDevice) => {
        if(deviceRefIds.includes(prevDevice.id)){        
        if (!prevDevice.hasSingleAlarm) {
          prevDevice.hasSingleAlarm = true;
        }

        if (!prevDevice.hasCorrelativeAlarm) {
          prevDevice.icon =
            icons[prevDevice.additional_data.elementType](singleAlarmColor);
        }
      }
        newSites.push(prevDevice);
      });

      return newSites;
    });    
  }

  //Funcion que permite marcar los elementos del mapa que
  //pertenecen a un correlation alarm especifico.
  //Recibe un objeto con todos los datos de la correlacion
  function showCorrelationInMap(correlationData, correlationIndex) {
    //executePost(config.REACT_APP_OPENSEARCH_BASE_URL+config.REACT_APP_ONU_TOPOLOGY_INDEX);

    setFlyToOtherPlace(false);

    //Me quedo con los devices correlacionados.
    var correlatedDevices = correlationData.correlatedDevices;

    var devicesToUpdate = [];
    correlatedDevices.forEach((correlatedDevice) => {
      var deviceToSelect = sites.find(
        (element) => element.id === correlatedDevice
      );
      if (deviceToSelect) {
        devicesToUpdate.push(deviceToSelect.id);
      }
    });

    var commonElementType;
    var commonElementValue;
    //Me quedo con el elemento en comun
    if (correlationData.alarmResource) {
      var commonElement = correlationData.alarmResource;
      if (commonElement?.includes(":")) {
        commonElementType = commonElement.split(":")[0];
        commonElementValue = commonElement.split(":")[1];
      }
    }

    //Si el elemento en comun es un splitter lo agrego para cambiar
    //el color del icon segun la causa de la alarm correlation
    if (commonElementType.includes("splitter")) {
      devicesToUpdate.push(commonElementValue);
    }

    setCircles((prevState) => {
      var newCircles = [];
      prevState.map((prevCircle) => {
        if (commonElementType === "powerDistributionArea") {
          prevCircle.color = config.REACT_APP_PDA_DEFAULT_COLOR;
          prevCircle.hasAlarm = false;
          if (commonElementValue === prevCircle.id) {
            prevCircle.color = determineColorBasedonCommonsAlarmTypes(
              correlationData.commonAlarmTypeIds
            );
            prevCircle.hasAlarm = true;
          }
        } else if (commonElementType === "cabinet") {
          prevCircle.color = config.REACT_APP_CABINET_DEFAULT_COLOR;
          prevCircle.hasAlarm = false;
          if (commonElementValue === prevCircle.id) {
            prevCircle.color = determineColorBasedonCommonsAlarmTypes(
              correlationData.commonAlarmTypeIds
            );
            prevCircle.hasAlarm = true;
          }
        } else {
          prevCircle.color = config.REACT_APP_CABINET_DEFAULT_COLOR;
          prevCircle.hasAlarm = false;
        }

        newCircles.push(prevCircle);
      });

      return newCircles;
    });

    setSites((prevState) => {
      var newSites = [];
      prevState.map((prevDevice) => {
        if (devicesToUpdate.includes(prevDevice.id)) {
          prevDevice.icon = icons[prevDevice.additional_data.elementType](
            determineColorBasedonCommonsAlarmTypes(
              correlationData.commonAlarmTypeIds
            )
          );
          prevDevice.hasCorrelativeAlarm = true;
          //prevDevice.hasSingleAlarm = false;
        } else {
          if (!prevDevice.hasSingleAlarm) {
            prevDevice.icon =
              icons[prevDevice.additional_data.elementType](defaultColor);
            prevDevice.hasCorrelativeAlarm = false;
            prevDevice.hasSingleAlarm = false;
          } else {
            prevDevice.icon =
              icons[prevDevice.additional_data.elementType](singleAlarmColor);
            prevDevice.color = singleAlarmColor;
            prevDevice.hasSingleAlarm = true;
          }
        }
        newSites.push(prevDevice);
      });

      return newSites;
    });
  }

  function determineColorBasedonCommonsAlarmTypes(commonAlarmTypes) {
    //Valido que color darle en base a si el elemento comun es un splitter,
    //un PDA o un cabinet
    var newColor = defaultColor;

    var tempAlarmType = config.REACT_APP_TEMPERATURE_ALARM_TYPE;
    var losiAlarmType = config.REACT_APP_LOSI_ALARM_TYPE;
    var lobiAlarmType = config.REACT_APP_LOBI_ALARM_TYPE;

    if (
      arrayContainsString(commonAlarmTypes, losiAlarmType) &&
      arrayContainsString(commonAlarmTypes, lobiAlarmType)
    ) {
      newColor = powerareaCutColor;
    } else if (arrayContainsString(commonAlarmTypes, tempAlarmType)) {
      newColor = temperatureColor;
    } else if (arrayContainsString(commonAlarmTypes, lobiAlarmType)) {
      newColor = fiberCutColor;
    } else {
      newColor = unknownColor;
    }

    return newColor;
  }

  function arrayContainsString(array, string) {
    let result = array.filter((item) => item.includes(string));
    return result.length !== 0;
  }

  //En true para que el mapa se relocalice y haga zoom a la zona de los elementos
  //luego cada vez que se clickee en una correlation no deberá auto ubicarse.
  const [flyToOtherPlace, setFlyToOtherPlace] = useState(true);

  //Mantengo los markers para el mapa
  const [sites, setSites] = useState(drawTopology);

  //Mantengo las lineas para el mapa
  const [lines, setLines] = useState(null);

  //Mantengo los PDA y CABINETs (Circulos)
  const [circles, setCircles] = useState(null);

  const actions = [
    <IconButton onClick={() => window.location.reload()}>
      <RefreshIcon />
    </IconButton>,
  ];

  return (
    <Layout
      title={<FormattedMessage id="title.alarms" />}
      actions={actions}
      helText={<FormattedMessage id="helper.alarms.administration" />}
    >
      <Zoom in={showMapFab} unmountOnExit>
        <Fab
          color="primary"
          sx={{ position: "fixed", bottom: "24px", right: "24px" }}
          onClick={() => mapAccordionRef.current.scrollIntoView()}
        >
          <MapIcon />
        </Fab>
      </Zoom>
      {true ? (
        <Stack spacing={2} ref={containerRef} sx={{ width: "100%" }}>
          <Card ref={mapAccordionRef}>
            <CardHeader
              action={
                <Stack direction="row">
                  <IconButton onClick={() => window.location.reload()}>
                    <RefreshIcon />
                  </IconButton>
                  <IconButton onClick={handleTopologyExpansion}>
                    {topologyExpanded ? (
                      <ArrowUpwardIcon />
                    ) : (
                      <ArrowDownwardIcon />
                    )}
                  </IconButton>
                </Stack>
              }
              title={<FormattedMessage id="title.topology" />}
            />
            <Divider />
            <Collapse in={topologyExpanded}>
              <CardContent>
                <Alert severity="info">
                  Select elements to be displayed even when there are no alarms
                  that affect them
                </Alert>
                <FormControlLabel
                  control={
                    <Checkbox
                      id="lines"
                      defaultChecked
                      onChange={handleCheckboxChange}
                    />
                  }
                  label="Connections"
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      id="PDA"
                      defaultChecked
                      onChange={handleCheckboxChange}
                    />
                  }
                  label="PDAs"
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      id="cabinet"
                      defaultChecked
                      onChange={handleCheckboxChange}
                    />
                  }
                  label="Cabinets"
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      id="splitter"
                      defaultChecked
                      onChange={handleCheckboxChange}
                    />
                  }
                  label="Splitters"
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      id="ONU"
                      defaultChecked
                      onChange={handleCheckboxChange}
                    />
                  }
                  label="ONTs"
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      id="OLT"
                      defaultChecked
                      onChange={handleCheckboxChange}
                    />
                  }
                  label="OLTs"
                />
                <Box
                  sx={{
                    height: "600px",
                    overflow: "hidden",
                    position: "relative",
                  }}
                  ref={mapRef}
                >
                  <Box
                    component="a"
                    href={config.REACT_APP_CONDOR_URL}
                    target="_blank"
                    sx={{
                      position: "absolute",
                      zIndex: "999",
                      backgroundColor: "white",
                      opacity: "0.8",
                      p: 0.5,
                      textDecoration: "inherit",
                      color: "inherit",
                      bottom: "0",
                      display: "flex",
                      alignItems: "center",
                      gap: 0.5,
                    }}
                  >
                    <Typography component="span" variant="body2">
                      Powered by
                    </Typography>
                    <img
                      src={condorLogoGrey}
                      style={{ filter: "grayscale(100%)" }}
                      height="25px"
                      alt=""
                    ></img>
                  </Box>
                  <CorrelationsMap
                    sites={sites}
                    lines={lines}
                    circles={circles}
                    flyToOtherPlace={flyToOtherPlace}
                  />
                </Box>
              </CardContent>
            </Collapse>
          </Card>

          <CorrelationsTable
            title="title.correlations"
            handleShowInMap={showCorrelationInMap}
            resetCorrelationsOnMap={resetCorrelatedAlarmsMarkers}
          />

          <AlarmsTable
            title="title.alarms"
            handleShowSingleAlarmInMap={showSingleAlarmInMap}
            resetSingleAlarmsOnMap={resetSingleAlarmsMarkers}
            selectAllSingleAlarmInMap={markAllTheSingleAlarmsInMap}
          ></AlarmsTable>
        </Stack>
      ) : (
        <Box sx={{ width: "100%" }}>
          <LinearProgress color="primary" />
        </Box>
      )}
    </Layout>
  );
};

export default Alarms;
