import React, { Component } from 'react';
import './Settings.scss';
import Grow from '@material-ui/core/Grow';
import Fab from '@material-ui/core/Fab';
import ApiClient from './../../apiClient/ApiClient';
import { withSnackbar } from 'notistack';

class Settings extends Component {
  constructor(props) {
    super(props);

    this.handleMashTunPIDClick = this.handleMashTunPIDClick.bind(this);
    this.handleBoilKettlePIDClick = this.handleBoilKettlePIDClick.bind(this);
    this.handleAllValvesClick = this.handleAllValvesClick.bind(this);
  }

  handleMashTunPIDClick() {
    
    ApiClient.startPIDAutotune('MashTun').then((resp) => {
      console.log('[API]', resp);
      if (resp.error) {
        this.props.enqueueSnackbar(resp.error, { 
          variant: 'error',
        });
      }
    });
    this.props.history.push('/advanced')
  }
  
  handleBoilKettlePIDClick() {
    ApiClient.startPIDAutotune('BoilKettle').then((resp) => {
      console.log('[API]', resp);
      if (resp.error) {
        this.props.enqueueSnackbar(resp.error, { 
          variant: 'error',
        });
      }
    });
    this.props.history.push('/advanced')
  }

  handleAllValvesClick() {
    ApiClient.openAllValves().then((resp) => {
      console.log('[API]', resp);
      if (resp.error) {
        this.props.enqueueSnackbar(resp.error, { 
          variant: 'error',
        });
      }
    });
    this.props.history.push('/advanced')
  };


  render() {
    return(
      <Grow in={true}>
        <div className="Settings">
          <h1>Settings</h1>
          <h4>PID Auto Tunning</h4>
          <div className="pid-autotune">
            <label>Perform PID autotune on MashTun</label>
            <Fab variant="extended" onClick={this.handleMashTunPIDClick} size="large" aria-label="mashtun-autotune">
              Auto tune
            </Fab>
          </div>

          <div className="pid-autotune">
            <label>Perform PID autotune on Boil Kettle</label>
            <Fab variant="extended" onClick={this.handleBoilKettlePIDClick} size="large" aria-label="boilkettle-autotune">
              Auto tune
            </Fab>
          </div>

          <h4>Valves</h4>
          <div className="valves">
            <label>Open all valves to help drain hoses</label>
            <Fab variant="extended" onClick={this.handleAllValvesClick} size="large" aria-label="open-all-valves">
              Open valves
            </Fab>
          </div>

        </div>
      </Grow>
    );
  }
}

export default withSnackbar(Settings);