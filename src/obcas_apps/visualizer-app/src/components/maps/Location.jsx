import {
  Grid,
  Stack,
  Box,
  Select,
  FormControl,
  InputLabel,
  MenuItem,
  OutlinedInput,
  Button,
  IconButton,
  Modal,
  Paper,
  FormHelperText,
} from "@mui/material";
import { FormattedMessage, useIntl } from "react-intl";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMap,
  useMapEvent,
  Circle,
  Polyline,
  Tooltip,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import icon from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";
import React, { useEffect, useMemo, useRef, useState } from "react";
import LocationService from "../../services/location-service";
import { useSetRecoilState } from "recoil";
import { commonLoading } from "@condor/utils/hooks/common";
import "leaflet-control-geocoder/dist/Control.Geocoder.css";
import "leaflet-control-geocoder/dist/Control.Geocoder.js";
import SearchIcon from "@mui/icons-material/Search";
import MapIcon from "@mui/icons-material/Map";
import CloseIcon from "@mui/icons-material/Close";
import useValidators from "../../hooks/useValidations";
import CommonDataService from "../../services/common-data-service";
import Alert from "@mui/material/Alert";
import LabeledMarker from 'leaflet-labeled-circle';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

L.Marker.prototype.options.icon = DefaultIcon;

const MapEvents = ({ setMarkerLatLng }) => {
  const map = useMapEvent("click", (e) => {
    setMarkerLatLng(e.latlng);
  });
  return null;
};

const LeafletControlGeocoder = ({ address, setMarkerLatLng }) => {
  const map = useMap();

  useEffect(() => {
    // creaet Geocoder nominatim
    var geocoder = L.Control.Geocoder.nominatim();

    if (address) {
      geocoder.geocode(address, (resultArray) => {
        if (resultArray.length > 0) {
          const result = resultArray[0];
          const latlng = result.center;

          //L.marker(latlng).addTo(map).bindPopup(result.name);
          setMarkerLatLng(latlng);
          map.flyToBounds(result.bbox);
        }
      });
    }
  }, [address]);

  return null;
};

const AddressForm = ({ addresInputs, editable, errors, register, address }) => {
  return (
    <>
      {addresInputs.map((item) => (
        <Grid item xs={3} {...item.gridProps} key={item.props.name}>
          <FormControl
            fullWidth
            {...(editable && { required: item.props.required })}
          >
            <InputLabel id={`${item.props.name}-label`}>
              {item.props.label}
            </InputLabel>

            {editable && item.children ? (
              <Select
                labelId={`${item.props.name}-label`}
                label={item.props.label}
                inputProps={{
                  ...(item.props.inputProps && {
                    "data-test": item.props.inputProps["data-test"],
                  }),
                }}
                {...register(item.props.name, item.validations)}
                error={!!errors[item.props.name]}
                {...(editable &&
                  address && { defaultValue: address[item.props.name] })}
              >
                {item.children}
              </Select>
            ) : (
              <OutlinedInput
                sx={{
                  "& .MuiInputBase-input.Mui-disabled": {
                    WebkitTextFillColor: "#000000",
                  },
                }}
                labelId={`${item.props.name}-label`}
                label={item.props.label}
                disabled={!editable}
                inputProps={{
                  ...(item.props.inputProps && {
                    "data-test": item.props.inputProps["data-test"],
                  }),
                }}
                style={!editable ? { backgroundColor: "#ebebeb" } : {}}
                error={!!errors[item.props.name]}
                {...register(item.props.name, item.validations)}
              ></OutlinedInput>
            )}
            <FormHelperText error={!!errors[item.props.name]}>
              {errors[item.props.name]?.message}
            </FormHelperText>
          </FormControl>
        </Grid>
      ))}
    </>
  );
};

