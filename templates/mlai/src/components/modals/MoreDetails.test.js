import React from "react";
import { configure, shallow } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import MoreDetails from "./MoreDetails";


configure({ adapter: new Adapter() });

describe("<MoreDetails />", () => {
    let wrapper

    beforeEach(() => {
        wrapper = shallow(<MoreDetails/>)
    })

    it("render with visible Modal", () => {
        wrapper.setProps({modalVisible: true})
        expect(wrapper.text()).toContain("More Details");
    });

    it("render without visiblle Modal", () => {
        wrapper.setProps({modalVisible: false})
        expect(wrapper.contains(<MoreDetails />)).toBe(false);
    })
})