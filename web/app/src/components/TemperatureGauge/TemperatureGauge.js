import React, { Component } from 'react';
import './TemperatureGauge.scss';

class TemperatureGauge extends Component {
  constructor(props) {
    super(props);
    this.state = {
      id: props.id,
      value: 0,
    };
  }

  render() {
    const { value } = this.state
    return(
      <div>
        <p>{value}°</p>
      </div>
    );
  }
}

export default TemperatureGauge;