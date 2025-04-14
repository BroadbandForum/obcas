
import { useConfig } from "@condor/utils";

const CommonDataService = () => {
  const config = useConfig();

  const getServices = () => {
    return new Promise((resolve, reject) => {
      resolve(config.REACT_APP_SERVICES.split(","));
    });
  };

  const getInstallers = () => {
    return new Promise((resolve, reject) => {
      resolve(config.REACT_APP_INSTALLERS.split(","));
    });
  };

  const getLocationTypes = () => {
    return new Promise((resolve, reject) => {
      resolve(config.REACT_APP_LOCATION_TYPES.split(","));
    });
  };

  return {
    getServices: getServices,
    getInstallers: getInstallers,
    getLocationTypes: getLocationTypes,
  };
};

export default CommonDataService;
