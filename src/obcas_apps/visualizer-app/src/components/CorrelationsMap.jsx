import { MapWithMarkersAndRadius } from "./maps/Location";

const CorrelationsMap = (props) => {
  const { sites, lines, circles, flyToOtherPlace } = props;

  return <MapWithMarkersAndRadius markers={sites} lines={lines} circles={circles} flyToOtherPlace={flyToOtherPlace}/>;
};

export default CorrelationsMap;
