import React, { Component } from 'react';
import './Home.scss';
import TemperatureGauge from '../../components/TemperatureGauge';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {};
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