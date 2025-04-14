import appEn from "./lang/en.json";
import appEs from "./lang/es.json";
import { utilsIntlEn, utilsIntlEs } from "@condor/utils";

export const messages = {
  en: { ...appEn, ...utilsIntlEn },
  es: { ...appEs, ...utilsIntlEs },
};

export const DEFAULT_LOCALE = "en"
