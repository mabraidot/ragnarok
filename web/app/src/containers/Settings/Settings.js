import React, { Component } from 'react';
import './Settings.scss';
import Grow from '@material-ui/core/Grow';

class Settings extends Component {

  render() {
    return(
      <Grow in={true}>
        <div className="Settings">
          <h1>Settings</h1>
          <p>
            Settings page
          </p>
        </div>
      </Grow>
    );
  }
}

export default Settings;