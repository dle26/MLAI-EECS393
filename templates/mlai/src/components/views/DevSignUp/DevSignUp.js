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
import FiberNewIcon from '@material-ui/icons/FiberNew';
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

class DevSignUp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      devname: "",
      password: "",
      firstname: "",
      lastname: "",
      routeToDevSignIn: false,
      devnameExisted: false
    };
  }

  dev_signUp() {
    axios
      .post("http://localhost:5000/dev/register", {
        devname: this.state.devname,
        password: this.state.password,
        firstname: this.state.firstname,
        lastname: this.state.lastname
      })
      .then(response => {
        this.setState({ routeToDevSignIn: true });
      })
      .catch(error => {
        console.log("Dev name existed");
        this.setState({ devnameExisted: true });
      });
  }

  render() {
    const { classes } = this.props;

    if (this.state.routeToDevSignIn) return <Redirect to="/devSignIn" />;

    return (
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <div className={classes.paper}>
          <Avatar className={classes.avatar}>
            <FiberNewIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
         Create New Developer Account
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                id="firstname"
                label="First Name"
                defaultValue={this.state.firstname}
                autoFocus
                onChange={e => {
                  this.setState({ firstname: e.target.value });
                }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                id="lastname"
                label="Last Name"
                defaultValue={this.state.lastname}
                autoFocus
                onChange={e => {
                  this.setState({ lastname: e.target.value });
                }}
              />
            </Grid>
          </Grid>
          {this.state.devnameExisted && (
            <Grid item xs={12}>
              <Typography component="h4" variant="h5" color="secondary">
                devname existed
              </Typography>
            </Grid>
          )}
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="devname"
            label="devname"
            defaultValue={this.state.devname}
            autoFocus
            onChange={e => {
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
            onChange={e => {
              this.setState({ password: e.target.value });
            }}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
            onClick={this.dev_signUp.bind(this)}
          >
            Sign Up
          </Button>
          <Grid container>
            <Grid item>
              <RouterLink to="/devSignin">
                Already have a developer account? Sign In
              </RouterLink>
            </Grid>
          </Grid>
        </div>
        <Box mt={8}>
          <Copyright />
        </Box>
      </Container>
    );
  }
}
DevSignUp.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withRouter(withStyles(styles)(DevSignUp));
