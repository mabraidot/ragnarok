import React, { Component } from 'react';
import './TemperatureGauge.scss';

class TemperatureGauge extends Component {
  constructor(props) {
    super(props);
    this.state = {
      id: props.id,
    };
  }
  
  // async componentDidMount() {
  // }

  render() {
    return(
      <div>
        <p>{this.state.id}</p>
        <p>{this.props.value}°</p>
      </div>
    );
  }
}

export default TemperatureGauge;