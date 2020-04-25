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

    if(this.state.username != null) {
      axios
      .post("http://34.67.45.99:5000/userinfo", {
        "username": this.state.username
      })
      .then(response => {
        this.setState({firstname: response.data.firstname, lastname: response.data.lastname})
      })
      .catch(error => {
        console.log("Unable to get user info provided credentials.");
      });
    }

  }

  render() {
    const {classes, className, ...rest } = this.props;

    const user = {
      name: this.state.firstname + " " + this.state.lastname,
      avatar: '/images/avatars/avatar_11.png',
    };

    return (
      <div
        {...rest}
        className={clsx(classes.root, className)}
      >
        <Typography
          className={classes.name}
          variant="h4"
        >
          {user.name}
        </Typography>
      </div>
    );

  }
}

Profile.propTypes = {
  className: PropTypes.string
};

export default withStyles(styles)(Profile);
