import React, { Component } from 'react';
import './TemperatureGauge.scss';
import homeApi from '../../apiClient/homeApi';

class TemperatureGauge extends Component {
  constructor(props) {
    super(props);
    this.state = {
      id: props.id,
      value: 0,
    };
  }
  
  async componentDidMount() {
    this.homeApi = new homeApi();
    this.homeApi.getMashTunTemperature().then((data) => {
      this.setState({ value: data });
    });
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