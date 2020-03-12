import React, { Component } from "react";
import { Redirect } from "react-router-dom";
import { DropzoneArea } from "material-ui-dropzone";

export default class componentName extends Component {
  constructor(props) {
    super(props);
    this.state = {
      token: sessionStorage.getItem("Token"),
      files: []
    };
  }

  componentDidMount() {
    console.log("token: " + this.state.token);
  }

  uploadFiles(files) {
      this.setState({
          files: files
      })
  }

  render() {
    if (this.state.token == null) return <Redirect to="/signIn" />;

    return (
      <div>
        <DropzoneArea
          acceptedFiles={["image/*", "video/*", "application/*"]}
          onChange={this.uploadFiles.bind(this)}
          showFileNames
          dropzoneText="Drop the file here"
          showAlerts={false}
          filesLimit={20}
        />
      </div>
    );
  }
}
