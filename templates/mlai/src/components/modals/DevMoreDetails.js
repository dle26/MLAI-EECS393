import React, { Component } from "react";
import Dialog from "@material-ui/core/Dialog";
import {
  DialogTitle,
  Typography,
  //Grid,
  DialogContent,
} from "@material-ui/core";
import axios from "axios";
import { Form, Input, Button, message } from "antd";
import { UploadOutlined, InboxOutlined } from "@ant-design/icons";

export default class DevMoreDetails extends Component {
  constructor(props) {
    super(props);
    const { files } = this.props;
    this.state = {
      files,
      // more details info
      details: "",
      uploading: false,
    };
  }

  uploadingToggle() {
    this.setState({
      uploading: !this.state.uploading,
    });
  }

  closeModal() {
    this.props.moreDetailsVisible();
    this.props.uploadingToggle();
  }

  upload() {
    const url = "http://localhost:5000/developerfeedback";
    const formData = new FormData();
    console.log("more detail files");
    console.log(this.props.files);
    this.props.files.forEach((file) =>
      formData.append("files[]", file, file.name)
    );

    formData.set("details", this.state.details);
    formData.set("Devname", sessionStorage.getItem("Devname"));

    const headers = {
      headers: { "Content-Type": "multipart/form-data" },
    };

    this.uploadingToggle();

    axios
      .post(url, formData, headers)
      .then((response) => {
        //handle success
        console.log(response);
        this.props.addFile([]);
        this.setState({ success: true });
        alert(".Py file(s) uploaded succesfully");
        this.closeModal();
      })
      .catch((response) => {
        //handle error
        console.log(response);
        alert("File upload failed. Please try again. If persists, report to admin.");
        this.closeModal();
      });

    this.uploadingToggle();
  }

  detailsOnChange = (e) => {
    const { value } = e.target;
    this.setState({ details: value });
  };


  onChange(info) {
    if (info.file.status !== "uploading") {
      console.log(info.file, info.fileList);
    }
    if (info.file.status === "done") {
      message.success(`${info.file.name} file uploaded successfully`);
    } else if (info.file.status === "error") {
      message.error(`${info.file.name} file upload failed.`);
    }
  }

  render() {
    const layout = {
      labelCol: { span: 8 },
      wrapperCol: { span: 50 },
    };

    const props = {
      name: "file",
      action: "https://www.mocky.io/v2/5cc8019d300000980a055e76",
    };

    return (
      <Dialog
        maxWidth={"md"}
        onClose={this.closeModal.bind(this)}
        open={this.props.modalVisible}
      >
        <DialogTitle>
          <Typography color="primary" variant="h2">
            More Details
          </Typography>
        </DialogTitle>

        <DialogContent dividers>
          <Form
            {...layout}
            name="nest-messages"
            // onFinish={onFinish}
          >
            <Form.Item
              name="details"
              label="Details"
              rules={[
                {
                  required: true,
                  message: "Please input your description",
                },
              ]}
            >
              <Input.TextArea
                size="large"
                placeholder="Tell us more details about this code"
                onChange={this.detailsOnChange.bind(this)}
              />
            </Form.Item>




            <Form.Item
              wrapperCol={{
                xs: { span: 24, offset: 0 },
                sm: { span: 16, offset: 8 },
              }}
            >
              <Button
                type="primary"
                onClick={this.upload.bind(this)}
                disabled={this.state.details.length === 0}
                // loading={! this.state.uploading}
                style={{ marginTop: 16 }}
              >
                {!this.state.uploading ? "Submit" : "Submitting..."}
              </Button>
            </Form.Item>
          </Form>
        </DialogContent>
      </Dialog>
    );
  }
}
