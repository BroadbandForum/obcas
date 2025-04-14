export const NokiaStyle = {
  palette: {
    primary: {
      light: "#4167a7",
      main: "#124191",
      dark: "#0c2d65",
    },
    secondary: {
      light: "#8b8b8b",
      main: "#6e6e6e",
      dark: "#4d4d4d",
    },
  },
  components: {
    // Name of the component
    MuiTableCell: {
      styleOverrides: {
        // Name of the slot
        head: ({ theme }) => ({
          // Some CSS
          //backgroundColor: theme.palette.primary.light,
          color: "black",
          fontWeight: "bold",
        }),
      },
    },
    MuiContainer: {
      styleOverrides: {
        root: ({ theme }) => ({
          backgroundColor:
            theme.palette.mode === "light"
              ? theme.palette.grey[100]
              : theme.palette.grey[900],
        }),
      },
    },
    MuiTypography: {
      styleOverrides: {
        root: ({ ownerState }) => ({
          ...(ownerState.variant === "h6" && {
            fontSize: "16px",
            fontWeight: "bold",
          }),
        }),
      },
    },
  },
};
