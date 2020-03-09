import React, {Component} from 'react';
import { Link as RouterLink } from 'react-router-dom';
import clsx from 'clsx';
import PropTypes from 'prop-types';
import { Avatar, Typography } from '@material-ui/core';
import { withStyles } from "@material-ui/core/styles";
import axios from "axios";


const styles = theme => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    minHeight: 'fit-content'
  },
  avatar: {
    width: 60,
    height: 60
  },
  name: {
    marginTop: theme.spacing(1)
  }
});

class Profile extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: sessionStorage.getItem("Username")
    }
  }

  componentDidMount() {
    console.log("making call to get use information")
    axios
      .get("http://localhost:5000/userinfo", {
        username: "phanlongboy",
      })
      .then(response => {
        this.setState({firstname: response.data.firstname, lastname: response.data.lastname})
      })
      .catch(error => {
        console.log("Unable to get user info provided credentials.");
      });
  }

  render() {
    const {classes, className, ...rest } = this.props;

    const user = {
      name: 'Shen Zhi',
      avatar: '/images/avatars/avatar_11.png',
      bio: 'Brain Director'
    };

    return (
      <div
        {...rest}
        className={clsx(classes.root, className)}
      >
        <Avatar
          alt="Person"
          className={classes.avatar}
          component={RouterLink}
          src={user.avatar}
          to="/settings"
        />
        <Typography
          className={classes.name}
          variant="h4"
        >
          {user.name}
        </Typography>
        <Typography variant="body2">{user.bio}</Typography>
      </div>
    );

  }
}

Profile.propTypes = {
  className: PropTypes.string
};

export default withStyles(styles)(Profile);
