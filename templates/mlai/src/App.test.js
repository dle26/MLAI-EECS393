import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import { configure, shallow } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import shadows from "@material-ui/core/styles/shadows";
import {Route} from 'react-router-dom';

import RouteWithLayout from './components/RouteWithLayout/RouteWithLayout';

configure({ adapter: new Adapter() });

describe("<App />", () => {
  
  it("render without crashing", () => {
    const div = document.createElement("div");
    ReactDOM.render(<App />, div);
  });

  it("App render 4 router links", () => {
      const wrapper = shallow(<App />);
      expect(wrapper.find(RouteWithLayout)).toHaveLength(1);
      expect(wrapper.find(Route)).toHaveLength(3);
  });
  
});
