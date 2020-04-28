import React, { Component } from "react";
import Avatar from "@material-ui/core/Avatar";
// import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import { Form, Input, Button, Checkbox } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";

import Link from "@material-ui/core/Link";
import Grid from "@material-ui/core/Grid";
import Box from "@material-ui/core/Box";
import DeveloperModeIcon from "@material-ui/icons/DeveloperMode";
import Typography from "@material-ui/core/Typography";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import axios from "axios";
import { Redirect, withRouter, Link as RouterLink } from "react-router-dom";

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {/* {'Copyright © '} */}
      <Link
        color="inherit"
        href="https://github.com/justinphan3110/MLAI-EECS393"
      >
        EECS 393 Spring 2020
      </Link>
    </Typography>
  );
}

const styles = (theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
});

class DevSignIn extends Component {
  constructor(props) {
    super(props);
    this.state = {
      devname: "",
      password: "",
      routeToHome: false,
      routeToSignUp: false,
    };
  }

  dev_login() {
    axios
      .post("http://34.66.1.253:5000/dev/login", {
        devname: this.state.devname,
        password: this.state.password,
      })
      .then((response) => {
        sessionStorage.setItem("devtoken", response.data.devtoken);
        sessionStorage.setItem("Devname", this.state.devname);
        this.setState({ routeToHome: true });
      })
      .catch((error) => {
        console.log("Unable to log in with provided credentials.");
      });
  }

  render() {
    const { classes } = this.props;

    const layout = {
      labelCol: { span: 8 },
      wrapperCol: { span: 16 },
    };
    const tailLayout = {
      wrapperCol: { offset: 8, span: 16 },
    };

    if (this.state.routeToHome) return <Redirect to="/developer" />;

    return (
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <div className={classes.paper}>
          <Avatar className={classes.avatar}>
            <DeveloperModeIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Developer Sign in
          </Typography>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="devname"
            label="devname"
            defaultValue={this.state.devname}
            autoFocus
            onChange={(e) => {
              this.setState({ devname: e.target.value });
            }}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            label="Password"
            type="password"
            id="password"
            defaultValue={this.state.password}
            onChange={(e) => {
              this.setState({ password: e.target.value });
            }}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
            onClick={this.dev_login.bind(this)}
            style={{backgroundColor: "#61646b"}}
          >
            Sign In
          </Button>
          <Grid item xs>
          <RouterLink to="/devSignup">
          Create new Developer Account
          </RouterLink>
          </Grid>
          <Grid item xs>
            <RouterLink to="/signin">Sign in as an user</RouterLink>
          </Grid>
        </div>
        <Box mt={8}>
          <Copyright />
        </Box>
      </Container>
    );
  }
}
DevSignIn.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withRouter(withStyles(styles)(DevSignIn));
