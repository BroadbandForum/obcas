import { useConfig } from "@condor/utils";
//import data from "../assets/countries+states+cities.json";
import provincias from "../assets/provincias.json";
import localidades from "../assets/localidades.json";

const LocationService = () => {
  const Config = useConfig();

  const getCountries = () => {
    return new Promise((resolve, reject) => {
      /*resolve(
        data.map((country) => ({
          name: country.name,
          lat: country.latitude,
          lng: country.longitude,
        }))
      );*/
      resolve([
        { name: "Argentina", lat: "-34.00000000", lng: "-64.00000000" },
      ]);
    });
  };

  const getStates = (countryName) => {
    return new Promise((resolve, reject) => {
      /*resolve(
        data
          .find((country) => country.name === countryName)
          .states.map((state) => ({
            name: state.name,
            lat: state.latitude,
            lng: state.longitude,
          }))
      );*/
      resolve(
        provincias.map((state) => ({
          name: state.nombre,
          lat: state.centroide.lat,
          lng: state.centroide.lon,
        })).sort(sortByName)
      );
    });
  };

  const sortByName = (a, b) => {
    if (a.name > b.name) {
      return 1;
    }
    if (a.name < b.name) {
      return -1;
    }
    // a must be equal to b
    return 0;
  };

  const getCities = (countryName, stateName) => {
    return new Promise((resolve, reject) => {
      /*resolve(
        data
          .find((country) => country.name === countryName)
          .states.find((state) => state.name == stateName)
          .cities.map((city) => ({
            name: city.name,
            lat: city.latitude,
            lng: city.longitude,
          }))
      );*/
      resolve(
        localidades
          .filter((city) => city.provincia.nombre == stateName)
          .map((city) => ({
            name: city.nombre,
            lat: city.centroide.lat,
            lng: city.centroide.lon,
            municipality: city.municipio.nombre,
          })).sort(sortByName)
      );
    });
  };

  return {
    getCountries: getCountries,
    getStates: getStates,
    getCities: getCities,
  };
};

export default LocationService;
