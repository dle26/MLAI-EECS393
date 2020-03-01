import React, { Component } from 'react'
import { Redirect } from 'react-router-dom';

export default class componentName extends Component {

    constructor(props) {
        super(props);
        this.state = {
            token: sessionStorage.getItem("Token"),
        }
    }

    componentDidMount() {
        console.log("token: " + this.state.token);
    }

    render() {

        if(this.state.token == null)
            return <Redirect to='/signIn'/>;

        return (
            <div>
                Hello World
            </div>
        )
    }
}
