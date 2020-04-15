import React from "react";
import { configure, shallow } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import Dashboard from "./Dashboard";
import Container from "@material-ui/core/Container";
import { mount } from 'enzyme'
import { MemoryRouter } from 'react-router-dom'
import { Redirect } from "react-router-dom";


configure({ adapter: new Adapter() });

describe("<Dashboard />", () => {
    let wrapper

    beforeEach(() => {
        wrapper = mount(
          <MemoryRouter>
            <Dashboard />
          </MemoryRouter>
        )
    })

    it("render without token", () => {
        expect(wrapper.find(Redirect)).toHaveLength(1);
    });

    it("render with token", () => {

      sessionStorage.setItem("Token", "123");
      wrapper = mount(
        <MemoryRouter>
          <Dashboard />
        </MemoryRouter>
      )
      console.log("in Test:" + sessionStorage.getItem("Token"));
      expect(wrapper.text()).toContain("Click or drag file to this area to upload")
    })

    afterEach(() => {
      sessionStorage.clear();
    })
})