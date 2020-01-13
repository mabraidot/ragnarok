import React, { Component } from 'react';
import './Home.scss';
import Grid from '@material-ui/core/Grid';
import Grow from '@material-ui/core/Grow';
import Fab from '@material-ui/core/Fab';
import AdvancedIcon from '@material-ui/icons/TouchAppRounded';
import PanToolIcon from '@material-ui/icons/PanTool';
import Gauge from '../../components/Gauge';
import Socket from './../../components/Socket/Socket';

import ApiClient from './../../apiClient/ApiClient';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

import { withSnackbar } from 'notistack';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      socket: new Socket(),

      MashTunFocus: true,
      MashTunTemperatureSetPoint: 0,
      MashTunTemperatureProbe: 0,
      MashTunWaterLevelSetPoint: 0,
      MashTunWaterLevelProbe: 0,
      MashTunTimeSetPoint: 0,
      MashTunTimeProbe: 0,
      
      BoilKettleFocus: false,
      BoilKettleTemperatureSetPoint: 0,
      BoilKettleTemperatureProbe: 0,
      BoilKettleWaterLevelSetPoint: 0,
      BoilKettleWaterLevelProbe: 0,
      BoilKettleTimeSetPoint: 0,
      BoilKettleTimeProbe: 0,

      cookingRunning: false,
      automaticGaugeOrder: true,
      dialogOpen: false,
      dialogTitle: '',
      dialogDescription: '',
      dialogProcess: ''
    };
    this.handleAdvancedClick = this.handleAdvancedClick.bind(this);
    this.toggleGauge = this.toggleGauge.bind(this);
    this.handleClose = this.handleClose.bind(this);
    this.handleOpen = this.handleOpen.bind(this);
    this.handleContinueAction = this.handleContinueAction.bind(this);
  }

  componentDidMount() {
    const { socket } = this.state.socket;
    // const { dialogOpen } = this.state;

    socket.onmessage = (result) => {
      const data = JSON.parse(result.data)
      if (typeof data.MashTunTemperatureProbe !== 'undefined') {
        this.setState({MashTunTemperatureProbe: data.MashTunTemperatureProbe.toFixed(1)});
      }

      if (typeof data.MashTunTemperatureSetPoint !== 'undefined') {
        if (data.MashTunTemperatureSetPoint !== this.state.MashTunTemperatureSetPoint) {
          this.setState({MashTunTemperatureSetPoint: data.MashTunTemperatureSetPoint.toFixed(1)});
        }
      }
      if (typeof data.MashTunWaterLevelProbe !== 'undefined') {
        this.setState({MashTunWaterLevelProbe: data.MashTunWaterLevelProbe.toFixed(1)});
      }
      if (typeof data.MashTunWaterLevelSetPoint !== 'undefined') {
        if (data.MashTunWaterLevelSetPoint !== this.state.MashTunWaterLevelSetPoint) {
          this.setState({MashTunWaterLevelSetPoint: data.MashTunWaterLevelSetPoint.toFixed(1)});
        }
      }
      if (typeof data.MashTunTimeProbe !== 'undefined') {
        this.setState({MashTunTimeProbe: data.MashTunTimeProbe});
      }
      if (typeof data.MashTunTimeSetPoint !== 'undefined') {
        if (data.MashTunTimeSetPoint !== this.state.MashTunTimeSetPoint) {
          this.setState({MashTunTimeSetPoint: data.MashTunTimeSetPoint});
        }
      }

      if (typeof data.BoilKettleTemperatureProbe !== 'undefined') {
        this.setState({BoilKettleTemperatureProbe: data.BoilKettleTemperatureProbe.toFixed(1)});
      }
      if (typeof data.BoilKettleTemperatureSetPoint !== 'undefined') {
        if (data.BoilKettleTemperatureSetPoint !== this.state.BoilKettleTemperatureSetPoint) {
          this.setState({BoilKettleTemperatureSetPoint: data.BoilKettleTemperatureSetPoint.toFixed(1)});
        }
      }
      
      if (typeof data.BoilKettleWaterLevelProbe !== 'undefined') {
        this.setState({BoilKettleWaterLevelProbe: data.BoilKettleWaterLevelProbe.toFixed(1)});
      }
      if (typeof data.BoilKettleWaterLevelSetPoint !== 'undefined') {
        if (data.BoilKettleWaterLevelSetPoint !== this.state.BoilKettleWaterLevelSetPoint) {
          this.setState({BoilKettleWaterLevelSetPoint: data.BoilKettleWaterLevelSetPoint.toFixed(1)});
        }
      }

      if (typeof data.BoilKettleTimeProbe !== 'undefined') {
        this.setState({BoilKettleTimeProbe: data.BoilKettleTimeProbe});
      }
      if (typeof data.BoilKettleTimeSetPoint !== 'undefined') {
        if (data.BoilKettleTimeSetPoint !== this.state.BoilKettleTimeSetPoint) {
          this.setState({BoilKettleTimeSetPoint: data.BoilKettleTimeSetPoint});
        }
      }

      if (typeof data.cookingStep !== 'undefined') {
        if (data.cookingStep === 'paused' && !this.state.dialogOpen){
          this.handleOpen({
            'title': 'Process paused', 
            'description': 'Cooling process is about to start. Please connect the water hose to the chiller\'s inlet and outlet.',
            'process': 'resumeCooking'
          });
        } else if (data.cookingStep !== 'paused' && this.state.dialogOpen && this.state.dialogProcess === 'resumeCooking') {
          this.handleClose();
        }
        if (data.cookingStep !== 'mash' && data.cookingStep !== 'finish') {
          this.toggleGauge('boil', true);
        } else {
          this.toggleGauge('mash', true);
        }
      }

      if (typeof data.cookingRunning !== 'undefined') {
        this.setState({cookingRunning: (data.cookingRunning === 'False') ? false : true});
      }



      if (data.notice) {
        for(const message in data.notice){
          this.props.enqueueSnackbar(data.notice[message], { 
            variant: 'info',
          });
        }
      }
      if (data.error) {
        for(const message in data.error){
          this.props.enqueueSnackbar(data.error[message], { 
            variant: 'error',
          });
        }
      }
      if (data.persistent_notice) {
        for(const message in data.persistent_notice){
          this.props.enqueueSnackbar(data.persistent_notice[message], { 
            variant: 'info',
            persist: true,
          });
        }
      }
      if (data.persistent_error) {
        for(const message in data.persistent_error){
          this.props.enqueueSnackbar(data.persistent_error[message], { 
            variant: 'error',
            persist: true,
          });
        }
      }
      // console.log('[WS]: message!:', data);
    };

  }

  componentWillUnmount() {
    const { socket } = this.state.socket;
    socket.close();
  }

  handleOpen = (msg) => {
    this.setState({ 
      dialogOpen: true, 
      dialogTitle: msg.title,
      dialogDescription: msg.description, 
      dialogProcess: msg.process || ''
    });
  };

  handleClose = () => {
    this.setState({ 
      dialogOpen: false, 
      dialogTitle: '',
      dialogDescription: '',
      dialogProcess: '' 
    });
  };

  handleContinueAction = () => {
    this.handleClose();
    ApiClient.cookResume().then((resp) => {
      console.log('[API]', resp);
      if (resp.notice) {
        this.props.enqueueSnackbar(resp.notice, { 
          variant: 'info',
        });
      }
      if (resp.error) {
        this.props.enqueueSnackbar(resp.error, { 
          variant: 'error',
        });
      }
    });
  }

  handleStopCookingClick = () => {
    this.handleClose();
    ApiClient.cookStop().then((resp) => {
      console.log('[API]', resp);
      if (resp.notice) {
        this.props.enqueueSnackbar(resp.notice, { 
          variant: 'info',
        });
      }
      if (resp.error) {
        this.props.enqueueSnackbar(resp.error, { 
          variant: 'error',
        });
      }
    });    
  }

  handleAdvancedClick() {
    this.props.history.push('/advanced')
  }

  toggleGauge(gauge = 'mash', auto = true) {
    const { MashTunFocus, BoilKettleFocus, automaticGaugeOrder } = this.state;

    const newAutomaticGaugeOrder = (!auto) ? !automaticGaugeOrder : automaticGaugeOrder;
    if (automaticGaugeOrder || !auto) {
      if (gauge === 'mash' && !MashTunFocus) {
        this.setState({MashTunFocus: true, BoilKettleFocus: false, automaticGaugeOrder: newAutomaticGaugeOrder});
      }else if(gauge === 'boil' && !BoilKettleFocus) {
        this.setState({MashTunFocus: false, BoilKettleFocus: true, automaticGaugeOrder: newAutomaticGaugeOrder});
      }
    }
  }

  render() {
    const { 
      MashTunTemperatureSetPoint,
      MashTunTemperatureProbe,
      MashTunWaterLevelSetPoint,
      MashTunWaterLevelProbe,
      MashTunTimeSetPoint,
      MashTunTimeProbe,
      MashTunFocus,
      BoilKettleTemperatureSetPoint,
      BoilKettleTemperatureProbe,
      BoilKettleWaterLevelSetPoint,
      BoilKettleWaterLevelProbe,
      BoilKettleTimeSetPoint,
      BoilKettleTimeProbe,
      BoilKettleFocus,
    } = this.state;

    return(
      <Grow in={true}>
        <div className="Home">
          <Dialog
            open={this.state.dialogOpen}
            onClose={this.handleClose}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogTitle id="alert-dialog-title">{this.state.dialogTitle}</DialogTitle>
            <DialogContent>
              <DialogContentText id="alert-dialog-description">
                {this.state.dialogDescription}
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={this.handleClose} color="secondary" autoFocus>Cancel</Button>
              {this.state.dialogProcess === 'stopCooking' ? 
                <Button onClick={this.handleStopCookingClick} color="primary">Stop</Button>
              :
                <Button onClick={this.handleContinueAction} color="primary">Continue</Button>
              }
            </DialogActions>
          </Dialog>
          <Grid container>
            <Grid item xs onClick={() => this.toggleGauge('mash', false)}>
              <Gauge
                id='MashTunGauge'
                title='Mash Tun'
                setPointTemperature={MashTunTemperatureSetPoint}
                valueTemperature={MashTunTemperatureProbe}
                setPointWater={MashTunWaterLevelSetPoint}
                valueWater={MashTunWaterLevelProbe}
                setPointTime={MashTunTimeSetPoint}
                valueTime={MashTunTimeProbe}
                focus={MashTunFocus}
              />
            </Grid>
            <Grid item xs>
              <div className="button-advanced" style={{paddingTop: (!this.state.cookingRunning) ? '5.5em' : '3.5em'}}>
                <Fab variant="extended" onClick={this.handleAdvancedClick} size="large" aria-label="advanced">
                  <AdvancedIcon />
                  Advanced
                </Fab>
                {(this.state.cookingRunning) && (
                <Fab variant="extended" onClick={() => {this.handleOpen({
                      'title': 'Stop Cooking Process', 
                      'description': 'Are you sure to stop the current cooking process?',
                      'process': 'stopCooking'
                    });}} size="large" aria-label="stop">
                  <PanToolIcon />
                  Stop Cooking
                </Fab>
                )}
              </div>
            </Grid>
            <Grid item xs onClick={() => this.toggleGauge('boil', false)}>
              <Gauge
                id='BoilKettleGauge'
                title='Boil Kettle'
                setPointTemperature={BoilKettleTemperatureSetPoint}
                valueTemperature={BoilKettleTemperatureProbe}
                setPointWater={BoilKettleWaterLevelSetPoint}
                valueWater={BoilKettleWaterLevelProbe}
                setPointTime={BoilKettleTimeSetPoint}
                valueTime={BoilKettleTimeProbe}
                focus={BoilKettleFocus}
              />
            </Grid>
          </Grid>
        </div>
      </Grow>
    );
  }
}

export default withSnackbar(Home);