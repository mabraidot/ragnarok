import React, { Component } from 'react';
import './Advanced.scss';
import Grow from '@material-ui/core/Grow';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Slider from '@material-ui/core/Slider';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import Socket from './../../components/Socket/Socket';

class Advanced extends Component {
  constructor(props) {
    super(props);
    this.state = {
      socket: new Socket(),

      MashTunHeater: false,
      MashTunValveInlet: false,
      MashTunValveOutlet: false,
      
      MashTunTemperatureSetPoint: 65,
      MashTunTemperatureProbe: 23.2,
      MashTunWaterSetPoint: 14.5,
      MashTunWaterProbe: 12.8,
      MashTunTimeSetPoint: 15,
      MashTunTimeProbe: 5,
      
      BoilKettleHeater: false,
      BoilKettleValveWater: false,
      BoilKettleValveInlet: false,
      BoilKettleValveOutlet: false,

      BoilKettleTemperatureSetPoint: 100,
      BoilKettleTemperatureProbe: 40.8,
      BoilKettleWaterSetPoint: 7.5,
      BoilKettleWaterProbe: 3.4,
      BoilKettleTimeSetPoint: 60,
      BoilKettleTimeProbe: 20,

      ChillerValveWater: false,
      ChillerValveWort: false,
      OutletValveDump: false,
      Pump: false,

    };
  }
  
  componentDidMount() {
    const { socket } = this.state.socket;
    socket.onmessage = (result) => {
      const data = JSON.parse(result.data);

      if (data.MashTunTemperatureProbe) {
        this.setState({MashTunTemperatureProbe: data.MashTunTemperatureProbe});
      }
      if (data.MashTunTemperatureSetPoint) {
        this.setState({MashTunTemperatureSetPoint: data.MashTunTemperatureSetPoint});
      }
      if (data.MashTunWaterProbe) {
        this.setState({MashTunWaterProbe: data.MashTunWaterProbe});
      }
      if (data.MashTunWaterSetPoint) {
        this.setState({MashTunWaterSetPoint: data.MashTunWaterSetPoint});
      }
      if (data.MashTunTimeProbe) {
        this.setState({MashTunTimeProbe: data.MashTunTimeProbe});
      }
      if (data.MashTunTimeSetPoint) {
        this.setState({MashTunTimeSetPoint: data.MashTunTimeSetPoint});
      }

      if (data.BoilKettleTemperatureProbe) {
        this.setState({BoilKettleTemperatureProbe: data.BoilKettleTemperatureProbe});
      }
      if (data.BoilKettleTemperatureSetPoint) {
        this.setState({BoilKettleTemperatureSetPoint: data.BoilKettleTemperatureSetPoint});
      }
      if (data.BoilKettleWaterProbe) {
        this.setState({BoilKettleWaterProbe: data.BoilKettleWaterProbe});
      }
      if (data.BoilKettleWaterSetPoint) {
        this.setState({BoilKettleWaterSetPoint: data.BoilKettleWaterSetPoint});
      }
      if (data.BoilKettleTimeProbe) {
        this.setState({BoilKettleTimeProbe: data.BoilKettleTimeProbe});
      }
      if (data.BoilKettleTimeSetPoint) {
        this.setState({BoilKettleTimeSetPoint: data.BoilKettleTimeSetPoint});
      }

      // console.log('[WS]: message!:', data);
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
  };

  handleSliderSetPoint = name => (event, value) => {
    const { state } = this.state;
    this.setState({ ...state, [name]: value });
    console.log('[ADV]: SetPoint:', name, value);
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
                  defaultValue={this.state.MashTunWaterSetPoint}
                  aria-labelledby="discrete-slider-always"
                  step={0.1}
                  max={16}
                  valueLabelDisplay="auto"
                  onChangeCommitted={this.handleSliderSetPoint("MashTunWaterSetPoint")}
                />
                <div className="label"><span>{this.state.MashTunWaterProbe}L</span> / {this.state.MashTunWaterSetPoint}L</div>
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
                  defaultValue={this.state.BoilKettleWaterSetPoint}
                  aria-labelledby="discrete-slider-always"
                  step={0.1}
                  max={16}
                  valueLabelDisplay="auto"
                  onChangeCommitted={this.handleSliderSetPoint("BoilKettleWaterSetPoint")}
                />
                <div className="label"><span>{this.state.BoilKettleWaterProbe}L</span> / {this.state.BoilKettleWaterSetPoint}L</div>
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

export default Advanced;