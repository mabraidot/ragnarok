import React, { Component } from 'react';
import './TemperatureGauge.scss';
import CircularProgress from '@material-ui/core/CircularProgress';

class TemperatureGauge extends Component {
  constructor(props) {
    super(props);
    this.state = {
      id: props.id,
      title: props.title,
      setPoint: props.setPoint || 100
    };
  }
  
  // async componentDidMount() {
  // }

  render() {
    let currentTemp = this.props.value * 100 / this.state.setPoint;

    return(
      <div className="TemperatureGauge">
        <h3>{this.state.title}</h3>
        <div className="gauge">
          <CircularProgress className="setPointGauge" size="9em" thickness={3} variant="static" value={100} />
          <CircularProgress className="currentGauge" size="9em" thickness={3} variant="static" value={currentTemp} />
          <div className="temperature">
            <div><span className="current">{this.props.value}</span><span>o</span></div>
            <div className="setPoint">{this.state.setPoint}°</div>
          </div>
        </div>
      </div>
    );
  }
}

export default TemperatureGauge;