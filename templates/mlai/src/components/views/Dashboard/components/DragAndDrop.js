import React, { Component } from 'react';
import clsx from 'clsx';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/styles';
import {
  Card,
  CardHeader,
  CardContent,
  CardActions,
  Divider,
  Button
} from '@material-ui/core';

import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';
import ArrowRightIcon from '@material-ui/icons/ArrowRight';

const styles = theme => ({
    root: {},
    chartContainer: {
      height: 400,
      position: 'relative'
    },
    actions: {
      justifyContent: 'flex-end'
    }
  });


class DragAndDrop extends Component {
    constructor(props) {
        super(props)
        this.state = {
            files: []
        }
    }

    render() {
        const { classes} = this.props;
        // const {className, ...rest } = this.props;

        return (
            <Card
            //   {...rest}
              className={classes.root}
            >
              <CardHeader
                action={
                  <Button
                    size="small"
                    variant="text"
                  >
                    Last 7 days <ArrowDropDownIcon />
                  </Button>
                }
                title="Latest Sales"
              />
              <Divider />
              <Divider />
              <CardActions className={classes.actions}>
                <Button
                  color="primary"
                  size="small"
                  variant="text"
                >
                  Overview <ArrowRightIcon />
                </Button>
              </CardActions>
            </Card>
          );
    }


}

DragAndDrop.propTypes = {
    className: PropTypes.string
  };
  
export default withStyles(styles)(DragAndDrop);
