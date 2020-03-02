import React, {Component} from 'react';
import { Link as RouterLink } from 'react-router-dom';
import clsx from 'clsx';
import PropTypes from 'prop-types';
import { Avatar, Typography } from '@material-ui/core';
import { withStyles } from "@material-ui/core/styles";


const styles = theme => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    minHeight: 'fit-content'
  },
  avatar: {
    width: 60,
    height: 60
  },
  name: {
    marginTop: theme.spacing(1)
  }
});

class Profile extends Component {
  constructor(props) {
    super(props)
  }

  render() {
    const {classes, className, ...rest } = this.props;

    const user = {
      name: 'Shen Zhi',
      avatar: '/images/avatars/avatar_11.png',
      bio: 'Brain Director'
    };

    return (
      <div
        {...rest}
        className={clsx(classes.root, className)}
      >
        <Avatar
          alt="Person"
          className={classes.avatar}
          component={RouterLink}
          src={user.avatar}
          to="/settings"
        />
        <Typography
          className={classes.name}
          variant="h4"
        >
          {user.name}
        </Typography>
        <Typography variant="body2">{user.bio}</Typography>
      </div>
    );

  }
}

Profile.propTypes = {
  className: PropTypes.string
};

export default withStyles(styles)(Profile);
