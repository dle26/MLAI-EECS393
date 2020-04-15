import React, { useState, Component } from "react";
import { Link as RouterLink } from "react-router-dom";
import clsx from "clsx";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/styles";
import { AppBar, Toolbar, Badge, Hidden, IconButton } from "@material-ui/core";
import MenuIcon from "@material-ui/icons/Menu";
import NotificationsIcon from "@material-ui/icons/NotificationsOutlined";
import InputIcon from "@material-ui/icons/Input";
import { withStyles } from "@material-ui/core/styles";
import { Redirect } from "react-router-dom";

const styles = (theme) => ({
  root: {
    boxShadow: "none",
    backgroundColor: "#61646b" 
  },
  flexGrow: {
    flexGrow: 1,
  },
  signOutButton: {
    marginLeft: theme.spacing(1),
  },
});

class Topbar extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { classes, className, onSidebarOpen, ...rest } = this.props;
    return (
      <AppBar {...rest} className={clsx(classes.root, className)}>
        <Toolbar>
          <RouterLink to="/">
            <img alt="Logo" src="/images/logos/logo--white.svg" />
          </RouterLink>
          <div className={classes.flexGrow} />
          <Hidden mdDown>
            <IconButton color="inherit">
              <Badge
                // badgeContent={notifications.length}
                color="primary"
                variant="dot"
              >
                <NotificationsIcon />
              </Badge>
            </IconButton>
            <RouterLink to="/signIn" style={{ color: '#FFF' }}>
              <IconButton
                className={classes.signOutButton}
                color="inherit"
              >
                <InputIcon />
              </IconButton>
            </RouterLink>
          </Hidden>
          <Hidden lgUp>
            <IconButton color="inherit" onClick={onSidebarOpen}>
              <MenuIcon />
            </IconButton>
          </Hidden>
        </Toolbar>
      </AppBar>
    );
  }
}

Topbar.propTypes = {
  className: PropTypes.string,
  onSidebarOpen: PropTypes.func,
};

export default withStyles(styles)(Topbar);
