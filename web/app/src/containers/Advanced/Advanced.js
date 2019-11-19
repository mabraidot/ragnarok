import React, { Component } from 'react';
import './Advanced.scss';
import Grow from '@material-ui/core/Grow';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';

class Advanced extends Component {

  render() {
    return(
      <Grow in={true}>
        <div className="Advanced">
          <h2>Advanced Mode</h2>
          <Grid container space={5}>

            <Grid item xs={12}>
              <h4>Mash Tun</h4>
            </Grid>
            <Grid item xs={4}>
              <div>Temperature</div>
              <Button variant="contained" className="button-set">Set</Button>
              <Button variant="contained" className="button-stop" disabled>Stop</Button>
            </Grid>
            <Grid item xs={4}>
              <div>Water</div>
              <Button variant="contained" className="button-set">Set</Button>
              <Button variant="contained" className="button-stop">Stop</Button>
            </Grid>
            <Grid item xs={4}>
              <div>Time</div>
              <Button variant="contained" className="button-set">Set</Button>
              <Button variant="contained" className="button-stop">Stop</Button>
            </Grid>


            <Grid item xs={12}>
              <h4>Boil Kettle</h4>
            </Grid>

          </Grid>
        </div>
      </Grow>
    );
  }
}

export default Advanced;