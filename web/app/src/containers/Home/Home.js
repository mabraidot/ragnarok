import React, { Component } from 'react';
import './Home.scss';
import Grid from '@material-ui/core/Grid';
import Grow from '@material-ui/core/Grow';
import Fab from '@material-ui/core/Fab';
import AdvancedIcon from '@material-ui/icons/TouchAppRounded';
import Gauge from '../../components/Gauge';
import Socket from './../../components/Socket/Socket';
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
    };
    this.handleAdvancedClick = this.handleAdvancedClick.bind(this);
    this.toggleGauge = this.toggleGauge.bind(this);
  }

  componentDidMount() {
    const { socket } = this.state.socket;
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

      if (data.notice) {
        for(const message in data.notice){
          this.props.enqueueSnackbar(data.notice[message], { 
            variant: 'info',
            persist: true,
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
      if (data.process) {
        if (data.process[0] !== 'mash' && data.process[0] !== 'finish') {
          this.toggleGauge('boil');
        } else {
          this.toggleGauge('mash');
        }
      }
      // console.log('[WS]: message!:', data);
    };
  }

  componentWillUnmount() {
    const { socket } = this.state.socket;
    socket.close();
  }

  handleAdvancedClick() {
    this.props.history.push('/advanced')
  }

  toggleGauge(gauge = 'mash') {
    console.log(gauge);
    if (gauge === 'mash') {
      this.setState({MashTunFocus: true, BoilKettleFocus: false});
    }else{
      this.setState({MashTunFocus: false, BoilKettleFocus: true});
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
          <Grid container>
            <Grid item xs onClick={() => this.toggleGauge('mash')}>
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
              <div className="button-advanced">
                <Fab variant="extended" onClick={this.handleAdvancedClick} size="large" aria-label="advanced">
                  <AdvancedIcon />
                  Advanced
                </Fab>
              </div>
            </Grid>
            <Grid item xs onClick={() => this.toggleGauge('boil')}>
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