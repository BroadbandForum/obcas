import { Error, NotFound } from "@condor/utils";
import { ThemeProvider, createTheme } from "@mui/material";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { NokiaStyle } from "./NokiaStyle";
import { IntlProvider } from "react-intl";
import { messages, DEFAULT_LOCALE } from "./messages-intl";
import Alarms from "./pages/Alarms";

const defaultTheme = createTheme(NokiaStyle);
const locale = messages.hasOwnProperty(navigator.language.split(/-|_/)[0])
  ? navigator.language.split(/-|_/)[0]
  : DEFAULT_LOCALE;

function App() {
  return (
    <IntlProvider
      messages={messages[locale]}
      locale={locale}
      defaultLocale="en"
    >
      <BrowserRouter>
        <ThemeProvider theme={defaultTheme}>
          <Routes>
            <Route exact path="/">
              <Route index element={<Alarms />} />
              <Route path="alarms-correlation">
                <Route index element={<Alarms />} />
                <Route path="alarms" element={<Alarms />} />
              </Route>
            </Route>
            <Route path="/error" element={<Error />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </ThemeProvider>
      </BrowserRouter>
    </IntlProvider>
  );
}

export default App;
