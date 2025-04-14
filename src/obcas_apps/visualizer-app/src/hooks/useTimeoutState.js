import { useConfig } from "@condor/utils";
import { useCallback, useState } from "react";

export const useTimeoutState = (
  defaultValue,
  defaultOpts = { timeout: 3000 }
) => {
  const [state, _setState] = useState(defaultValue);
  const [currentTimeoutId, setCurrentTimeoutId] = useState(null);
  const config = useConfig();

  if (config && config.REACT_APP_TIME_MESSAGES) {
    defaultOpts.timeout = parseInt(config.REACT_APP_TIME_MESSAGES);
  }

  const setState = useCallback(
    (value, opts = defaultOpts) => {
      if (currentTimeoutId != null) {
        clearTimeout(currentTimeoutId);
      }

      _setState(value);

      const id = setTimeout(() => _setState(defaultValue), opts.timeout);
      setCurrentTimeoutId(id);
    },
    [currentTimeoutId, defaultValue]
  );
  return [state, setState];
};
