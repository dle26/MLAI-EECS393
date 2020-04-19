import React, { Component, useState } from "react";
import { Redirect } from "react-router-dom";
import { Grid, Typography } from "@material-ui/core";
import { DropzoneArea } from "material-ui-dropzone";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import axios, { post } from "axios";
import { Upload, message, Button } from "antd";
import { InboxOutlined, UploadOutlined } from "@ant-design/icons";
import clsx from 'clsx';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import { useMediaQuery } from '@material-ui/core';

// import { Button } from "@material-ui/core";

import ArrowDropDownIcon from "@material-ui/icons/ArrowDropDown";
import ArrowRightIcon from "@material-ui/icons/ArrowRight";
import DevMoreDetails from "../../modals/DevMoreDetails";
import { Topbar } from "../../layouts/Main/components/Sidebar";

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

    const dummyRequest = ({ file, onSuccess }) => {
      setTimeout(() => {
        onSuccess("ok");
      }, 0);
    };


    if (sessionStorage.getItem("Token") == null) return <Redirect to="/devSignIn" />;


    return (
 <Grid> <h1> Guidelines for Submitting Source Code to MLAI platform (as of April 5th 2020)</h1>
<h3> Please use these guidelines if you plan to submit your machine learning project for use on the MLAI platform</h3>

<h2> General Guidelines: </h2>

<h4> <ol>
<li>All source code must be written in Python 3 </li>

<li>You must include all description of your project, proposed applications, and a README with package requirements </li>

<li>All projects must be relevant to machine learning. MLAI, inc. reserves the right to reject any submitted projects </li>
</ol>
</h4>



<h2>Specific Formatting Guidelines:</h2>

<h4> <ol>
<li>All source code needed to run your technique must be in a single Python file with a name that uniquely identifies your project (i.e. VGG16_CNN)</li>

<li>You must implement all the functions in the Technique Abstract Class inside a class object corresponding to the name of your technique (you may include as many additional utility functions as are needed)</li>

<li>You must ensure that the data will be automatically formatted/structured in a manner that will not crash your algorithm. The data will be input as a multidimensional numpy array, where each index corresponds to a sample. Original dimensions of each sample are also available (Appendix C).</li>

<li>Please reference Appendix B for a specific example of acceptable MLAI source code </li></ol> </h4>


<h3>

Appendix A:</h3> <h4>Technique Abstract Class (All techniques in the MLAI package are subclasses of Technique </h4>

<h3>Appendix B: </h3><h4>Example of acceptable source code for the SVM algorithm </h4>

<h3>Appendix C:</h3><h4> Documentation for MLAI Data class </h4>
<h1> Please note this page is a work in progress. </h1>

 </Grid>



    );
  }
}

Developer.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(Developer);
