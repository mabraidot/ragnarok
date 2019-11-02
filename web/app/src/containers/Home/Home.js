import React, { Component } from 'react';
import TemperatureGauge from '../../components/TemperatureGauge';
import './Home.scss';

class Home extends Component {

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