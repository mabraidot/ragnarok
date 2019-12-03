import React, { Component } from 'react';
import './Advanced.scss';
import Grow from '@material-ui/core/Grow';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Slider from '@material-ui/core/Slider';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import Socket from './../../components/Socket/Socket';
import ApiClient from './../../apiClient/ApiClient';
import { withSnackbar } from 'notistack';

class Advanced extends Component {
  constructor(props) {
    super(props);
    this.state = {
      socket: new Socket(),

      MashTunHeater: false,
      MashTunValveInlet: false,
      MashTunValveOutlet: false,
      
      MashTunTemperatureSetPoint: 65,
      MashTunTemperatureProbe: 0,
      MashTunWaterLevelSetPoint: 14.5,
      MashTunWaterLevelProbe: 0,
      MashTunTimeSetPoint: 15,
      MashTunTimeProbe: 0,
      
      BoilKettleHeater: false,
      BoilKettleValveWater: false,
      BoilKettleValveInlet: false,
      BoilKettleValveOutlet: false,

      BoilKettleTemperatureSetPoint: 100,
      BoilKettleTemperatureProbe: 0,
      BoilKettleWaterLevelSetPoint: 7.5,
      BoilKettleWaterLevelProbe: 0,
      BoilKettleTimeSetPoint: 60,
      BoilKettleTimeProbe: 0,

      ChillerValveWater: false,
      ChillerValveWort: false,
      OutletValveDump: false,
      Pump: false,

      notice: true,
      noticeType: 'error',
      noticeMessage: 'este es un mensaje de error'

    };
  }
  
