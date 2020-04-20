import React, { Component } from 'react';
import clsx from 'clsx';
import PropTypes from 'prop-types';
import { Divider, Drawer } from '@material-ui/core';
import DashboardIcon from '@material-ui/icons/Dashboard';
import PeopleIcon from '@material-ui/icons/People';
import ShoppingBasketIcon from '@material-ui/icons/ShoppingBasket';
import TextFieldsIcon from '@material-ui/icons/TextFields';
import ImageIcon from '@material-ui/icons/Image';
import AccountBoxIcon from '@material-ui/icons/AccountBox';
import SettingsIcon from '@material-ui/icons/Settings';
import LockOpenIcon from '@material-ui/icons/LockOpen';
import { makeStyles, withStyles } from "@material-ui/core/styles";

import { Profile, SidebarNav, UpgradePlan } from './components';

const styles = theme => ({
  drawer: {
    width: 240,
    [theme.breakpoints.up('lg')]: {
      marginTop: 64,
      height: 'calc(100% - 64px)'
    }
  },
  root: {
    backgroundColor: theme.palette.white,
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    padding: theme.spacing(2)
  },
  divider: {
    margin: theme.spacing(2, 0)
  },
  nav: {
    marginBottom: theme.spacing(2)
  }
});

class Sidebar extends Component {
  constructor(props){
    super(props)
  }

  render() {
    const { open, variant, onClose, className, ...rest } = this.props;
    const {classes} = this.props;

    const pages = [
      {
        title: 'Upload New Python',
        href: '/developer',
        icon: <DashboardIcon />
      },
      {
        title: 'Technique Rules',
        href: '/developer/rules',
        icon: <ImageIcon />
      }
    ];

    return (
      <Drawer
      anchor="left"
      classes={{ paper: classes.drawer }}
      onClose={onClose}
      open={open}
      variant={variant}
    >
      <div
        {...rest}
        className={clsx(classes.root, className)}
      >
        <Profile />
        <Divider className={classes.divider} />
        <SidebarNav
          className={classes.nav}
          pages={pages}
        />
      </div>
    </Drawer>
    )
  }
}


Sidebar.propTypes = {
  className: PropTypes.string,
  onClose: PropTypes.func,
  open: PropTypes.bool.isRequired,
  variant: PropTypes.string.isRequired
};

export default withStyles(styles)(Sidebar);
