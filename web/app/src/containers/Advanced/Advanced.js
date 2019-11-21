import React, { Component } from 'react';
import './Advanced.scss';
import Grow from '@material-ui/core/Grow';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Slider from '@material-ui/core/Slider';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';

class Advanced extends Component {
  constructor(props) {
    super(props);
    this.state = {
      checkedA: false,
      checkedB: false,
    };
  }
  
  handleChange = name => event => {
    const { state } = this.state;
    this.setState({ ...state, [name]: event.target.checked });
  };

  handleSliderSetPoint = name => (event, value) => {
    const { state } = this.state;
    alert(value[1]);
  }

  render() {
    const marksTemperature = [
      {
        value: 0,
        label: '0°C',
      },
      {
        value: 25,
        label: '25°C',
      },
      {
        value: 50,
        label: '50°C',
      },
      {
        value: 75,
        label: '75°C',
      },
      {
        value: 100,
        label: '100°C',
      },
    ];

    const marksWater = [
      {
        value: 0,
        label: '0L',
      },
      {
        value: 4,
        label: '4L',
      },
      {
        value: 8,
        label: '8L',
      },
      {
        value: 12,
        label: '12L',
      },
      {
        value: 16,
        label: '16L',
      },
    ];

    const marksTime = [
      {
        value: 0,
        label: '0\'',
      },
      {
        value: 30,
        label: '30\'',
      },
      {
        value: 60,
        label: '60\'',
      },
      {
        value: 90,
        label: '90\'',
      },
      {
        value: 120,
        label: '120\'',
      },
    ];

    return(
      <Grow in={true}>
        <div className="Advanced">
        <div className="label" style={{padding: '0.5rem'}}>Advanced Mode</div>
          <Grid container>

            <Grid item xs={6}>
              <Paper elevation={2}>
                <h4>Mash Tun</h4>
                <Slider
                  className="temperature"
                  defaultValue={[0, 0]}
                  aria-labelledby="discrete-slider-always"
                  step={1}
                  max={marksTemperature[4].value}
                  marks={marksTemperature}
                  valueLabelDisplay="on"
                  onChangeCommitted={this.handleSliderSetPoint("mashTunTemperature")}
                />
                <div className="label">Temperature</div>

                <Slider
                  className="water"
                  defaultValue={[0, 0]}
                  aria-labelledby="discrete-slider-always"
                  step={0.1}
                  max={marksWater[4].value}
                  marks={marksWater}
                  valueLabelDisplay="on"
                  onChangeCommitted={this.handleSliderSetPoint("mashTunWater")}
                />
                <div className="label">Water level</div>

                <Slider
                  className="time"
                  defaultValue={[0, 0]}
                  aria-labelledby="discrete-slider-always"
                  step={1}
                  max={marksTime[4].value}
                  marks={marksTime}
                  valueLabelDisplay="on"
                  onChangeCommitted={this.handleSliderSetPoint("mashTunTime")}
                />
                <div className="label">Process time</div>
                
                <p> </p>
                <h4>Valves</h4>
                <FormControlLabel
                  control={<Switch checked={this.state.checkedA} onChange={this.handleChange('checkedA')}  value="checkedA" className="heater" />}
                  label="Heater"
                />
                <FormControlLabel
                  control={<Switch checked={this.state.checkedA} onChange={this.handleChange('checkedA')}  value="checkedA" />}
                  label="Inlet"
                />
                <FormControlLabel
                  control={<Switch checked={this.state.checkedB} onChange={this.handleChange('checkedB')}  value="checkedB" />}
                  label="Outlet"
                />
              </Paper>
            </Grid>
            
            
            

            <Grid item xs={6}>
              <Paper elevation={2}>
                <h4>Boil Kettle</h4>
                <Slider
                  className="temperature"
                  defaultValue={[0, 0]}
                  aria-labelledby="discrete-slider-always"
                  step={1}
                  max={marksTemperature[4].value}
                  marks={marksTemperature}
                  valueLabelDisplay="on"
                  onChangeCommitted={this.handleSliderSetPoint("boilKettleTemperature")}
                />
                <div className="label">Temperature</div>

                <Slider
                  className="water"
                  defaultValue={[0, 12]}
                  aria-labelledby="discrete-slider-always"
                  step={0.1}
                  max={marksWater[4].value}
                  marks={marksWater}
                  valueLabelDisplay="on"
                  onChangeCommitted={this.handleSliderSetPoint("boilKettleWater")}
                />
                <div className="label">Water level</div>

                <Slider
                  className="time"
                  defaultValue={[0, 0]}
                  aria-labelledby="discrete-slider-always"
                  step={1}
                  max={marksTime[4].value}
                  marks={marksTime}
                  valueLabelDisplay="on"
                  onChangeCommitted={this.handleSliderSetPoint("boilKettleTime")}
                />
                <div className="label">Process time</div>

                <p> </p>
                <h4>Valves</h4>
                <FormControlLabel
                  control={<Switch checked={this.state.checkedA} onChange={this.handleChange('checkedA')}  value="checkedA" className="heater" />}
                  label="Heater"
                />
                <FormControlLabel
                  control={<Switch checked={this.state.checkedA} onChange={this.handleChange('checkedA')}  value="checkedA" />}
                  label="Water"
                />
                <FormControlLabel
                  control={<Switch checked={this.state.checkedB} onChange={this.handleChange('checkedB')}  value="checkedB" />}
                  label="Inlet"
                />
                <FormControlLabel
                  control={<Switch checked={this.state.checkedB} onChange={this.handleChange('checkedB')}  value="checkedB" />}
                  label="Outlet"
                />
              </Paper>
            </Grid>









            <Grid item xs={6}>
              <Paper elevation={2}>
                <h4>Chiller valves</h4>
                <FormControlLabel
                  control={<Switch checked={this.state.checkedB} onChange={this.handleChange('checkedB')}  value="checkedB" />}
                  label="Water"
                />
                <FormControlLabel
                  control={<Switch checked={this.state.checkedB} onChange={this.handleChange('checkedB')}  value="checkedB" />}
                  label="Wort"
                />
              </Paper>
            </Grid>
            
            <Grid item xs={6}>
              <Paper elevation={2}>
                <h4>Outlet valve</h4>
                <FormControlLabel
                  control={<Switch checked={this.state.checkedB} onChange={this.handleChange('checkedB')}  value="checkedB" />}
                  label="Dump"
                />
              </Paper>
            </Grid>

            <Grid item xs={12}>
              <Paper elevation={2}>
                <h4>Pump</h4>
                <FormControlLabel
                  control={<Switch checked={this.state.checkedB} onChange={this.handleChange('checkedB')}  value="checkedB" className="heater" />}
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