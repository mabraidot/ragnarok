import React, { Component } from 'react';
import './Home.scss';
import TemperatureGauge from '../../components/TemperatureGauge';

const BASE_URI = 'ws://localhost:8000/ws';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      socket: new WebSocket(BASE_URI)
    };
  }

  componentDidMount() {
    const { socket } = this.state;
    socket.onopen = () => {
        console.log('WS: Socket connected!');
    };
    socket.onmessage = (result) => {
      console.log('WS: message!:', result.data);
    };
    socket.onerror = (error) => {
      console.log('WS: error!:', error.message);
      socket.close();
    };
    socket.onclose = (close) => {
      console.log('WS: Closing:', close.code, close.reason);
    };
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