  componentDidMount() {
    const { socket } = this.state.socket;
    socket.onmessage = (result) => {
      const data = JSON.parse(result.data);

      if (data.MashTunTemperatureProbe) {
        this.setState({MashTunTemperatureProbe: data.MashTunTemperatureProbe.toFixed(1)});
      }
      if (data.MashTunTemperatureSetPoint) {
        if (data.MashTunTemperatureSetPoint !== this.state.MashTunTemperatureSetPoint) {
          this.setState({MashTunTemperatureSetPoint: data.MashTunTemperatureSetPoint.toFixed(1)});
        }
      }
      if (data.MashTunWaterLevelProbe) {
        this.setState({MashTunWaterLevelProbe: data.MashTunWaterLevelProbe.toFixed(1)});
      }
      if (data.MashTunWaterLevelSetPoint) {
        if (data.MashTunWaterLevelSetPoint !== this.state.MashTunWaterLevelSetPoint) {
          this.setState({MashTunWaterLevelSetPoint: data.MashTunWaterLevelSetPoint.toFixed(1)});
        }
      }
      if (data.MashTunTimeProbe) {
        this.setState({MashTunTimeProbe: data.MashTunTimeProbe});
      }
      if (data.MashTunTimeSetPoint) {
        if (data.MashTunTimeSetPoint !== this.state.MashTunTimeSetPoint) {
          this.setState({MashTunTimeSetPoint: data.MashTunTimeSetPoint});
        }
      }

      if (data.BoilKettleTemperatureProbe) {
        this.setState({BoilKettleTemperatureProbe: data.BoilKettleTemperatureProbe.toFixed(1)});
      }
      if (data.BoilKettleTemperatureSetPoint) {
        if (data.BoilKettleTemperatureSetPoint !== this.state.BoilKettleTemperatureSetPoint) {
          this.setState({BoilKettleTemperatureSetPoint: data.BoilKettleTemperatureSetPoint.toFixed(1)});
        }
      }
      if (data.BoilKettleWaterLevelProbe) {
        this.setState({BoilKettleWaterLevelProbe: data.BoilKettleWaterLevelProbe.toFixed(1)});
      }
      if (data.BoilKettleWaterLevelSetPoint) {
        if (data.BoilKettleWaterLevelSetPoint !== this.state.BoilKettleWaterLevelSetPoint) {
          this.setState({BoilKettleWaterLevelSetPoint: data.BoilKettleWaterLevelSetPoint.toFixed(1)});
        }
      }
      if (data.BoilKettleTimeProbe) {
        this.setState({BoilKettleTimeProbe: data.BoilKettleTimeProbe});
      }
      if (data.BoilKettleTimeSetPoint) {
        if (data.BoilKettleTimeSetPoint !== this.state.BoilKettleTimeSetPoint) {
          this.setState({BoilKettleTimeSetPoint: data.BoilKettleTimeSetPoint});
        }
      }

      if (data.MashTunHeater) {
        this.setState({MashTunHeater: (data.MashTunHeater === 'False') ? false : true});
      }
      if (data.BoilKettleHeater) {
        this.setState({BoilKettleHeater: (data.BoilKettleHeater === 'False') ? false : true});
      }

      if (data.OutletValveDump) {
        this.setState({OutletValveDump: (data.OutletValveDump === '0') ? false : true});
      }
      if (data.ChillerValveWort) {
        this.setState({ChillerValveWort: (data.ChillerValveWort === '0') ? false : true});
      }
      if (data.ChillerValveWater) {
        this.setState({ChillerValveWater: (data.ChillerValveWater === '0') ? false : true});
      }
      if (data.BoilKettleValveOutlet) {
        this.setState({BoilKettleValveOutlet: (data.BoilKettleValveOutlet === '0') ? false : true});
      }
      if (data.BoilKettleValveInlet) {
        this.setState({BoilKettleValveInlet: (data.BoilKettleValveInlet === '0') ? false : true});
      }
      if (data.BoilKettleValveWater) {
        this.setState({BoilKettleValveWater: (data.BoilKettleValveWater === '0') ? false : true});
      }
      if (data.MashTunValveOutlet) {
        this.setState({MashTunValveOutlet: (data.MashTunValveOutlet === '0') ? false : true});
      }
      if (data.MashTunValveInlet) {
        this.setState({MashTunValveInlet: (data.MashTunValveInlet === '0') ? false : true});
      }
      
      if (data.Pump) {
        this.setState({Pump: (data.Pump === 'False') ? false : true});
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
      console.log('[WS]: message!:', data);
    };
  }

  componentWillUnmount() {
    const { socket } = this.state.socket;
    socket.close();
  }

  intToMinutes = (number) => {
    var minutes = parseInt(Number(number));
    var seconds = Math.round((Number(number)-minutes) * 60);
    return `${minutes.toString().padStart(2,"00")}:${seconds.toString().padStart(2,"00")}`;
  }

  handleSwitchChange = name => event => {
    const { state } = this.state;
    this.setState({ ...state, [name]: event.target.checked });
    console.log('[ADV]: Switch:', name, (event.target.checked) ? 'ON' : 'OFF');
    
    ApiClient.setSwitch(name, event.target.checked).then((resp) => {
      console.log('[API]', resp);
    });
  };

  handleSliderSetPoint = name => (event, value) => {
    const { state } = this.state;
    this.setState({ ...state, [name]: value });
    console.log('[ADV]: SetPoint:', name, value);
  
    ApiClient.setPoint(name, value).then((resp) => {
      console.log('[API]', resp);
      if (resp.error) {
        this.props.enqueueSnackbar(resp.error, { 
          variant: 'error',
        });
      }
    });

  }

  render() {
    
    // const marksTemperature = [
    //   { value: 0, label: '0°C' },
    //   { value: 25, label: '25°C' },
    //   { value: 50, label: '50°C' },
    //   { value: 75, label: '75°C' },
    //   { value: 100, label: '100°C' },
    // ];

    // const marksWater = [
    //   { value: 0, label: '0L' },
    //   { value: 4, label: '4L' },
    //   { value: 8, label: '8L' },
    //   { value: 12, label: '12L' },
    //   { value: 16, label: '16L' },
    // ];

    // const marksTime = [
    //   { value: 0, label: '0\'' },
    //   { value: 30, label: '30\'' },
    //   { value: 60, label: '60\'' },
    //   { value: 90, label: '90\'' },
    //   { value: 120, label: '120\'' },
    // ];

    return(
      <Grow in={true}>
        <div className="Advanced">
        {/* <div className="label" style={{padding: '0.5rem'}}>Advanced Mode</div> */}
        <h4>Advanced Mode</h4>
          <Grid container>

            <Grid item xs={6}>
              <Paper elevation={2}>
                <h4>Mash Tun</h4>
                <Slider
                  className="temperature"
                  defaultValue={this.state.MashTunTemperatureSetPoint}
                  aria-labelledby="discrete-slider-always"
                  step={1}
                  max={110}
                  valueLabelDisplay="auto"
                  onChangeCommitted={this.handleSliderSetPoint("MashTunTemperatureSetPoint")}
                />
                <div className="label"><span>{this.state.MashTunTemperatureProbe}°</span> / {this.state.MashTunTemperatureSetPoint}°</div>
                <div className="foot">Temperature</div>

                <Slider
                  className="water"
                  defaultValue={this.state.MashTunWaterLevelSetPoint}
                  aria-labelledby="discrete-slider-always"
                  step={0.1}
                  max={16}
                  valueLabelDisplay="auto"
                  onChangeCommitted={this.handleSliderSetPoint("MashTunWaterLevelSetPoint")}
                />
                <div className="label"><span>{this.state.MashTunWaterLevelProbe}L</span> / {this.state.MashTunWaterLevelSetPoint}L</div>
                <div className="foot">Water Level</div>

                <Slider
                  className="time"
                  defaultValue={this.state.MashTunTimeSetPoint}
                  aria-labelledby="discrete-slider-always"
                  step={1}
                  max={120}
                  valueLabelDisplay="auto"
                  onChangeCommitted={this.handleSliderSetPoint("MashTunTimeSetPoint")}
                />
                <div className="label"><span>{this.intToMinutes(this.state.MashTunTimeProbe)}'</span> / {this.intToMinutes(this.state.MashTunTimeSetPoint)}</div>
                <div className="foot">Process time</div>

                <p> </p>
                <h4>Mash Tun Valves</h4>
                <FormControlLabel
                  control={<Switch checked={this.state.MashTunHeater} onChange={this.handleSwitchChange('MashTunHeater')}  value="MashTunHeater" className="heater" />}
                  label="Heater"
                />
                <FormControlLabel
                  control={<Switch checked={this.state.MashTunValveInlet} onChange={this.handleSwitchChange('MashTunValveInlet')}  value="MashTunValveInlet" />}
                  label="Inlet"
                />
                <FormControlLabel
                  control={<Switch checked={this.state.MashTunValveOutlet} onChange={this.handleSwitchChange('MashTunValveOutlet')}  value="MashTunValveOutlet" />}
                  label="Outlet"
                />
              </Paper>
            </Grid>
            
            
            

            <Grid item xs={6}>
              <Paper elevation={2}>
                <h4>Boil Kettle</h4>
                <Slider
                  className="temperature"
                  defaultValue={this.state.BoilKettleTemperatureSetPoint}
                  aria-labelledby="discrete-slider-always"
                  step={1}
                  max={110}
                  valueLabelDisplay="auto"
                  onChangeCommitted={this.handleSliderSetPoint("BoilKettleTemperatureSetPoint")}
                />
                <div className="label"><span>{this.state.BoilKettleTemperatureProbe}°</span> / {this.state.BoilKettleTemperatureSetPoint}°</div>
                <div className="foot">Temperature</div>

                <Slider
                  className="water"
                  defaultValue={this.state.BoilKettleWaterLevelSetPoint}
                  aria-labelledby="discrete-slider-always"
                  step={0.1}
                  max={16}
                  valueLabelDisplay="auto"
                  onChangeCommitted={this.handleSliderSetPoint("BoilKettleWaterLevelSetPoint")}
                />
                <div className="label"><span>{this.state.BoilKettleWaterLevelProbe}L</span> / {this.state.BoilKettleWaterLevelSetPoint}L</div>
                <div className="foot">Water Level</div>

                <Slider
                  className="time"
                  defaultValue={this.state.BoilKettleTimeSetPoint}
                  aria-labelledby="discrete-slider-always"
                  step={1}
                  max={120}
                  valueLabelDisplay="auto"
                  onChangeCommitted={this.handleSliderSetPoint("BoilKettleTimeSetPoint")}
                />
                <div className="label"><span>{this.intToMinutes(this.state.BoilKettleTimeProbe)}</span> / {this.intToMinutes(this.state.BoilKettleTimeSetPoint)}</div>
                <div className="foot">Process Time</div>

                <p> </p>
                <h4>Boil Kettle Valves</h4>
                <FormControlLabel
                  control={<Switch checked={this.state.BoilKettleHeater} onChange={this.handleSwitchChange('BoilKettleHeater')}  value="BoilKettleHeater" className="heater" />}
                  label="Heater"
                />
                <FormControlLabel
                  control={<Switch checked={this.state.BoilKettleValveWater} onChange={this.handleSwitchChange('BoilKettleValveWater')}  value="BoilKettleValveWater" />}
                  label="Water"
                />
                <FormControlLabel
                  control={<Switch checked={this.state.BoilKettleValveInlet} onChange={this.handleSwitchChange('BoilKettleValveInlet')}  value="BoilKettleValveInlet" />}
                  label="Inlet"
                />
                <FormControlLabel
                  control={<Switch checked={this.state.BoilKettleValveOutlet} onChange={this.handleSwitchChange('BoilKettleValveOutlet')}  value="BoilKettleValveOutlet" />}
                  label="Outlet"
                />
              </Paper>
            </Grid>









            <Grid item xs={6}>
              <Paper elevation={2}>
                <h4>Chiller valves</h4>
                <FormControlLabel
                  control={<Switch checked={this.state.ChillerValveWater} onChange={this.handleSwitchChange('ChillerValveWater')}  value="ChillerValveWater" />}
                  label="Water"
                />
                <FormControlLabel
                  control={<Switch checked={this.state.ChillerValveWort} onChange={this.handleSwitchChange('ChillerValveWort')}  value="ChillerValveWort" />}
                  label="Wort"
                />
              </Paper>
            </Grid>
            
            <Grid item xs={6}>
              <Paper elevation={2}>
                <h4>Outlet valve</h4>
                <FormControlLabel
                  control={<Switch checked={this.state.OutletValveDump} onChange={this.handleSwitchChange('OutletValveDump')}  value="OutletValveDump" />}
                  label="Dump"
                />
              </Paper>
            </Grid>

            <Grid item xs={6}>
              <Paper elevation={2}>
                <h4>Pump</h4>
                <FormControlLabel
                  control={<Switch checked={this.state.Pump} onChange={this.handleSwitchChange('Pump')}  value="Pump" className="heater" />}
                  label="Motor"
                /> 
              </Paper>
            </Grid>


          </Grid>
        </div>
      </Grow>
    );
  }
}

export default withSnackbar(Advanced);