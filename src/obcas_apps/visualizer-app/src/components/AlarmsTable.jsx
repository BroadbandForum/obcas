import {
  Accordion,
  AccordionActions,
  AccordionDetails,
  Box,
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
import MapIcon from "@mui/icons-material/Map";

import { Fragment, useContext, useEffect, useState } from "react";
import {
  FormattedDate,
  FormattedMessage,
  FormattedTime,
  useIntl,
} from "react-intl";

import { ALARMS } from "../model/alarms.js";
import CorrelationChip from "./CorrelationChip.jsx";
import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";
import ArrowUpwardIcon from "@mui/icons-material/ArrowUpward";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import AccordionSummary from "@mui/material/AccordionSummary";
import { GetActiveAlarms } from "../services/opensearch-service.js";
import { useConfig } from "@condor/utils";
import dayjs from "dayjs";
import RefreshIcon from "@mui/icons-material/Refresh";
import { DateTimePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import FilterAltIcon from "@mui/icons-material/FilterAlt";
import FilterAltOffIcon from "@mui/icons-material/FilterAltOff";
import ClearIcon from "@mui/icons-material/Clear";
import CheckIcon from "@mui/icons-material/Check";
import { Controller, useForm } from "react-hook-form";
import SelectAllIcon from "@mui/icons-material/SelectAll";
import CheckBoxOutlineBlankIcon from "@mui/icons-material/CheckBoxOutlineBlank";
import CheckBoxIcon from "@mui/icons-material/CheckBox";

const severities = {
  critical: "rgb(217, 7, 10)",
  major: "rgb(255, 121, 0)",
  minor: "rgb(255, 191, 2)",
  warning: "rgb(255, 243, 0)",
  indeterminate: "gray",
};

const AlarmsTable = ({
  title,
  handleShowSingleAlarmInMap,
  resetSingleAlarmsOnMap,
  selectAllSingleAlarmInMap
}) => {
  //Hook para leer las configuraciones del archivo env
  const config = useConfig();

  const [rows, setRows] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(100);
  const [update, setUpdate] = useState(0);

  const filterForm = useForm();
  const [filtersValue, setFiltersValue] = useState({});
  const [showFilters, setShowFilters] = useState(false);

  const handleChangePage = (event, newPage) => {
    if (newPage === pageWithSelectedRow) {
      setSelectedRows(lastRowsSelected);
    } else {
      setSelectedRows([]);
    }

    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  //States usados para marcar fila seleccionada segun pagina
  const [selectedRows, setSelectedRows] = useState([]);
  const [pageWithSelectedRow, setPageWithSelectedRow] = useState(0);
  const [lastRowsSelected, setLastRowsSelected] = useState([]);
  const [showAllSelected, setShowAllSelected] = useState(false);

  const handleSelectRow = (row, rowIndex) => {

    var disable = selectedRows.includes(rowIndex);
    //Actualizo mapa
    handleShowSingleAlarmInMap(row,disable);
    
    setSelectedRows((prev) => {
        if(prev.includes(rowIndex)){
          const index = prev.indexOf(rowIndex);
          if (index > -1) { // only splice array when item is found
            prev.splice(index, 1); // 2nd parameter means remove one item only
          }
          return prev;
        }else{
          return [...prev, rowIndex];
        }
      });
  
    setLastRowsSelected((prev) => [...prev, rowIndex]);
    setPageWithSelectedRow(page);
  };


  const resetSelectedRows = () => {
    //setUpdate(update + 1);

    setSelectedRows([]);
    setLastRowsSelected([]);
    setPageWithSelectedRow(0);

    //Actualizo mapa
    resetSingleAlarmsOnMap();
  };

  function handleSelectAll(rows){
    if (showAllSelected){
      resetSelectedRows();
      setShowAllSelected(false);
    }else{
      setSelectedRows([]);
      rows
      ?.slice(
        page * rowsPerPage,
        page * rowsPerPage + rowsPerPage
      )
      .forEach((row, index) => {
        setSelectedRows((prev) => {
          if(!prev.includes(index+1)){
            return [...prev, index+1];
          }
        });      
      });

      selectAllSingleAlarmInMap(rows);
      setShowAllSelected(true);
    }
  }

  const [expanded, setExpanded] = useState(true);

  const handleExpansion = () => {
    setExpanded((prevExpanded) => !prevExpanded);
  };

  useEffect(() => {
    GetActiveAlarms(config.REACT_APP_ACTIVE_ALARMS_INDEX)
      .then((result) => {
        let filteredResult = result;

        if (filtersValue.rangeSearch?.raisedTime) {
          if (filtersValue.rangeSearch.raisedTime.from) {
            filteredResult = filteredResult.filter((a) =>
              dayjs(a.raisedTime).isAfter(
                dayjs(filtersValue.rangeSearch.raisedTime.from)
              )
            );
          }

          if (filtersValue.rangeSearch.raisedTime.to) {
            filteredResult = filteredResult.filter((a) =>
              dayjs(a.raisedTime).isBefore(
                dayjs(filtersValue.rangeSearch.raisedTime.to)
              )
            );
          }
        }

        if (filtersValue.partialSearch) {
          Object.entries(filtersValue.partialSearch).forEach(([key, value]) => {
            filteredResult = filteredResult.filter((alarm) =>
              alarm[key]?.toLowerCase().includes(value.toLowerCase())
            );
          });
        }

        /*if (filtersValue.partialSearch?.deviceRefId) {
          filteredResult = filteredResult.filter((a) =>
            a.deviceRefId?.includes(filtersValue.partialSearch.deviceRefId)
          );
        }
        if (filtersValue.partialSearch?.alarmTypeId) {
          filteredResult = filteredResult.filter((a) =>
            a.alarmTypeId?.includes(filtersValue.partialSearch.alarmTypeId)
          );
        }
        if (filtersValue.partialSearch?.alarmResource) {
          filteredResult = filteredResult.filter((a) =>
            a.alarmResource?.includes(filtersValue.partialSearch.alarmResource)
          );
        }
        if (filtersValue.partialSearch?.vAniRefId) {
          filteredResult = filteredResult.filter((a) =>
            a.vAniRefId?.includes(filtersValue.partialSearch.vAniRefId)
          );
        }*/

        setRows(
          filteredResult.sort((a, b) =>
            dayjs(a.raisedTime).isBefore(dayjs(b.raisedTime)) ? 1 : -1
          )
        );
      })
      .catch({});
  }, [update, filtersValue]);

  const onSubmit = (data) => {
    resetSelectedRows();
    resetSingleAlarmsOnMap();
    setFiltersValue({
      partialSearch: {
        ...(data.deviceRefId && { deviceRefId: data.deviceRefId }),
        ...(data.alarmTypeId && { alarmTypeId: data.alarmTypeId }),
        ...(data.alarmResource && { alarmResource: data.alarmResource }),
        ...(data.vAniRefId && { vAniRefId: data.vAniRefId }),
      },
      rangeSearch: {
        raisedTime: {
          ...(data.timeFrom && { from: data.timeFrom }),
          ...(data.timeTo && { to: data.timeTo }),
        },
      },
    });
  };

  const onReset = () => {
    resetSelectedRows();
    resetSingleAlarmsOnMap();
    setFiltersValue({});
    filterForm.setValue("timeFrom", null);
    filterForm.setValue("timeTo", null);
    filterForm.setValue("deviceRefId", "");
    filterForm.setValue("alarmTypeId", "");
    filterForm.setValue("alarmResource", "");
    filterForm.setValue("vAniRefId", "");
  };

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
        title={<FormattedMessage id={title} />}
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
                label={<FormattedMessage id="field.deviceRefId" />}
                {...filterForm.register("deviceRefId")}
              />
              <TextField
                size="small"
                label={<FormattedMessage id="field.alarmTypeId" />}
                {...filterForm.register("alarmTypeId")}
              />
              <TextField
                size="small"
                label={<FormattedMessage id="field.alarmResource" />}
                {...filterForm.register("alarmResource")}
              />
              <TextField
                size="small"
                label={<FormattedMessage id="field.vAniRefId" />}
                {...filterForm.register("vAniRefId")}
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
                <TableRow>
                  <TableCell>
                    <FormattedMessage id="field.raisedTime" />
                  </TableCell>
                  <TableCell>
                    <FormattedMessage id="field.deviceRefId" />
                  </TableCell>
                  <TableCell>
                    <FormattedMessage id="field.alarmTypeId" />
                  </TableCell>
                  <TableCell>
                    <FormattedMessage id="field.alarmResource" />
                  </TableCell>
                  <TableCell>
                    <FormattedMessage id="field.vAniRefId" />
                  </TableCell>
                  <TableCell>
                    <Tooltip title="Show all alarms in map">
                      <IconButton
                        onClick={() => {
                          handleSelectAll(rows);
                        }}
                      >
                        <SelectAllIcon />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {rows
                  ?.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((row, index) => (
                    <TableRow
                      key={index}
                      sx={{
                        "&:last-child td, &:last-child th": { border: 0 },
                        "&.MuiTableRow-root.Mui-selected": {
                          backgroundColor: config.REACT_APP_SINGLE_ALARM_COLOR,
                          "& > .MuiTableCell-root": {
                            color: "white",
                          },
                        },
                      }}
                      selected={selectedRows.includes(index + 1)}
                    >
                      <TableCell>
                        <AlarmDate date={row.raisedTime} />
                      </TableCell>
                      <TableCell>{row.deviceRefId}</TableCell>
                      <TableCell>{row.alarmTypeId}</TableCell>
                      <TableCell>
                        <Tooltip title={row.alarmResource}>
                          <Typography
                            variant="body2"
                            sx={{
                              maxWidth: "200px",
                              whiteSpace: "nowrap",
                              overflow: "hidden",
                              textOverflow: "ellipsis",
                            }}
                          >
                            {row.alarmResource}
                          </Typography>
                        </Tooltip>
                      </TableCell>
                      <TableCell>{row.vAniRefId}</TableCell>
                      <TableCell>
                        <Tooltip title="Show Alarm In Map">
                          <IconButton
                            key={index}
                            onClick={() => {
                              handleSelectRow(row, index + 1);
                            }}
                          >
                            {selectedRows.includes(index + 1) ? (
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

const AlarmDate = ({ date }) => {
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

export default AlarmsTable;
