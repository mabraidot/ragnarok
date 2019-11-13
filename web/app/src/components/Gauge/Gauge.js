import React, { Component } from 'react';
import './Gauge.scss';
import CircularProgress from '@material-ui/core/CircularProgress';

class Gauge extends Component {
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

    const maxRadious = 74;
    const timeRadious = 74;
    const waterRadious = 64;
    const temperatureRadious = 58;

    const timeBorder = 2;
    const waterBorder = 1;
    const temperatureBorder = 2;

    const timeColour = "gold";
    const waterColour = "aqua";
    const temperatureColour = "crimson";

    const setPointTimeStyle = {
      width: `${timeRadious}vw`,
      height: `${timeRadious}vw`,
      color: timeColour,
      opacity: "0.1",
      position: "absolute",
      top: `${(maxRadious-timeRadious)/2}vw`,
      left: `${(maxRadious-timeRadious)/2}vw`,
      zIndex: "0",
    };
    const currentTimeStyle = {
      width: `${timeRadious}vw`,
      height: `${timeRadious}vw`,
      color: timeColour,
      position: "absolute",
      top: `${(maxRadious-timeRadious)/2}vw`,
      left: `${(maxRadious-timeRadious)/2}vw`,
      zIndex: "0",
    };

    const setPointWaterStyle = {
      width: `${waterRadious}vw`,
      height: `${waterRadious}vw`,
      color: waterColour,
      opacity: "0.1",
      position: "absolute",
      top: `${(maxRadious-waterRadious)/2}vw`,
      left: `${(maxRadious-waterRadious)/2}vw`,
      zIndex: "0",
    };
    const currentWaterStyle = {
      width: `${waterRadious}vw`,
      height: `${waterRadious}vw`,
      color: waterColour,
      position: "absolute",
      top: `${(maxRadious-waterRadious)/2}vw`,
      left: `${(maxRadious-waterRadious)/2}vw`,
      zIndex: "0",
    };

    const setPointTemperatureStyle = {
      width: `${temperatureRadious}vw`,
      height: `${temperatureRadious}vw`,
      color: temperatureColour,
      opacity: "0.1",
      position: "absolute",
      top: `${(maxRadious-temperatureRadious)/2}vw`,
      left: `${(maxRadious-temperatureRadious)/2}vw`,
      zIndex: "0",
    };
    const currentTemperatureStyle = {
      width: `${temperatureRadious}vw`,
      height: `${temperatureRadious}vw`,
      color: temperatureColour,
      position: "absolute",
      top: `${(maxRadious-temperatureRadious)/2}vw`,
      left: `${(maxRadious-temperatureRadious)/2}vw`,
      zIndex: "0",
    };

    const componentStyle = {
      justifyContent: 'center',
      position: 'relative',
      width: `${maxRadious}vw`,
      verticalAlign: 'top',
    }
    const labelsStyle = {
      height: `${maxRadious}vw`,
      zIndex: '10',
      justifyContent: 'center',
      display: 'flex',
      flex: '1',
      flexDirection: 'column',
    }
    const labelsCurrentStyle = {
      fontSize: '13vw',
      fontWeight: 'bold',
    }

    return(
      <div className="Gauge">
        <h3>{this.state.title}</h3>
        <div style={componentStyle}>
          <CircularProgress style={setPointTimeStyle} thickness={timeBorder} variant="static" value={100} />
          <CircularProgress style={currentTimeStyle} thickness={timeBorder} variant="static" value={55} />

          <CircularProgress style={setPointWaterStyle} thickness={waterBorder} variant="static" value={100} />
          <CircularProgress style={currentWaterStyle} thickness={waterBorder} variant="static" value={75} />

          <CircularProgress style={setPointTemperatureStyle} thickness={temperatureBorder} variant="static" value={100} />
          <CircularProgress style={currentTemperatureStyle} thickness={temperatureBorder} variant="static" value={currentTemp} />
          <div style={labelsStyle}>
            <div style={labelsCurrentStyle}>{this.props.value}°</div>
            <div className="setPoint">{this.state.setPoint}°</div>
          </div>
        </div>
      </div>
    );
  }
}

export default Gauge;