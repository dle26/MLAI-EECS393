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
import MoreDetails from "../../modals/MoreDetails";
import ResultModal from "../../modals/ResultModal";

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
      moreDetailsVisible: false,

      //result
      resultVisible: false,
      result: {},
    };
  }

  moreDetailsVisible() {
    this.setState({
      moreDetailsVisible: ! this.state.moreDetailsVisible
    });
  }

  resultModalVisible() {
    this.setState({
      resultVisible: ! this.state.resultVisible
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

  setResult(r) {
    this.setState({
      result: r
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

    const dummyRequest = ({ file, onSuccess }) => {
      setTimeout(() => {
        onSuccess("ok");
      }, 0);
    };


    if (sessionStorage.getItem("Token") == null) return <Redirect to="/signIn" />;

    return (
      <Grid container spacing={6}>
        <Grid item lg={12} md={12} xl={9} xs={12} alignItems={'stretch'}>
          <Dragger
            customRequest={dummyRequest}
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
              Support for a single or bulk upload. Strictly prohibited from
              uploading company data or other banned files
            </p>
          </Dragger>
        </Grid>

        <Grid item lg={8} md={12} xl={9} xs={12} alignItems={'stretch'}>
          <Typography variant="h4" gutterBottom>
              Or, if you prefer to upload an entire directory, go below.
          </Typography>
        </Grid>

        <Grid item lg={8} md={12} xl={9} xs={12}>
          <Upload
            customRequest={dummyRequest}
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
            resultModalVisible={this.resultModalVisible.bind(this)}
            setResult={this.setResult.bind(this)}
          />

          <ResultModal
            modalVisible={this.state.resultVisible}
            resultModalVisible={this.resultModalVisible.bind(this)}
            result={this.state.result}
            files={this.state.files}
            addFile={this.addFile.bind(this)}
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
