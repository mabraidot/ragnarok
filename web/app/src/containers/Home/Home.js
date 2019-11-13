import React, { Component } from 'react';
import './Home.scss';
import Grid from '@material-ui/core/Grid';
import Grow from '@material-ui/core/Grow';
import TemperatureGauge from '../../components/TemperatureGauge';
import Gauge from '../../components/Gauge';

const BASE_URI = 'ws://localhost:8000/ws';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      socket: new WebSocket(BASE_URI),
      MashTunTemperatureSetPoint: 65,
      MashTunTemperatureProbe: 23.2,
      MashTunWaterSetPoint: 14.5,
      MashTunWaterProbe: 12.8,
      MashTunTimeSetPoint: 9.5,
      MashTunTimeProbe: 5.2,

      BoilKettleTemperatureSetPoint: 100,
      BoilKettleTemperatureProbe: 99.8,
      BoilKettleWaterSetPoint: 7.5,
      BoilKettleWaterProbe: 3.4,
      BoilKettleTimeSetPoint: 60.0,
      BoilKettleTimeProbe: 20.5,
    };
  }

  componentDidMount() {
    const { socket } = this.state;
    socket.onopen = () => {
        console.log('[WS]: Socket connected!');
    };
    socket.onmessage = (result) => {
      const data = JSON.parse(result.data)
      if (data.MashTunTemperatureProbe) {
        this.setState({MashTunTemperatureProbe: data.MashTunTemperatureProbe});
      }
      if (data.BoilKettleTemperatureProbe) {
        this.setState({BoilKettleTemperatureProbe: data.BoilKettleTemperatureProbe});
      }
      console.log('[WS]: message!:', data, data[0]);
    };
    socket.onerror = (error) => {
      console.log('[WS]: error!:', error.message);
      socket.close();
    };
    socket.onclose = (close) => {
      console.log('[WS]: Closing:', close.code, close.reason);
    };
  }

  componentWillUnmount() {
    const { socket } = this.state;
    socket.close();
  }

  render() {
    const { 
      MashTunTemperatureSetPoint, 
      MashTunTemperatureProbe, 
      MashTunWaterSetPoint, 
      MashTunWaterProbe, 
      MashTunTimeSetPoint, 
      MashTunTimeProbe, 

      BoilKettleTemperatureSetPoint, 
      BoilKettleTemperatureProbe, 
      BoilKettleWaterSetPoint, 
      BoilKettleWaterProbe, 
      BoilKettleTimeSetPoint, 
      BoilKettleTimeProbe, 
    } = this.state;
    return(
      <Grow in={true}>
        <div className="Home">
          {/* <h1>Home Screen</h1>
          <p>The Ragnarök is coming ...</p> */}
          <Grid container justify="space-evenly">
            <Gauge
              id='MashTunGauge'
              title='Mash Tun'
              setPointTemperature={MashTunTemperatureSetPoint}
              valueTemperature={MashTunTemperatureProbe}
              setPointWater={MashTunWaterSetPoint}
              valueWater={MashTunWaterProbe}
              setPointTime={MashTunTimeSetPoint}
              valueTime={MashTunTimeProbe}
              focus={true}
            />
            <Gauge
              id='BoilKettleGauge'
              title='Boil Kettle'
              setPointTemperature={BoilKettleTemperatureSetPoint}
              valueTemperature={BoilKettleTemperatureProbe}
              setPointWater={BoilKettleWaterSetPoint}
              valueWater={BoilKettleWaterProbe}
              setPointTime={BoilKettleTimeSetPoint}
              valueTime={BoilKettleTimeProbe}
              focus={false}
            />
            {/* <TemperatureGauge id='MashTunTemperatureGauge' title='Mash Tun' setPoint={65} value={MashTunTemperatureProbe} />
            <TemperatureGauge id='BoilKettleTemperatureGauge' title='Boil Kettle' setPoint={100} value={BoilKettleTemperatureProbe} /> */}
          </Grid>
        </div>
      </Grow>
    );
  }
}

export default Home;