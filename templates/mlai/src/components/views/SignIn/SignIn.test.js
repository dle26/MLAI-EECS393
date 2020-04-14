import React from "react";
import { configure, shallow } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import SignIn from "./SignIn";
import Container from "@material-ui/core/Container";
import { mount } from 'enzyme'
import { MemoryRouter } from 'react-router-dom'


configure({ adapter: new Adapter() });

describe("<SignIn />", () => {
    let wrapper

    beforeEach(() => {
        wrapper = mount(
          <MemoryRouter>
            <SignIn />
          </MemoryRouter>
        )
    })

    it("render without crashing", () => {
        expect(wrapper.find(Container)).toHaveLength(1);
    });

    it("Contains Sign In", () => {
        expect(wrapper.text()).toContain('Sign In');
    })

    it("Contains Session Storage", () => {
        sessionStorage.setItem("Token", "123");
        expect(wrapper.text()).toContain('Sign In');
        sessionStorage.clear();
    })
})