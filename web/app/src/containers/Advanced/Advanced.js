import React, { Component } from 'react';
import './Advanced.scss';
import Grow from '@material-ui/core/Grow';

class Advanced extends Component {

  render() {
    return(
      <Grow in={true}>
        <div className="Advanced">
          <h1>Advanced Mode</h1>
          <p>
            Machine's manual control
          </p>
        </div>
      </Grow>
    );
  }
}

export default Advanced;