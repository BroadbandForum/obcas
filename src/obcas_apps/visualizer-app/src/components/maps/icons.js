import L from "leaflet";
import olt from "../../assets/olt.png";
import ont from "../../assets/ont.png";
import splitter from "../../assets/splitter.png";

const commonSize = { iconSize: [60, 60], iconAnchor: [30, 60] };

const markerHtmlStyles = (color, icon) => `
  background-color: ${color};
  width: 2rem;
  height: 2rem;
  display: block;
  left: -1rem;
  top: -1rem;
  position: relative;
  border-radius: 2rem 2rem 0;
  transform: rotate(45deg);
  border: 1px solid #FFFFFF;
  background-image: url('${icon}');
  background-size: contain;
  background-repeat: no-repeat;`;

const icon = (color, icon) =>
  L.divIcon({
    className: "my-custom-pin",
    iconAnchor: [0, 24],
    labelAnchor: [-6, 0],
    popupAnchor: [0, -36],
    html: `<span style="${markerHtmlStyles(color, icon)}" />`,
  });

const oltIcon = (color) => icon(color, olt);

const ontIcon = (color) => icon(color, ont);

const splitterIcon = (color) => icon(color, splitter);

export { oltIcon, ontIcon, splitterIcon };
