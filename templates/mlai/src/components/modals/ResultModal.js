import React, { Component } from "react";
import { Modal } from "antd";
import ListSubheader from "@material-ui/core/ListSubheader";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import Collapse from "@material-ui/core/Collapse";
import StarIcon from "@material-ui/icons/Star";
import CastForEducationIcon from "@material-ui/icons/CastForEducation";
import TimelineIcon from "@material-ui/icons/Timeline";
import SendIcon from "@material-ui/icons/Send";
import ExpandLess from "@material-ui/icons/ExpandLess";
import ExpandMore from "@material-ui/icons/ExpandMore";
import LinkIcon from "@material-ui/icons/Link";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import Link from "@material-ui/core/Link";
import DialpadIcon from "@material-ui/icons/Dialpad";
import DragHandleIcon from "@material-ui/icons/DragHandle";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';

const styles = (theme) => ({
  root: {
    width: "100%",
    backgroundColor: theme.palette.background.paper,
  },
  nested: {
    paddingLeft: theme.spacing(4),
  },

  collapse: {
    width: "100%",
    // paddingLeft: "10%",
  },
});

class ResultModal extends Component {
  constructor(props) {
    super(props);
    const { files, result } = this.props;
    this.state = {
      files,
      result,
      educationLinksOpen: false,
      techniquesOpen: false,
    };
  }

  closeModal() {
    this.props.resultModalVisible();
  }

  render() {
    if (!this.props.modalVisible) return <React.Fragment> </React.Fragment>;
    if( !this.props.result) return <React.Fragment></React.Fragment>;
    
    const {labels} = this.props.result
    const { classes } = this.props;
    const {
      names,
      samples,
      results,
      accuracy,
      f1_score,
      feature_importances,
      confusion_matrix,
      ch_score,
      silhouette
    } = this.props.result.techniques;

    var index = -1;

    console.log(labels)

    let techniques = names.map((t) => {
      index = index + 1;
      return (
        <ListItem key={t + "title"} button>
          <ListItemIcon>
            <DragHandleIcon />
          </ListItemIcon>
          <ListItemText primary={t} />
          <List>
            <ListItem key={t + " samples"}>
              <ListItemText
                primary={"Sample"}
                secondary={"[" + samples[index].toString() + "]"}
              />
            </ListItem>

            <ListItem key={t + " results"}>
              <ListItemText
                primary={"Result"}
                secondary={"[" + results[index].toString() + "]"}
              />
            </ListItem>

            {accuracy ? (
              <ListItem key={t + " accuracy"}>
                <ListItemText
                  primary={"Accuracy"}
                  secondary={accuracy[index]}
                />
                <ListItemSecondaryAction>

                </ListItemSecondaryAction>
              </ListItem>
            ) : null}

            {f1_score ? (
              <ListItem key={t + " f1_score"}>
                <ListItemText
                  primary={"F1 Score"}
                  secondary={f1_score[index]}
                />
              </ListItem>
            ) : null}

            {ch_score ? (
              <ListItem key={t + " ch_score"}>
                <ListItemText
                  primary={"CH Score"}
                  secondary={ch_score[index]}
                />
              </ListItem>
            ) : null}

            {silhouette ? (
              <ListItem key={t + " silhouette"}>
              <ListItemText
                primary={"Silhouette"}
                secondary={silhouette[index]}
              />
            </ListItem>
          ) : null}


            <ListItem key={t + " feature_importances"}>
              <ListItemText
                primary={"Feature Importances"}
                secondary={"[" + feature_importances[index].toString() + "]"}
              />
            </ListItem>

            <ListItem key={t + "table"}>
              <ListItemText
                primary={"Confusion Matrix"}
                secondary={
                  <TableContainer>
                    <Table size="small" aria-label="table">
                    <TableHead>
                      <TableRow>
                        {labels.map((row) => (
                          <TableCell align="right">{row}</TableCell>
                        ))}
                      </TableRow>
                    </TableHead>


                      <TableBody>
                        {confusion_matrix[index].map((row) => (
                          <TableRow key={Math.random()}>
                            {row.map((r) => {
                              return <TableCell align="right">{r}</TableCell>;
                            })}
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                }
              />
            </ListItem>
          </List>
        </ListItem>
      );
    });

    let educationLinks = this.props.result["education"].map((c) => {
      return (
        <Link href={c} target="_blank">
          <ListItem key={c} button className={classes.nested}>
            <ListItemIcon>
              <LinkIcon />
            </ListItemIcon>
            <ListItemText primary={c} />
          </ListItem>
        </Link>
      );
    });

    return (
      <Modal
        title="Result"
        visible={this.props.modalVisible}
        onOk={this.closeModal.bind(this)}
        onCancel={this.closeModal.bind(this)}
        width={1200}
      >
        <List
          component="nav"
          aria-labelledby="result after running MLAI"
          subheader={
            <ListSubheader component="div" id="nested-list-subheader">
              Result after running MLAI
            </ListSubheader>
          }
          className={classes.root}
        >
          <ListItem key={"best"} button>
            <ListItemIcon>
              <StarIcon />
            </ListItemIcon>
            <ListItemText
              primary="Best"
              secondary={this.props.result["best"]}
            />
          </ListItem>
          <ListItem key={"Analysis Type"} button>
            <ListItemIcon>
              <TimelineIcon />
            </ListItemIcon>
            <ListItemText
              primary="Analysis Type"
              secondary={this.props.result["analysis_type"]}
            />
          </ListItem>

          <ListItem
            key={"Techniques Open"}
            button
            onClick={() => {
              this.setState({ techniquesOpen: !this.state.techniquesOpen });
            }}
          >
            <ListItemIcon>
              <DialpadIcon />
            </ListItemIcon>
            <ListItemText primary="Techniques" />
            {this.state.techniquesOpen ? <ExpandLess /> : <ExpandMore />}
          </ListItem>
          <Collapse in  ={this.state.techniquesOpen} timeout="auto" unmountOnExit>
            {techniques}
          </Collapse>

          <ListItem
            key={"Education Open"}
            button
            onClick={() => {
              this.setState({
                educationLinksOpen: !this.state.educationLinksOpen,
              });
            }}
          >
            <ListItemIcon>
              <CastForEducationIcon />
            </ListItemIcon>
            <ListItemText primary="Education" />
            {this.state.educationLinksOpen ? <ExpandLess /> : <ExpandMore />}
          </ListItem>
          <Collapse
            className={classes.collapse}
            in={this.state.educationLinksOpen}
            timeout="auto"
            unmountOnExit
          >
            <List component="div" disablePadding>
              {educationLinks}
            </List>
          </Collapse>
        </List>
      </Modal>
    );
  }
}

ResultModal.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ResultModal);