export const Location = ({
  setAddressData, //funcion para setear los datos de la direccion en el componente padre de Location
  register, //register del useForm hook
  errors, //errors del useForm hook
  watch, //watch del useForm hook
  editable = true,
  address, //Objeto address con todos los campos
  latLng, //Arry de dos elementos con la latitud y la longitud del marker del mapa
  hideMap = false, //ocultar el mapa para usar solo los datos de formulario address
  exclude = [], //Permite sacar campos del formulario, por ejemplo piso departamento y tipo que no se usan en alta de CTO
}) => {
  const [countries, setCountries] = useState([]);
  const [states, setStates] = useState([]);
  const [cities, setCities] = useState([]);

  const [country, setCountry] = useState(address ? address.country : "");
  const [state, setState] = useState(address ? address.state : "");
  const [city, setCity] = useState(address ? address.city : "");
  const [street, setStreet] = useState(address ? address.street : "");
  const [number, setNumber] = useState(address ? address.number : "");

  const [height, setHeight] = useState(0);
  const ref = useRef(null);

  const [locationTypes, setLocationTypes] = useState([]);

  const intl = useIntl();
  const validators = useValidators();

  const [map, setMap] = useState(null);
  const markerRef = useRef(null);
  const [fullAddress, setFullAddress] = useState("");
  const [markerLatLng, setMarkerLatLng] = useState(latLng ? latLng : null);

  const setLoading = useSetRecoilState(commonLoading);

  const service = LocationService();
  const commonDataService = CommonDataService();

  useEffect(() => {
    setHeight(ref.current.clientHeight);
    setTimeout(function () {
      map?.invalidateSize();
    }, 400);
  }, [map, ref]);

  useEffect(() => {
    if (markerLatLng) {
      var latlngbounds = new L.latLngBounds();
      latlngbounds.extend(L.latLng(markerLatLng));
      map?.fitBounds(latlngbounds);
    } else if (address) {
      //Si no viene la latLon pero si viene el address es el caso del cliente,
      //busco la direccion para mostrar algo en el mapa
      searchAddress();
    }
  }, [map, markerLatLng]);

  useEffect(() => {
    if (editable) {
      commonDataService
        .getLocationTypes()
        .then((result) => setLocationTypes(result))
        .catch((error) => {
          console.log(error);
        });

      if (countries.length === 0) {
        setLoading(true);
        service
          .getCountries()
          .then((result) => {
            setCountries(result);
          })
          .catch((error) => {
            console.log(error);
          })
          .finally(() => {
            setLoading(false);
          });
      }
      if (country && states.length === 0) {
        setLoading(true);
        service
          .getStates(country)
          .then((result) => {
            setStates(result);
          })
          .catch((error) => {
            console.log(error);
          })
          .finally(() => {
            setLoading(false);
          });
      }

      if (country && state && cities.length === 0) {
        setLoading(true);
        service
          .getCities(country, state)
          .then((result) => {
            setCities(result);
          })
          .catch((error) => {
            console.log(error);
          })
          .finally(() => {
            setLoading(false);
          });
      }
    }
  }, [country, state]);

  watch((data, { name, type }) => {
    //console.log(data, name, type);
    switch (name) {
      case "country":
        setCountry(data?.country);
        setStates([]);
        setCities([]);
        setAddressData("state", "");
        setAddressData("city", "");
        setState("");
        setCity("");
        let country = countries.find(
          (country) => country.name === data?.country
        );
        !hideMap && country && map.flyTo([country.lat, country.lng], 5);
        break;
      case "state":
        setState(data?.state);
        setCities([]);
        setAddressData("city", "");
        setCity("");
        let state = states.find((state) => state.name === data?.state);
        !hideMap && state && map.flyTo([state.lat, state.lng], 8);
        break;
      case "city":
        setCity(data?.city);
        let city = cities.find((city) => city.name === data?.city);
        !hideMap && city && map.flyTo([city.lat, city.lng], 13);
        break;
      case "street":
        setStreet(data?.street);
        break;
      case "number":
        setNumber(data?.number);
        break;
    }
  });

  const markerEventHandlers = useMemo(
    () => ({
      dragend() {
        const marker = markerRef.current;
        if (marker != null) {
          handleMarkerPosition(marker.getLatLng());
        }
      },
    }),
    []
  );

  const handleMarkerPosition = (latLng) => {
    setMarkerLatLng(latLng);
    setAddressData("lat", latLng.lat);
    setAddressData("lon", latLng.lng);
  };

  const searchAddress = () => {
    //setFullAddress(`${street} ${number}, ${city}, ${state}, ${country}`);
    setFullAddress(
      [street, number, city, state, country].filter(Boolean).join(", ")
    );
  };

  const addresInputs = [
    {
      props: {
        label: <FormattedMessage id="field.country" />,
        name: "country",
        required: true,
        inputProps: { "data-test": "country" },
      },
      validations: {
        required: validators.required,
      },
      children:
        editable &&
        countries.map((country) => (
          <MenuItem key={country.name} value={country.name}>
            {country.name}
          </MenuItem>
        )),
    },
    {
      props: {
        label: <FormattedMessage id="field.state" />,
        name: "state",
        required: true,
        inputProps: { "data-test": "state" },
      },
      validations: {
        required: validators.required,
      },
      children:
        editable &&
        states.map((state) => (
          <MenuItem key={state.name} value={state.name}>
            {state.name}
          </MenuItem>
        )),
    },
    {
      props: {
        label: <FormattedMessage id="field.city" />,
        name: "city",
        required: true,
        inputProps: { "data-test": "city" },
      },
      validations: {
        required: validators.required,
      },
      children:
        editable &&
        cities.map((city) => (
          <MenuItem key={city.name} value={city.name}>
            {`${city.name} (${city.municipality})`}
          </MenuItem>
        )),
    },
    {
      props: {
        label: <FormattedMessage id="field.street" />,
        name: "street",
        required: true,
        inputProps: { "data-test": "street" },
      },
      validations: {
        required: validators.required,
      },
      gridProps: {
        xs: 2,
      },
    },
    {
      props: {
        label: <FormattedMessage id="field.number" />,
        name: "number",
        required: true,
        inputProps: { "data-test": "number" },
      },
      validations: {
        required: validators.required,
        pattern: validators.numbers,
      },
      gridProps: {
        xs: 1,
      },
    },
    {
      props: {
        label: <FormattedMessage id="field.floor" />,
        name: "floor",
        inputProps: { "data-test": "floor" },
        required: false,
      },
      validations: {
        pattern: validators.numbers,
      },
      gridProps: {
        xs: 1,
      },
    },
    {
      props: {
        label: <FormattedMessage id="field.apartment" />,
        name: "apartment",
        inputProps: { "data-test": "apartment" },
        required: false,
      },
      // validations: {
      //   pattern: validators.numbers,
      // },
      gridProps: {
        xs: 1,
      },
    },
    {
      props: {
        label: <FormattedMessage id="field.type" />,
        name: "type",
        required: true,
        inputProps: { "data-test": "type" },
      },
      validations: {
        required: validators.required,
      },
      gridProps: {
        xs: 1,
      },
      children:
        editable &&
        locationTypes.map((type) => (
          <MenuItem key={type} value={type}>
            {type}
          </MenuItem>
        )),
    },
  ].filter((item) => !exclude.includes(item.props.name));

  return (
    <>
      {hideMap ? (
        <Grid container spacing={2} columns={{ xs: 3, sm: 6 }}>
          <AddressForm
            addresInputs={addresInputs}
            editable={editable}
            errors={errors}
            register={register}
            address={address}
          />
        </Grid>
      ) : (
        <>
          <Stack gap={2} direction={{ sm: "column", md: "row" }} sx={{ mb: 1 }}>
            <Grid container spacing={2} columns={{ xs: 3 }} ref={ref}>
              <AddressForm
                addresInputs={addresInputs}
                editable={editable}
                errors={errors}
                register={register}
                address={address}
              />
              <input
                type="hidden"
                id="lat"
                name="lat"
                {...register("lat", { required: true })}
              ></input>
              <input
                type="hidden"
                id="lon"
                name="lon"
                {...register("lon", { required: true })}
              ></input>
            </Grid>
            <Grid
              container
              direction="column"
              justifyContent="flex-start"
              alignItems="stretch"
            >
              <Grid item xs={1}>
                {ref && (
                  <Box
                    sx={{
                      height: `${height - (editable ? 60 : 0)}px`,
                      width: "100%",
                      ...((!!errors.lat || !!errors.lon) && {
                        border: 1,
                        borderColor: "red",
                      }),
                    }}
                  >
                    <MapContainer
                      style={{ height: "100%", minHeight: "100%" }}
                      center={[-34, -64]}
                      zoom={5}
                      ref={setMap}
                    >
                      <TileLayer
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                      />
                      {markerLatLng && (
                        <Marker
                          position={markerLatLng}
                          draggable={editable}
                          eventHandlers={markerEventHandlers}
                          ref={markerRef}
                        >
                          <Popup>
                            {address ? address.formatedAddress() : fullAddress}
                          </Popup>
                        </Marker>
                      )}

                      {(editable || (address && !latLng)) && (
                        <>
                          <LeafletControlGeocoder
                            address={fullAddress}
                            setMarkerLatLng={handleMarkerPosition}
                          />

                          <MapEvents
                            setMarkerLatLng={handleMarkerPosition}
                          ></MapEvents>
                        </>
                      )}
                    </MapContainer>
                  </Box>
                )}
              </Grid>
              {editable && (
                <Grid item xs={1} sx={{ mt: 1 }}>
                  {street || number || country || state || city ? (
                    !markerLatLng && (
                      <Alert
                        severity={
                          !!errors.lat || !!errors.lon ? "error" : "info"
                        }
                      >
                        <FormattedMessage id="location.click.to.search.message" />
                      </Alert>
                    )
                  ) : (
                    <Alert severity="info">
                      <FormattedMessage id="location.complete.address.to.search.message" />
                    </Alert>
                  )}
                  {editable && markerLatLng && (
                    <Alert severity="info">
                      <FormattedMessage id="location.drag.to.set.marker.message" />
                    </Alert>
                  )}
                </Grid>
              )}
            </Grid>
          </Stack>
          {editable && (street || number || country || state || city) && (
            <Button
              fullWidth
              variant="outlined"
              startIcon={<SearchIcon />}
              data-test="searchAddress"
              onClick={searchAddress}
              {...((!!errors.lat || !!errors.lon) && {
                color: "error",
              })}
            >
              {`${intl.formatMessage({ id: "button.search" })} ${[
                street,
                number,
                city,
                state,
                country,
              ]
                .filter(Boolean)
                .join(", ")}`}
            </Button>
          )}
        </>
      )}
    </>
  );
};

