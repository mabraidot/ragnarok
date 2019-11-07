import React, { Component } from 'react';
import './TemperatureGauge.scss';

class TemperatureGauge extends Component {
  constructor(props) {
    super(props);
    this.state = {
      id: props.id,
      title: props.title
    };
  }
  
  // async componentDidMount() {
  // }

  render() {
    return(
      <div>
        <h3>{this.state.title}</h3>
        <p>{this.props.value}°</p>
      </div>
    );
  }
}

export default TemperatureGauge;