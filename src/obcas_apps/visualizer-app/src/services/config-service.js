import { readRemoteFile } from "react-papaparse";

const configURL =
  "https://docs.google.com/spreadsheets/d/e/2PACX-1vSXMSzAPPIWcP3oKGM8YNdXAKP4mevt_Ma_khmtPgb6Ll2A6sskHcgqq881hDf0kVCcga5laKpWThXF/pub?gid=852269341&single=true&output=csv";

export const getConfig = () => {
  return new Promise((resolve, reject) => {
    readRemoteFile(configURL, {
      header: true,
      download: true,
      complete: (results) => resolve(results.data[0]),
      error: (error) => {
        reject(error);
      },
    });
  });
};
