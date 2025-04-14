import {
  Button,
  Card,
  CardContent,
  CardHeader,
  Collapse,
  Divider,
  IconButton,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  TextField,
  Toolbar,
  Tooltip,
  Typography,
} from "@mui/material";
import { Fragment, useContext, useEffect, useState } from "react";
import {
  FormattedDate,
  FormattedMessage,
  FormattedTime,
  useIntl,
} from "react-intl";
import { CORRELATIONS } from "../model/correlations.js";
import CorrelationChip from "./CorrelationChip.jsx";
import MapIcon from "@mui/icons-material/Map";
import { GetActiveCorrelatedAlarms } from "../services/opensearch-service.js";
import { useConfig } from "@condor/utils";
import dayjs from "dayjs";
import RefreshIcon from "@mui/icons-material/Refresh";
import { DateTimePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import FilterAltIcon from "@mui/icons-material/FilterAlt";
import ClearIcon from "@mui/icons-material/Clear";
import { Controller, useForm } from "react-hook-form";
import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";
import ArrowUpwardIcon from "@mui/icons-material/ArrowUpward";
import CheckIcon from "@mui/icons-material/Check";
import FilterAltOffIcon from "@mui/icons-material/FilterAltOff";
import CheckBoxOutlineBlankIcon from "@mui/icons-material/CheckBoxOutlineBlank";
import CheckBoxIcon from "@mui/icons-material/CheckBox";

const severities = {
  critical: "rgb(217, 7, 10)",
  major: "rgb(255, 121, 0)",
  minor: "rgb(255, 191, 2)",
  warning: "rgb(255, 243, 0)",
  indeterminate: "gray",
};

const CorrelationsTable = ({
  title,
  handleShowInMap,
  resetCorrelationsOnMap,
}) => {
  //Hook para leer las configuraciones del archivo env
  const config = useConfig();

  const [rows, setRows] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [update, setUpdate] = useState(0);

  const filterForm = useForm();
  const [filtersValue, setFiltersValue] = useState({});
  const [showFilters, setShowFilters] = useState(false);

  const handleChangePage = (event, newPage) => {
    if (newPage === pageWithSelectedRow) {
      setSelectedRow(lastRowSelected);
    } else {
      setSelectedRow(0);
    }
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  //States usados para marcar fila seleccionada segun pagina
  const [selectedRow, setSelectedRow] = useState(0);
  const [pageWithSelectedRow, setPageWithSelectedRow] = useState(0);
  const [lastRowSelected, setLastRowSelected] = useState(0);

  const handleSelectRow = (rowIndex,row) => {

    if(selectedRow===rowIndex){
      resetCorrelationsOnMap();
    }else{
      handleShowInMap(row, rowIndex);
    }

    setSelectedRow((prev) => {
      if(prev === rowIndex){
        return 0;
      }else{
        return rowIndex;
      }
    });

    setLastRowSelected((prev) => {
      if(prev === rowIndex){
        return 0;
      }else{
        return rowIndex;
      }
    });

    setPageWithSelectedRow(page);
  };

  const resetSelectedRows = () => {
    setUpdate(update + 1);

    setSelectedRow(0);
    setLastRowSelected(0);
    setPageWithSelectedRow(0);

    //Actualizo mapa
    resetCorrelationsOnMap();

  };

  const [expanded, setExpanded] = useState(true);
  const handleExpansion = () => {
    setExpanded((prevExpanded) => !prevExpanded);
  };

  useEffect(() => {
    GetActiveCorrelatedAlarms(config.REACT_APP_ACTIVE_ALARMS_INDEX)
      .then((result) => {
        let filteredResult = result;
         

        //if 'from' is set, it keeps the alarms that ocurred after the specified time
        if (filtersValue.rangeSearch?.time) {
          if (filtersValue.rangeSearch.time.from) {
            filteredResult = filteredResult.filter((a) =>
              dayjs(a.time).isAfter(dayjs(filtersValue.rangeSearch.time.from))
            );
          }
          
          //if 'to' is set, it keeps the alarms that ocurred before the specified time
          if (filtersValue.rangeSearch.time.to) {
            filteredResult = filteredResult.filter((a) =>
              dayjs(a.time).isBefore(dayjs(filtersValue.rangeSearch.time.to))
            );
          }
        }
         //If 'correlated devices' filter is set then it filters alarms where the correlated devices match the search query
        if (filtersValue.partialSearch?.correlatedDevices) {
          filteredResult = filteredResult.filter((a) =>
            formatCorrelatedDevices(a.correlatedDevices)
              .join(", ")
              .toLowerCase()
              .includes(
                filtersValue.partialSearch.correlatedDevices.toLowerCase()
              )
          );
        }

        //Searches for alarms where the formatted splitter information contains the given attribute
        if (filtersValue.partialSearch?.commonAttribute) {
          filteredResult = filteredResult.filter((a) =>
            formatSplitterInfo(a)
              .toLowerCase()
              .includes(
                filtersValue.partialSearch.commonAttribute.toLowerCase()
              )
          );
        }
        //searches for alarms where the common alarm type IDs contain the given type
        if (filtersValue.partialSearch?.commonAlarmTypeIds) {
          filteredResult = filteredResult.filter((a) =>
            formatCommonAlarmTypes(a.commonAlarmTypeIds)
              .toLowerCase()
              .includes(
                filtersValue.partialSearch.commonAlarmTypeIds.toLowerCase()
              )
          );
        }
        //it filters alarms by correlation state
        if (filtersValue.partialSearch?.correlationStatus) {
          filteredResult = filteredResult.filter((a) =>
            (a.correlationStatus ? a.correlationStatus : a.alarmStatus)
              .toLowerCase()
              .includes(
                filtersValue.partialSearch.correlationStatus.toLowerCase()
              )
          );
        }

        setRows((prev) => []);

        setRows((prev) =>
          filteredResult.sort((a, b) =>
            dayjs(a.time).isBefore(dayjs(b.time)) ? 1 : -1
          )
        );
      })
      .catch({});
  }, [update, filtersValue]);

  const onSubmit = (data) => {
    resetSelectedRows();
    setFiltersValue({
      partialSearch: {
        ...(data.correlatedDevices && {
          correlatedDevices: data.correlatedDevices,
        }),
        ...(data.commonAttribute && { commonAttribute: data.commonAttribute }),
        ...(data.commonAlarmTypeIds && {
          commonAlarmTypeIds: data.commonAlarmTypeIds,
        }),
        ...(data.correlationStatus && {
          correlationStatus: data.correlationStatus,
        }),
      },
      rangeSearch: {
        time: {
          ...(data.timeFrom && { from: data.timeFrom }),
          ...(data.timeTo && { to: data.timeTo }),
        },
      },
    });
  };

  const onReset = () => {
    resetSelectedRows();
    setFiltersValue({});
    filterForm.setValue("timeFrom", null);
    filterForm.setValue("timeTo", null);
    filterForm.setValue("correlatedDevices", "");
    filterForm.setValue("commonAttribute", "");
    filterForm.setValue("commonAlarmTypeIds", "");
    filterForm.setValue("correlationStatus", "");
  };

  function determineColorBasedonAlarmResource(correlationData) {
    //Colores usados para identificar las alarm correlations con los markers del mapa
    const powerareaCutColor = config.REACT_APP_PDA_ALARM_COLOR;
    const fiberCutColor = config.REACT_APP_FIBERCUT_ALARM_COLOR;
    const temperatureColor = config.REACT_APP_TEMPERATURE_ALARM_COLOR;
    const unknownColor = config.REACT_APP_UNKNOWN_ALARM_COLOR;

    var tempAlarmType = config.REACT_APP_TEMPERATURE_ALARM_TYPE;
    var losiAlarmType = config.REACT_APP_LOSI_ALARM_TYPE;
    var lobiAlarmType = config.REACT_APP_LOBI_ALARM_TYPE;

    var commonAlarmTypes = correlationData?.commonAlarmTypeIds;

    //Valido que color darle en base a si el elemento comun es un splitter,
    //un PDA o un cabinet
    var newColor;
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

  return (
    <Card>
      <CardHeader
        action={
          <Stack direction="row">
            {expanded && (
              <>
                <IconButton onClick={() => setShowFilters(!showFilters)}>
                  {showFilters ? <FilterAltOffIcon /> : <FilterAltIcon />}
                </IconButton>
                {/* <IconButton onClick={resetSelectedRows}>
                  <RefreshIcon />
                </IconButton> */}
              </>
            )}
            <IconButton onClick={handleExpansion}>
              {expanded ? <ArrowUpwardIcon /> : <ArrowDownwardIcon />}
            </IconButton>
          </Stack>
        }
        title={<FormattedMessage id="title.correlations" />}
      />
      <Divider />
      <Collapse in={expanded}>
        <CardContent>
          <Collapse in={showFilters}>
            <Stack
              direction="row"
              component="form"
              onSubmit={filterForm.handleSubmit(onSubmit)}
              sx={{ mb: 2 }}
              spacing={2}
            >
              {/*             <TextField
              size="small"
              label={<FormattedMessage id="field.correlativeId" />}
            /> */}
              <LocalizationProvider dateAdapter={AdapterDayjs}>
                <Controller
                  name="timeFrom"
                  control={filterForm.control}
                  defaultValue={null}
                  render={({ field: { onChange, value } }) => (
                    <DateTimePicker
                      slotProps={{ textField: { size: "small" } }}
                      label="Time from"
                      value={value}
                      control={filterForm.control}
                      onChange={(event) => onChange(event)}
                    />
                  )}
                />
                <Controller
                  name="timeTo"
                  control={filterForm.control}
                  defaultValue={null}
                  render={({ field: { onChange, value } }) => (
                    <DateTimePicker
                      slotProps={{ textField: { size: "small" } }}
                      label="Time to"
                      value={value}
                      control={filterForm.control}
                      onChange={(event) => onChange(event)}
                    />
                  )}
                />
              </LocalizationProvider>
              <TextField
                size="small"
                label={<FormattedMessage id="field.correlatedDevices" />}
                {...filterForm.register("correlatedDevices")}
              />
              <TextField
                size="small"
                label={<FormattedMessage id="field.commonAttribute" />}
                {...filterForm.register("commonAttribute")}
              />
              <TextField
                size="small"
                label={<FormattedMessage id="field.commonAlarmTypeIds" />}
                {...filterForm.register("commonAlarmTypeIds")}
              />
              <TextField
                size="small"
                label={<FormattedMessage id="field.correlationStatus" />}
                {...filterForm.register("correlationStatus")}
              />
              <IconButton color="primary" type="submit">
                <CheckIcon />
              </IconButton>
              <IconButton onClick={onReset}>
                <ClearIcon />
              </IconButton>
            </Stack>
          </Collapse>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow key="CorrelationTable-header">
                  <TableCell>
                    <FormattedMessage id="field.correlativeId" />
                  </TableCell>
                  <TableCell>
                    <FormattedMessage id="field.time" />
                  </TableCell>
                  <TableCell>
                    <FormattedMessage id="field.correlatedDevices" />
                  </TableCell>
                  <TableCell>
                    <FormattedMessage id="field.commonAttribute" />
                  </TableCell>
                  <TableCell>
                    <FormattedMessage id="field.commonAlarmTypeIds" />
                  </TableCell>
                  <TableCell>
                    <FormattedMessage id="field.correlationStatus" />
                  </TableCell>
                  <TableCell>Show in map</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {rows
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((row, index) => (
                    <TableRow
                      sx={{
                        "&:last-child td, &:last-child th": { border: 0 },
                        "&.MuiTableRow-root.Mui-selected": {
                          backgroundColor:
                            determineColorBasedonAlarmResource(row),
                          "& > .MuiTableCell-root": {
                            color: "white",
                          },
                        },
                      }}
                      selected={selectedRow === index + 1}
                    >
                      <TableCell sx={{ py: 0 }}>
                        <CorrelationChip
                          info={row}
                          selected={selectedRow === index + 1}
                        />
                      </TableCell>
                      <TableCell>
                        <CorrelationDate date={row.time} />
                      </TableCell>
                      <TableCell>
                        <Tooltip
                          title={formatCorrelatedDevices(row.correlatedDevices)}
                        >
                          <Typography
                            variant="body2"
                            sx={{
                              maxWidth: "200px",
                              whiteSpace: "nowrap",
                              overflow: "hidden",
                              textOverflow: "ellipsis",
                            }}
                          >
                            {formatCorrelatedDevices(row.correlatedDevices)}
                          </Typography>
                        </Tooltip>
                      </TableCell>
                      <TableCell>{formatSplitterInfo(row)}</TableCell>
                      <TableCell>
                        {formatCommonAlarmTypes(row.commonAlarmTypeIds)}
                      </TableCell>
                      <TableCell>
                        {row.correlationStatus
                          ? row.correlationStatus
                          : row.alarmStatus}
                      </TableCell>
                      <TableCell>
                        <Tooltip title="Show Correlation In Map">
                          <IconButton
                            key={index}
                            onClick={() => {
                              handleSelectRow(index + 1,row);                              
                            }}
                          >
                            {selectedRow === index + 1 ? (
                              <CheckBoxIcon sx={{ color: "white" }} />
                            ) : (
                              <CheckBoxOutlineBlankIcon />
                            )}
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
            <TablePagination
              component="div"
              count={rows?.length}
              page={page}
              rowsPerPage={rowsPerPage}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
            />
          </TableContainer>
        </CardContent>
      </Collapse>
    </Card>
  );
};

const prettifyCamelCase = (str) => {
  var output = "";
  var len = str.length;
  var char;

  for (var i = 0; i < len; i++) {
    char = str.charAt(i);

    if (i == 0) {
      output += char.toUpperCase();
    } else if (char !== char.toLowerCase() && char === char.toUpperCase()) {
      output += " " + char;
    } else if (char == "-" || char == "_") {
      output += " ";
    } else {
      output += char;
    }
  }

  return output;
};

const isSeverity = (key) => {
  return key.endsWith("Severity");
};

const isDate = (date) => {
  return new Date(date) !== "Invalid Date" && !isNaN(new Date(date));
};

function formatSplitterInfo(correlativeAlarm) {
  if (correlativeAlarm.commonAttribute) {
    return (
      correlativeAlarm.commonAttribute +
      ":" +
      correlativeAlarm.commonAttributeValue
    );
  } else if (correlativeAlarm.alarmResource) {
    if (correlativeAlarm.alarmResource.includes(":")) {
      return (
        correlativeAlarm.alarmResource.split(":")[0] +
        ":" +
        correlativeAlarm.alarmResource.split(":")[1]
      );
    }
  }
}

function formatCorrelatedDevices(correlatedDevicesToFormat) {
  var formattedDevices = correlatedDevicesToFormat.map(
    (notification, index, notifs) => {
      if (notifs.length !== index + 1) return notification + ", ";
      else {
        return notification;
      }
    }
  );
  return formattedDevices;
}

function formatCommonAlarmTypes(alarmTypeIds) {
  return alarmTypeIds.join(", ");
}

const CorrelationDate = ({ date }) => {
  const intl = useIntl();
  const parsedDate = new Date(date);

  const formattedDate = intl.formatDate(parsedDate, {
    year: "numeric",
    month: "short",
    day: "2-digit",
  });

  const formattedTime = intl.formatTime(parsedDate, {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });

  const dateTime = `${formattedDate} ${formattedTime}`;

  return dateTime;
};

export default CorrelationsTable;
