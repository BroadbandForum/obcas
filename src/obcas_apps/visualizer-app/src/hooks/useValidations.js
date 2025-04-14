import { useIntl } from "react-intl";

export default function useValidators() {
  const intl = useIntl();

  const validators = {
    required: {
      value: true,
      message: intl.formatMessage({ id: "error.required" }),
    },
    numbers: {
      value: /^[0-9]+$/,
      message: intl.formatMessage({ id: "error.onlyNumbers" }),
    },
    email: {
      value:
        /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
      message: intl.formatMessage({ id: "error.invalidEmail" }),
    },
  };

  return validators;
}
