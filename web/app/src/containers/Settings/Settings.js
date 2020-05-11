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
    this.handleCleaningShortClick = this.handleCleaningShortClick.bind(this);
    this.handleCleaningSanitizationClick = this.handleCleaningSanitizationClick.bind(this);
    this.handleCleaningFullClick = this.handleCleaningFullClick.bind(this);
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

  handleCleaningShortClick() {
    ApiClient.cleanShort().then((resp) => {
      console.log('[API]', resp);
      if (resp.notice) {
        this.props.enqueueSnackbar(resp.notice, { 
          variant: 'success',
        });
        this.props.history.push('/')
      }
      if (resp.error) {
        this.props.enqueueSnackbar(resp.error, { 
          variant: 'error',
        });
      }
      if (resp.persistent_notice) {
        this.props.enqueueSnackbar(resp.persistent_notice, { 
          variant: 'success',
          persist: true,
        });
      }
      if (resp.persistent_error) {
        this.props.enqueueSnackbar(resp.persistent_error, { 
          variant: 'error',
          persist: true,
        });
      }
    });
  }

  handleCleaningSanitizationClick() {
    ApiClient.cleanSanitization().then((resp) => {
      console.log('[API]', resp);
      if (resp.notice) {
        this.props.enqueueSnackbar(resp.notice, { 
          variant: 'success',
        });
        this.props.history.push('/')
      }
      if (resp.error) {
        this.props.enqueueSnackbar(resp.error, { 
          variant: 'error',
        });
      }
      if (resp.persistent_notice) {
        this.props.enqueueSnackbar(resp.persistent_notice, { 
          variant: 'success',
          persist: true,
        });
      }
      if (resp.persistent_error) {
        this.props.enqueueSnackbar(resp.persistent_error, { 
          variant: 'error',
          persist: true,
        });
      }
    });
  }

  handleCleaningFullClick() {
    ApiClient.cleanFull().then((resp) => {
      console.log('[API]', resp);
      if (resp.notice) {
        this.props.enqueueSnackbar(resp.notice, { 
          variant: 'success',
        });
        this.props.history.push('/')
      }
      if (resp.error) {
        this.props.enqueueSnackbar(resp.error, { 
          variant: 'error',
        });
      }
      if (resp.persistent_notice) {
        this.props.enqueueSnackbar(resp.persistent_notice, { 
          variant: 'success',
          persist: true,
        });
      }
      if (resp.persistent_error) {
        this.props.enqueueSnackbar(resp.persistent_error, { 
          variant: 'error',
          persist: true,
        });
      }
    });
  }


  render() {
    return(
      <Grow in={true}>
        <div className="Settings">
          <h1>Settings</h1>
          <h4>Cleaning</h4>
          <div className="cleaning">
            <label>Short cleaning program to rinse equipment</label>
            <Fab variant="extended" onClick={this.handleCleaningShortClick} size="large" aria-label="cleaning-short">
              Short
            </Fab>
          </div>
          <div className="cleaning">
            <label>Sanitization program before starting a new cooking process</label>
            <Fab variant="extended" onClick={this.handleCleaningSanitizationClick} size="large" aria-label="cleaning-sanitization">
              Sanitizacion
            </Fab>
          </div>
          <div className="cleaning">
            <label>Full cleaning program combines Short and Sanitization program</label>
            <Fab variant="extended" onClick={this.handleCleaningFullClick} size="large" aria-label="cleaning-full">
              Full
            </Fab>
          </div>


          <h4>Valves</h4>
          <div className="valves">
            <label>Open all valves to help drain hoses</label>
            <Fab variant="extended" onClick={this.handleAllValvesClick} size="large" aria-label="open-all-valves">
              Open valves
            </Fab>
          </div>


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


        </div>
      </Grow>
    );
  }
}

export default withSnackbar(Settings);