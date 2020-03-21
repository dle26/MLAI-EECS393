
import React, { Component } from "react";
import PropTypes from 'prop-types';
import clsx from 'clsx';
import { makeStyles, withStyles } from "@material-ui/core/styles";
import { Typography, Link } from '@material-ui/core';

const styles = theme => ({
  root: {
    padding: theme.spacing(4)
  }
});


class Footer extends Component{
  constructor(props) {
    super(props)
  }

  render() {

    const { classes} = this.props;
    const { className, ...rest } = this.props;
    return (
      <div
      {...rest}
      className={clsx(classes.root, className)}
    >
      <Typography variant="body1">
        <Link
          component="a"
          href="https://github.com/justinphan3110/MLAI-EECS393"
          target="_blank"
        >
          Machine Learning Accessibility Initiative (MLAI)
        </Link>
        . 2020
      </Typography>
    </div>
    )
  }
}
Footer.propTypes = {
  className: PropTypes.string
};

export default withStyles(styles)(Footer);

