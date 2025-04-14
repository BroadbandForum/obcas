import { Chip } from "@mui/material";
import CircleIcon from "@mui/icons-material/Circle";
import { green } from "@mui/material/colors";
import { useConfig } from "@condor/utils";

const CorrelationChip = ({ info, selected }) => {
  //Hook para leer las configuraciones del archivo env
  const config = useConfig();

  //Colores usados para identificar las alarm correlations con los markers del mapa
  const powerareaCutColor = config.REACT_APP_PDA_ALARM_COLOR;
  const fiberCutColor = config.REACT_APP_FIBERCUT_ALARM_COLOR;
  const temperatureColor = config.REACT_APP_TEMPERATURE_ALARM_COLOR;
  const unknownColor = config.REACT_APP_UNKNOWN_ALARM_COLOR;

  //Color default para los markers del mapa
  const defaultColor = config.REACT_APP_MARKER_DEFAULT_COLOR;

  let commonAlarmTypes = info.commonAlarmTypeIds;
  //Valido que color darle en base a si el elemento comun es un splitter,
  //un PDA o un cabinet
  let color = defaultColor;
  let label = "";

  var tempAlarmType = config.REACT_APP_TEMPERATURE_ALARM_TYPE;
  var losiAlarmType = config.REACT_APP_LOSI_ALARM_TYPE;
  var lobiAlarmType = config.REACT_APP_LOBI_ALARM_TYPE;

  if (
    arrayContainsString(commonAlarmTypes, losiAlarmType) &&
    arrayContainsString(commonAlarmTypes, lobiAlarmType)
  ) {
    color = powerareaCutColor;
    label = "Power Cut";
  } else if (arrayContainsString(commonAlarmTypes, tempAlarmType)) {
    color = temperatureColor;
    label = "Temperature";
  } else if (arrayContainsString(commonAlarmTypes, lobiAlarmType)) {
    color = fiberCutColor;
    label = "Fiber Cut";
  }else{
    color = unknownColor;
    label = "Unknown";
  }

  function arrayContainsString(array, string) {
    let result = array.filter((item) => item.includes(string));
    return result.length !== 0;
  }

  return (
    <Chip
      icon={
        <CircleIcon
          style={{
            color: selected ? "white" : color,
          }}
        />
      }
      label={label}
      variant="outlined"
      sx={{
        borderColor: selected ? "white" : color,
        color: selected ? "white" : color,
      }}
    />
  );
};

export default CorrelationChip;
