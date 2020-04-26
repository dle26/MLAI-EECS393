import React, { Component } from "react";
import ReactGA from 'react-ga'
import {Switch, BrowserRouter as Router, Route} from 'react-router-dom';
import { Main as MainLayout, Minimal as MinimalLayout, DevLay as DevLayout} from './components/layouts';
import {
  Dashboard as DashboardView,
  SignIn as SignInView,
  SignUp as SignUpView,
  DevSignIn as DevSignInView,
  DevSignUp as DevSignUpView,
  Developer as DeveloperView,
  DevRules as DevRulesView
} from './components/views';

import RouteWithLayout from './components/RouteWithLayout/RouteWithLayout'

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
            <RouteWithLayout key="developer" path="/developer" exact layout={DevLayout} strict component={DeveloperView} />
            <RouteWithLayout key="devRules" path="/developer/rules" exact layout={DevLayout} strict component={DevRulesView} />
            <Route key="devSignUp" path="/devSignUp" exact component={DevSignUpView} />
          </Switch>
        </div>
      </Router>
      // <Test />
    );
  }
}
