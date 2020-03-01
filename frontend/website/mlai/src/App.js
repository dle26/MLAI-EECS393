import React, { Component } from "react";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import Dashboard from "./components/Dashboard";
import ReactGA from 'react-ga'
import {Switch, BrowserRouter as Router, Route} from 'react-router-dom';

export default class App extends Component {
  render() {
    return (
      <Router>
        <div className="App Router">
          <Switch>
            <Route key="home" path="/" exact strict component={Dashboard} />\
            <Route key="signUp" path="/signUp" exact component={SignUp} />
            <Route key="signIn" path="/signIn" exact component={SignIn} />
            
          </Switch>
        </div>
      </Router>
    );
  }
}
