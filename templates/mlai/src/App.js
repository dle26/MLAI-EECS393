import React, { Component } from "react";
import ReactGA from 'react-ga'
import {Switch, BrowserRouter as Router, Route} from 'react-router-dom';
import { Main as MainLayout, Minimal as MinimalLayout } from './components/layouts';
import {
  Dashboard as DashboardView,
  SignIn as SignInView,
  SignUp as SignUpView,
  DevSignIn as DevSignInView
} from './components/views';

import RouteWithLayout from './components/RouteWithLayout/RouteWithLayout'
import Test from './Test'

export default class App extends Component {
  render() {
    return (
      <Router>
        <div className="App Router">
          <Switch>
            <RouteWithLayout key="home" path="/" exact layout={MainLayout} strict component={DashboardView} />
            <Route key="signUp" path="/signUp" exact component={SignUpView} />
            <Route key="signIn" path="/signIn" exact component={SignInView} />
            <Route key="devSignIn" path="/devSignIn" exact component={DevSignInView} />
          </Switch>
        </div>
      </Router>
      // <Test />
    );
  }
}
