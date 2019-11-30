import React, { Component } from 'react';
import './Settings.scss';
import Grow from '@material-ui/core/Grow';
import Fab from '@material-ui/core/Fab';
import ApiClient from './../../apiClient/ApiClient';

class Settings extends Component {
  constructor(props) {
    super(props);

    this.handleMashTunPIDClick = this.handleMashTunPIDClick.bind(this);
    this.handleBoilKettlePIDClick = this.handleBoilKettlePIDClick.bind(this);
  }

  handleMashTunPIDClick() {
    
    ApiClient.startPIDAutotune('MashTun').then((resp) => {
      console.log('[API]', resp);
    });
    this.props.history.push('/advanced')
  }
  
  handleBoilKettlePIDClick() {
    ApiClient.startPIDAutotune('BoilKettle').then((resp) => {
      console.log('[API]', resp);
    });
    this.props.history.push('/advanced')
  }

  render() {
    return(
      <Grow in={true}>
        <div className="Settings">
          <h1>Settings</h1>
          <h4>PID Auto Tunning</h4>
          <div className="pid-autotune">
            <Fab variant="extended" onClick={this.handleMashTunPIDClick} size="large" aria-label="mashtun-autotune">
              Auto tune Mash Tun
            </Fab>
            <Fab variant="extended" onClick={this.handleBoilKettlePIDClick} size="large" aria-label="boilkettle-autotune">
              Auto tune Boil Kettle
            </Fab>
          </div>
        </div>
      </Grow>
    );
  }
}

export default Settings;