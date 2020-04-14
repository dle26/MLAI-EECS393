import React from "react";
import { configure, shallow } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import SignUp from "./SignUp";
import Container from "@material-ui/core/Container";
import { mount } from 'enzyme'
import { MemoryRouter } from 'react-router-dom'


configure({ adapter: new Adapter() });

describe("<SignUp />", () => {
    let wrapper

    beforeEach(() => {
        wrapper = mount(
          <MemoryRouter>
            <SignUp />
          </MemoryRouter>
        )
    })

    it("render without crashing", () => {
        expect(wrapper.find(Container)).toHaveLength(1);
    });

    it("Contains Sign Up", () => {
        expect(wrapper.text()).toContain('Sign Up');
    })
})