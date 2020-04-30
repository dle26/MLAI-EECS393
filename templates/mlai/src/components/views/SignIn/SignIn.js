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
import WebAssetIcon from "@material-ui/icons/WebAsset";
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

class SignIn extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      password: "",
      routeToHome: false,
      routeToSignUp: false,
    };
  }

  login() {
    axios
      .post("http://34.70.151.69:5000/login", {
        username: this.state.username,
        password: this.state.password,
      })
      .then((response) => {
        sessionStorage.setItem("Token", response.data.token);
        sessionStorage.setItem("Username", this.state.username);
        this.setState({ routeToHome: true });
      })
      .catch((error) => {
        console.log("Unable to log in with provided credentials.");
      });
  }

  componentDidMount() {
    if (sessionStorage.getItem("Token") != null) sessionStorage.clear();
  }

  render() {
    const { classes } = this.props;

    if (this.state.routeToHome) return <Redirect to="/" />;

    return (
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <div className={classes.paper}>
          <Avatar className={classes.avatar}>
            <WebAssetIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="username"
            label="username"
            defaultValue={this.state.username}
            autoFocus
            onChange={(e) => {
              this.setState({ username: e.target.value });
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
            onClick={this.login.bind(this)}
            style={{backgroundColor: "#61646b"}}
          >
            Sign In
          </Button>
          <Grid container>
            <Grid item xs>
              <RouterLink to="/signup">
                Don't have an account? Sign Up
              </RouterLink>
            </Grid>
            <Grid item>
              <RouterLink to="/devSignIn">
                {"Sign in as a developer"}
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
SignIn.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withRouter(withStyles(styles)(SignIn));
