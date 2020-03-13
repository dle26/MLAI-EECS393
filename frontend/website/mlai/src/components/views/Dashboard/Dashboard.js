import React, { Component } from "react";
import { Redirect } from "react-router-dom";
import { Grid } from "@material-ui/core";
import { DropzoneArea } from "material-ui-dropzone";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import axios, { post } from "axios";

import { Button } from "@material-ui/core";
import ArrowDropDownIcon from "@material-ui/icons/ArrowDropDown";
import ArrowRightIcon from "@material-ui/icons/ArrowRight";

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
      token: sessionStorage.getItem("Token")
    };
  }

  componentDidMount() {
    console.log("token: " + this.state.token);
  }

  addFiles(file) {
    const url = "http://localhost:5000/upload";

    const formData = new FormData();
    
    console.warn("data: ", file[0]);

    formData.append("file", file[0]);
        
    const config = {
      headers: {
        "content-type": "multipart/form-data"
      }
    };

    axios
      .post(url, formData, config)
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.log(error);
      });
  }

  upload() {
    axios.post("http://localhost:5000/upload", {
      username: sessionStorage.getItem("Username"),
      files: this.state.files
    }).then;
  }
  render() {
    const { classes } = this.props;

    if (this.state.token == null) return <Redirect to="/signIn" />;

    return (
      <div>
        <Grid container spacing={4}>
          <DropzoneArea
            className="my_drop"
            style={{ margin: 0 }}
            dropzoneClass={"DropzoneArea"}
            showPreviews={false}
            accept=".csv"
            showAlerts={true}
            acceptedFiles={[
              "application/vnd.ms-excel",
              "text/csv",
              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
              "xls",
              "text/x-csv",
              "application/csv",
              "application/x-csv",
              "text/comma-separated-values",
              "text/x-comma-separated-values",
              "text/tab-separated-values",
              ".csv"
            ]}
            filesLimit={1}
            dropzoneText={"Drop file here, or click to select file"}
            cancelButtonText={true}
            showPreviewsInDropzone={true}
            onChange={this.addFiles.bind(this)}
            showFileNames={true}
            showPreviewsInDropzone={true}
            maxFileSize={10000000}
          />

          <Grid item lg={8} md={12} xl={9} xs={12}>
            <Button
              onClick={this.upload.bind(this)}
              variant="contained"
              color="primary"
            >
              Upload
            </Button>
          </Grid>
        </Grid>
      </div>
    );
  }
}

Dashboard.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(Dashboard);
