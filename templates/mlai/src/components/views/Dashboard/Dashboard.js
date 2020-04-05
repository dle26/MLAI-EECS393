import React, { Component } from "react";
import { Redirect } from "react-router-dom";
import { Grid, Typography } from "@material-ui/core";
import { DropzoneArea } from "material-ui-dropzone";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import axios, { post } from "axios";
import { Upload, message, Button } from "antd";
import { InboxOutlined, UploadOutlined } from "@ant-design/icons";

// import { Button } from "@material-ui/core";

import ArrowDropDownIcon from "@material-ui/icons/ArrowDropDown";
import ArrowRightIcon from "@material-ui/icons/ArrowRight";
import MoreDetails from "../../modals/MoreDetails";

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

class Dashboard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      token: sessionStorage.getItem("Token"),
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
    console.log("token: " + this.state.token);
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

    if (this.state.token == null) return <Redirect to="/signIn" />;

    return (
      <Grid container spacing={6}>
        <Grid item lg={8} md={12} xl={9} xs={12}>
          <Dragger
            action={"https://www.mocky.io/v2/5cc8019d300000980a055e76"}
            multiple={true}
            name={"file"}
            onChange={this.onChange.bind(this)}
          >
            <p className="ant-upload-drag-icon">
              <InboxOutlined />
            </p>
            <p className="ant-upload-text">
              Click or drag file to this area to upload
            </p>
            <p className="ant-upload-hint">
              Support for a single or bulk upload. Strictly prohibit from
              uploading company data or other band files
            </p>
          </Dragger>
        </Grid>

        <Grid item lg={8} md={12} xl={9} xs={12}>
          <Typography variant="h4" gutterBottom>
            Or
          </Typography>
        </Grid>

        <Grid item lg={8} md={12} xl={9} xs={12}>
          <Upload
            action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
            directory
            onChange={this.onChange.bind(this)}
          >
            <Button>
              <UploadOutlined /> Upload Directory
            </Button>
          </Upload>
        </Grid>

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

          <MoreDetails
            modalVisible={this.state.moreDetailsVisible}
            moreDetailsVisible={this.moreDetailsVisible.bind(this)}
            uploadingToggle={this.uploadingToggle.bind(this)}
            addFile={this.addFile.bind(this)}
            files={this.state.files}
            step={1}
          />
        </Grid>
      </Grid>
    );
  }
}

Dashboard.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(Dashboard);
