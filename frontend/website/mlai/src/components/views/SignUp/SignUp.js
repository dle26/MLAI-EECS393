import React, { Component } from "react";
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import Link from "@material-ui/core/Link";
import Grid from "@material-ui/core/Grid";
import Box from "@material-ui/core/Box";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import Typography from "@material-ui/core/Typography";
import PropTypes from "prop-types";
import { makeStyles, withStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import axios from "axios";
import { connect } from 'react-redux';
import { Redirect, withRouter, Link as RouterLink  } from 'react-router-dom';


import SignIn from "../SignIn/SignIn";

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {"Copyright © "}
      <Link color="inherit" href="https://material-ui.com/">
        Your Website
      </Link>{" "}
      {new Date().getFullYear()}
      {"."}
    </Typography>
  );
}

const styles = theme => ({
  paper: {
    marginTop: theme.spacing(8),
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main
  },
  form: {
    width: "100%", // Fix IE 11 issue.
    marginTop: theme.spacing(3)
  },
  submit: {
    margin: theme.spacing(3, 0, 2)
  }
});

class SignUp extends Component {
  constructor(props) {
    super(props);
    this.state = {
    //   firstName: "",
    //   lastName: "",
    //   username: "",
    //   password: "",

      routeToSignIn: false,
      usernameExisted: false
    };
  }

  signUp() {
    axios
      .post("http://localhost:5000/register", {
        username: this.state.username,
        password: this.state.password,
        firstname: this.state.firstName,
        lastname: this.state.lastName
      })
      .then(response => {
        this.routeToSignIn();
      })
      .catch(error => {
        this.setState({ usernameExisted: true });
      });
  }

  routeToSignIn() {
    console.log("route to sign in");
    this.setState({ routeToSignIn: true });
  }

  render() {
    const { classes } = this.props;

    if (this.state.routeToSignIn) 
        return <Redirect to='/signIn' />;

    return (
      <React.Fragment>
        <Container component="main" maxWidth="xs">
          <CssBaseline />
          <div className={classes.paper}>
            <Avatar className={classes.avatar}>
              <LockOutlinedIcon />
            </Avatar>
            <Typography component="h1" variant="h5">
              Sign up
            </Typography>
            <form className={classes.form} noValidate>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    autoComplete="fname"
                    name="firstName"
                    variant="outlined"
                    required
                    fullWidth
                    id="firstName"
                    label="First Name"
                    defaultValue={this.state.firstName}
                    autoFocus
                    onChange={e => {
                      this.setState({ firstName: e.target.value });
                    }}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    variant="outlined"
                    required
                    fullWidth
                    id="lastName"
                    label="Last Name"
                    name="lastName"
                    autoComplete="lname"
                    // defaultValue={this.state.lastName}
                    onChange={e => {
                      this.setState({ lastName: e.target.value });
                    }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    variant="outlined"
                    margin="normal"
                    required
                    fullWidth
                    id="username"
                    label="username"
                    // defaultValue={this.state.username}
                    autoFocus
                    onChange={e => {
                      this.setState({ username: e.target.value });
                    }}
                  />
                </Grid>
                {this.state.usernameExisted && (
                  <Grid item xs={12}>
                    <Typography component="h4" variant="h5" color="secondary">
                      username exsited
                    </Typography>
                  </Grid>
                )}
                <Grid item xs={12}>
                  <TextField
                    variant="outlined"
                    margin="normal"
                    required
                    fullWidth
                    label="Password"
                    type="password"
                    id="password"
                    defaultValue={this.state.password}
                    onChange={e => {
                      this.setState({ password: e.target.value });
                    }}
                  />
                </Grid>
              </Grid>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
                className={classes.submit}
                onClick={this.signUp.bind(this)}
              >
                Sign Up
              </Button>
              <Grid container justify="flex-end">
                <Grid item>
                  <RouterLink to="/signin">
                  Already have an account? Sign in
                  </RouterLink>
                </Grid>
              </Grid>
            </form>
          </div>
          <Box mt={5}>
            <Copyright />
          </Box>
        </Container>
      </React.Fragment>
    );
  }
}

SignUp.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withRouter((withStyles(styles)(SignUp)));
