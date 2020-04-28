import React, { Component, useState } from "react";
import { Redirect } from "react-router-dom";
import { Grid, Typography } from "@material-ui/core";
//import { DropzoneArea } from "material-ui-dropzone";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
//import axios, { post } from "axios";
import { Upload, message, Button } from "antd";
import { InboxOutlined} from "@ant-design/icons";

//import { Button } from "@material-ui/core";
import DevMoreDetails from "../../modals/DevMoreDetails";

const styles = theme => ({
  root: {},
  chartContainer: {
    height: 400,
    position: "relative"
  },
  actions: {
    justifyContent: "flex-end"
  }
});


class Developer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      devtoken: sessionStorage.getItem("devtoken"),
      files: [],
      uploading: false,
      moreDetailsVisible: false
    };
  }

  moreDetailsVisible() {
    this.setState({
      moreDetailsVisible: ! this.state.moreDetailsVisible
    });
  }

  uploadingToggle() {
    this.setState({
      uploading: ! this.state.uploading
    });
  }

  componentDidMount() {
    console.log("devtoken: " + this.state.devtoken);
  }

  addFile(file) {
    this.setState({
      files: file
    });
  }

  onChange(info) {
    const { status } = info.file;

    if (status !== "uploading") {
      console.log(info.file.originFileObj);
    }
    if (status === "removed") {
      console.log("file removed");

      for (var i = 0; i < this.state.files.length; i++) {
        if(this.state.files[i] === info.file.originFileObj)
          delete this.state.files[i];
      }
      //this.removeFile([...this.state.files, info.file.originFileObj]);
    }
    if (status === "done") {
      message.success(`${info.file.name} file uploaded successfully.`);

      this.addFile([...this.state.files, info.file.originFileObj]);

    } else if (status === "error") {
      message.error(`${info.file.name} file upload failed.`);
    }
  }

  upload() {
    this.uploadingToggle();

    this.moreDetailsVisible();

    this.uploadingToggle();
  }

  render() {
    const { Dragger } = Upload;

    const dummyRequest = ({ file, onSuccess }) => {
      setTimeout(() => {
        onSuccess("ok");
      }, 0);
    };


    if (sessionStorage.getItem("devtoken") == null) return <Redirect to="/devSignIn" />;


    return (
      <Grid container spacing={6}>
        <Grid item lg={12} md={12} xl={9} xs={12}>
          <Dragger
            customRequest={dummyRequest}
            multiple={true}
            name={"file"}
            accept={".py"}
            onChange={this.onChange.bind(this)}
          >
            <p className="ant-upload-drag-icon">
              <InboxOutlined />
            </p>
            <p className="ant-upload-text">
              Click or drag file to this area to upload
            </p>
            <p className="ant-upload-hint">
              Please upload your .py files here.
            </p>
          </Dragger>
          <Grid item lg={8} md={12} xl={9} xs={12}>
            <Button
              type="primary"
              onClick={this.upload.bind(this)}
              disabled={this.state.files.length === 0}
              loading={this.state.uploading}
              style={{ marginTop: 16 }}
            >
              {this.state.uploading ? "Uploading" : "Start Upload"}
            </Button>

            <DevMoreDetails
              modalVisible={this.state.moreDetailsVisible}
              moreDetailsVisible={this.moreDetailsVisible.bind(this)}
              uploadingToggle={this.uploadingToggle.bind(this)}
              addFile={this.addFile.bind(this)}
              files={this.state.files}
              step={1}
            />
          </Grid>
        </Grid>
      </Grid>
    );
  }
}

Developer.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(Developer);
