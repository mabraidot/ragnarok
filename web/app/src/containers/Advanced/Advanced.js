import React, { Component } from 'react';
import './Advanced.scss';
import Grow from '@material-ui/core/Grow';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Paper from '@material-ui/core/Paper';
import Slider from '@material-ui/core/Slider';

class Advanced extends Component {
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
          <h2>Advanced Mode</h2>
          <Grid container>

            <Grid item xs={6}>
              <Paper elevation={2}>
                <h4>Mash Tun</h4>
                <Slider
                  className="temperature"
                  defaultValue={0}
                  aria-labelledby="discrete-slider-always"
                  step={1}
                  max={marksTemperature[4].value}
                  marks={marksTemperature}
                  valueLabelDisplay="auto"
                />
                <div className="label">Temperature</div>

                <Slider
                  className="water"
                  defaultValue={0}
                  aria-labelledby="discrete-slider-always"
                  step={0.1}
                  max={marksWater[4].value}
                  marks={marksWater}
                  valueLabelDisplay="auto"
                />
                <div className="label">Water level</div>

                <Slider
                  className="time"
                  defaultValue={0}
                  aria-labelledby="discrete-slider-always"
                  step={1}
                  max={marksTime[4].value}
                  marks={marksTime}
                  valueLabelDisplay="auto"
                />
                <div className="label">Process time</div>

                <Button variant="contained" className="button-set">Inlet</Button>
                <Button variant="contained" className="button-set">Outlet</Button>
              </Paper>
            </Grid>
            
            
            {/* <Grid item xs={12}>
              <h4>Mash Tun</h4>
            </Grid>
            <Grid item xs={4}>
              <Paper elevation={2}>
                <div>Temperature</div>
                <Button variant="contained" className="button-set">Set</Button>
                <Button variant="contained" className="button-stop" disabled>Stop</Button>
              </Paper>
            </Grid>
            <Grid item xs={4}>
              <Paper elevation={2}>
                <div>Water</div>
                <Button variant="contained" className="button-set">Set</Button>
                <Button variant="contained" className="button-stop">Stop</Button>
              </Paper>
            </Grid>
            <Grid item xs={4}>
              <Paper elevation={2}>
                <div>Time</div>
                <Button variant="contained" className="button-set">Set</Button>
                <Button variant="contained" className="button-stop">Stop</Button>
              </Paper>
            </Grid>


            <Grid item xs={12}>
              <h4>Boil Kettle</h4>
            </Grid> */}

            <Grid item xs={6}>
              <Paper elevation={2}>
                <h4>Boil Kettle</h4>
                <Slider
                  className="temperature"
                  defaultValue={0}
                  aria-labelledby="discrete-slider-always"
                  step={1}
                  max={marksTemperature[4].value}
                  marks={marksTemperature}
                  valueLabelDisplay="auto"
                />
                <div className="label">Temperature</div>

                <Slider
                  className="water"
                  defaultValue={0}
                  aria-labelledby="discrete-slider-always"
                  step={0.1}
                  max={marksWater[4].value}
                  marks={marksWater}
                  valueLabelDisplay="auto"
                />
                <div className="label">Water level</div>

                <Slider
                  className="time"
                  defaultValue={0}
                  aria-labelledby="discrete-slider-always"
                  step={1}
                  max={marksTime[4].value}
                  marks={marksTime}
                  valueLabelDisplay="auto"
                />
                <div className="label">Process time</div>

                <Button variant="contained" className="button-set">Inlet</Button>
                <Button variant="contained" className="button-set">Pump In</Button>
                <Button variant="contained" className="button-set">Outlet</Button>
              </Paper>
            </Grid>

            <Grid item xs={4}>
              <Paper elevation={2}>
                <h4>Pump</h4>
                <Button variant="contained" className="button-set">Motor</Button>
              </Paper>
            </Grid>

            <Grid item xs={4}>
              <Paper elevation={2}>
                <h4>Outlet</h4>
                <Button variant="contained" className="button-set">Dump</Button>
              </Paper>
            </Grid>

            <Grid item xs={4}>
              <Paper elevation={2}>
                <h4>Chiller</h4>
                <Button variant="contained" className="button-set">Water</Button>
                <Button variant="contained" className="button-set">Wort</Button>
              </Paper>
            </Grid>


          </Grid>
        </div>
      </Grow>
    );
  }
}

export default Advanced;