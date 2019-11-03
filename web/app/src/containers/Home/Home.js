import React, { Component } from 'react';
import './Home.scss';
import TemperatureGauge from '../../components/TemperatureGauge';
import io from 'socket.io-client';

const BASE_URI = 'ws://localhost:8000/ws';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      socket: io(BASE_URI, {})
    };
  }

  componentDidMount() {
    const { socket } = this.state;
    socket.on('connect', () => {
        console.log('Socket connected!');
        socket.emit('Sucessfully connected!');
    });
    socket.on('message', (result) => {
      console.log('message!:', result);
      socket.emit('Sucessfully recevied!');
    });
  }

  render() {
    return(
      <div>
        <p>
          The Ragnarök is coming ...
        </p>
        <TemperatureGauge />
      </div>
    );
  }
}

export default Home;