const modalStyle = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  height: 400,
  p: 2,
};

export const LocationModalMap = ({
  address, //Objeto address con todos los campos
  latLng, //Arry de dos elementos con la latitud y la longitud del marker del mapa
  children,
  Component = IconButton,
}) => {
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  return (
    <>
      <Component onClick={handleOpen}>
        {children || <MapIcon></MapIcon>}
      </Component>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Paper sx={modalStyle}>
          <IconButton
            aria-label="delete"
            size="small"
            sx={{
              float: "right",
              position: "absolute",
              top: "-3%",
              right: "-3%",
              backgroundColor: (theme) => theme.palette.secondary.main,
              "&:hover": {
                backgroundColor: (theme) => theme.palette.secondary.light,
              },
            }}
            onClick={handleClose}
          >
            <CloseIcon fontSize="inherit" />
          </IconButton>
          <MapContainer
            style={{ height: "100%", minHeight: "100%" }}
            center={latLng}
            zoom={18}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {latLng && (
              <Marker position={latLng}>
                {address && (
                  <Popup>
                    {address.formatedAddress
                      ? address.formatedAddress()
                      : address}
                  </Popup>
                )}
              </Marker>
            )}
          </MapContainer>
        </Paper>
      </Modal>
    </>
  );
};

export const MapWithMarkers = ({ markers = [] }) => {
  const [map, setMap] = useState(null);
  useEffect(() => {
    var latlngbounds = new L.latLngBounds();
    markers.forEach((marker) => latlngbounds.extend(L.latLng(marker.latLng)));
    map?.fitBounds(latlngbounds);
  }, [map, markers]);
  return (
    <MapContainer
      style={{ height: "100%", minHeight: "100%" }}
      center={[0, 0]}
      zoom={1}
      ref={setMap}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {markers?.map((marker) => {
        return (
          <Marker
            position={marker.latLng}
            {...(marker.icon && {
              icon: L.icon({
                iconUrl: marker.icon,
                shadowUrl: iconShadow,
                iconSize: [25, 41],
                iconAnchor: [12, 41],
              }),
            })}
          >
            <Popup>{marker.description}</Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
};

export const MapWithMarkersAndRadius = ({
  markers = [],
  flyToOtherPlace,
  flyTo,
  lines = [],
  circles = []
}) => {
  const [map, setMap] = useState(null);

  useEffect(() => {
    if (markers?.length > 0) {
      var latlngbounds = new L.latLngBounds();
      markers.forEach((marker) => latlngbounds.extend(L.latLng(marker.latLng)));

      if (flyToOtherPlace) {
        map?.fitBounds(latlngbounds);
        //map?.setMinZoom(map.getZoom()-2);
        map?.setZoom(16);

      }
    }
  }, [map, markers]);

  useEffect(() => {
    if (flyTo) {
      map?.flyTo(flyTo.latLng, flyTo.zoomLevel);
    }
  }, [map, flyTo]);

  return (
    <MapContainer
      style={{ height: "100%", minHeight: "100%" }}
      center={[0, 0]}
      zoom={2}
      ref={setMap}
      scrollWheelZoom={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {markers?.map((marker) => {
        if(marker.show || marker.hasAlarm){

        return (
          <>
            <Marker key={`${marker.id}"-marker"`}
              position={marker.latLng}
              {...(marker.icon && {
                icon: marker.icon,
              })}
            >
              {" "}
              <Popup key={`${marker.id}"-popup"`}>
                {marker.additional_data &&
                  Object.keys(marker.additional_data).map((key) => (
                    <div key={`${marker.id}"-addData"${key}`}>
                      {key}: {marker.additional_data[key]}
                    </div>
                  ))}
              </Popup>
            </Marker>
          </>
        );
      }
      })}

      {circles?.map((circle,index) => {
        if(circle.show || circle.hasAlarm){
        return (<Circle key={circle.id} center={circle.latLng} radius={circle.radius} pathOptions={{ color: circle.color }}>
              <Popup key={`${circle.id}"-popup"`}>
                {circle.additional_data &&
                  Object.keys(circle.additional_data).map((key) => (
                    <div key={`${circle.id}"-addData"${key}`}>
                      {key}: {circle.additional_data[key]}
                    </div>
                  ))}
              </Popup>
        </Circle>);
        }
      })};

      {lines?.map((line, index) => (
          <Polyline key={index} pathOptions={{ color: "grey" }} positions={line} />
        ))}
    </MapContainer>
  );
};
