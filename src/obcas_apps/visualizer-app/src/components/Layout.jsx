import {
  Box,
  Button,
  Container,
  CssBaseline,
  Divider,
  IconButton,
  Link,
  Menu,
  MenuItem,
  Stack,
  Toolbar,
  Tooltip,
  Typography,
} from "@mui/material";
import condorLogoGrey from "../assets/logo_condor_gray.png";
import condorLogoColor from "../assets/bbflogo.png";
import { AccountCircle } from "@mui/icons-material";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import InfoIcon from "@mui/icons-material/Info";
import { useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { FormattedMessage } from "react-intl";
import { useConfig } from "@condor/utils";
import ReactTimeago from "react-timeago";
import MenuIcon from "@mui/icons-material/Menu";

const Layout = ({ children, title, actions = [], sections, helText }) => {
  const config = useConfig();
  const [anchorEl, setAnchorEl] = useState(null);
  const location = useLocation();

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
      }}
    >
      <CssBaseline />

      <Toolbar component="header">
        <Link href={config.REACT_APP_BBF_URL}>
          <img src={condorLogoColor} width="160px" alt=""></img>
        </Link>
        <Divider orientation="vertical" flexItem sx={{ 'marginLeft': '16px' }}/>
        <Typography variant="h6" sx={{ ml: 1, flexGrow: { xs: 1, sm: 0 } }}>
          <FormattedMessage id="home.page.portal.title" />
        </Typography>

        <Stack
          direction="row"
          spacing={1}
          sx={{ ml: 1, flexGrow: 1, display: { xs: "none", sm: "flex" } }}
        >

        </Stack>

        <Button
          color="inherit"
          onClick={handleMenu}
          startIcon={<AccountCircle></AccountCircle>}
          endIcon={<ArrowDropDownIcon></ArrowDropDownIcon>}
          sx={{ display: { xs: "none", sm: "flex" } }}
        >
          ADMIN
        </Button>
        <IconButton
          onClick={handleMenu}
          sx={{ display: { xs: "flex", sm: "none" } }}
        >
          <MenuIcon />
        </IconButton>
        <Menu
          id="menu-appbar"
          anchorEl={anchorEl}
          keepMounted
          open={Boolean(anchorEl)}
          onClose={handleClose}
        >
          <Divider sx={{ display: { xs: "flex", sm: "none" } }} />
          <MenuItem onClick={handleClose}>
            <FormattedMessage id="button.signout" />
          </MenuItem>
        </Menu>
      </Toolbar>

      <Divider />

      <Container
        maxWidth="100%"
        sx={{
          display: "flex",
          flexDirection: "row",
          alignItems: "center",
          ...(!sections && { py: 2 }),
        }}
      >
        <Box sx={{ flexGrow: 1 }}>{sections}</Box>
        <Typography variant="caption">
          <FormattedMessage id="title.last.updated" />
          <ReactTimeago date={new Date()} minPeriod={60} />
        </Typography>
      </Container>

      <Container
        component="main"
        maxWidth="100%"
        sx={{
          flexGrow: 1,
          pr: 2,
        }}
      >
        <Box
          sx={{
            display: "flex",
            flexDirection: "row",
            alignItems: "start",
          }}
        >
          {children}
        </Box>
      </Container>
      <Box component="footer">
        <Container
          maxWidth="100%"
          sx={{
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            py: 1,
          }}
        >
          <Box
            component="a"
            href={config.REACT_APP_CONDOR_URL}
            target="_blank"
            sx={{
              flexGrow: 1,
              display: "flex",
              flexDirection: "row",
              alignItems: "center",
              color: "inherit",
              textDecoration: "inherit",
            }}
          >
            <Typography variant="body1" component="span">
              Powered by{" "}
            </Typography>
            <img src={condorLogoGrey} style={{filter:"grayscale(100%)"}} height="40px" alt=""></img>
          </Box>
          <Typography variant="body1">v1.0</Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default Layout;
