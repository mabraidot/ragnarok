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
      MashTunTemperatureProbe: 0,
      BoilKettleTemperatureProbe: 0
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
    const { MashTunTemperatureProbe, BoilKettleTemperatureProbe } = this.state;
    return(
      <Grow in={true}>
        <div className="Home">
          {/* <h1>Home Screen</h1>
          <p>The Ragnarök is coming ...</p> */}
          <Grid container justify="space-evenly">
            <Gauge id='MashTunGauge' title='Mash Tun' setPoint={65} value={24} />
            <TemperatureGauge id='MashTunTemperatureGauge' title='Mash Tun' setPoint={65} value={MashTunTemperatureProbe} />
            <TemperatureGauge id='BoilKettleTemperatureGauge' title='Boil Kettle' setPoint={100} value={BoilKettleTemperatureProbe} />
          </Grid>
        </div>
      </Grow>
    );
  }
}

export default Home;