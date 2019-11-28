import React, { Component } from 'react';
import './Power.scss';
import Grow from '@material-ui/core/Grow';

import PowerIcon from '@material-ui/icons/PowerSettingsNewRounded';

class Power extends Component {
  
  constructor(props) {
    super(props)
    this.state = {
      hover: false
    }
  }
  
  handleClick = () => {
    this.setState({hover: !this.state.hover})
    if (!this.state.hover) {
      console.log('[SYS]: Powering down ...');
    }
    // Logic to Turn off the machine
  }
  
  render() {
    return(
      <Grow in={true}>
        <div className="Power-button">
          <PowerIcon className={(this.state.hover) ? "button-hover" : "button"} onTouchStart={this.handleClick} onTouchEnd={this.handleClick} />
          <p>Power Off</p>
        </div>
      </Grow>
    );
  }
}

export default Power;