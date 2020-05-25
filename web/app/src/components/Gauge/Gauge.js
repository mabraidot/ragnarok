import React, { Component } from 'react';
import './Gauge.scss';
import CircularProgress from '@material-ui/core/CircularProgress';

class Gauge extends Component {
  constructor(props) {
    super(props);
    this.state = {
      id: props.id,
      title: props.title,
    };
  }

  intToMinutes(number) {
    let time = `00:00`;
    if (Number(number) > 0.001) {
      const minutes = parseInt(Number(number));
      const seconds = Math.floor((Number(number)-minutes) * 60);
      time = `${minutes.toString().padStart(2,"00")}:${seconds.toString().padStart(2,"00")}`;
    }
    return time
  }

  render() {

    let currentTemp = this.props.valueTemperature * 100 / 125;
    let currentTime = this.props.valueTime * 100 / 120;
    let currentWater = this.props.valueWater * 100 / 16;

    const multiplier = (this.props.focus) ? 1 : 0.4 ;
    const maxDiameter = 80 * multiplier;
    const timeDiameter = 80 * multiplier;
    const waterDiameter = 70 * multiplier;
    const temperatureDiameter = 64 * multiplier;
    const fontSize = 4.4 * multiplier;
    const fontSizeBig = 12 * multiplier;

    const timeBorder = 1.8;
    const waterBorder = 1;
    const temperatureBorder = 2;

    const timeColour = "gold";
    const waterColour = "aqua";
    const temperatureColour = "crimson";

    const setPointTimeStyle = {
      width: `${timeDiameter}vw`,
      height: `${timeDiameter}vw`,
      color: timeColour,
      opacity: "0.1",
      position: "absolute",
      top: `${(maxDiameter-timeDiameter)/2}vw`,
      left: `${(maxDiameter-timeDiameter)/2}vw`,
      zIndex: "0",
    };
    const currentTimeStyle = {
      width: `${timeDiameter}vw`,
      height: `${timeDiameter}vw`,
      color: timeColour,
      position: "absolute",
      top: `${(maxDiameter-timeDiameter)/2}vw`,
      left: `${(maxDiameter-timeDiameter)/2}vw`,
      zIndex: "0",
    };

    const setPointWaterStyle = {
      width: `${waterDiameter}vw`,
      height: `${waterDiameter}vw`,
      color: waterColour,
      opacity: "0.1",
      position: "absolute",
      top: `${(maxDiameter-waterDiameter)/2}vw`,
      left: `${(maxDiameter-waterDiameter)/2}vw`,
      zIndex: "0",
    };
    const currentWaterStyle = {
      width: `${waterDiameter}vw`,
      height: `${waterDiameter}vw`,
      color: waterColour,
      position: "absolute",
      top: `${(maxDiameter-waterDiameter)/2}vw`,
      left: `${(maxDiameter-waterDiameter)/2}vw`,
      zIndex: "0",
    };

    const setPointTemperatureStyle = {
      width: `${temperatureDiameter}vw`,
      height: `${temperatureDiameter}vw`,
      color: temperatureColour,
      opacity: "0.1",
      position: "absolute",
      top: `${(maxDiameter-temperatureDiameter)/2}vw`,
      left: `${(maxDiameter-temperatureDiameter)/2}vw`,
      zIndex: "0",
    };
    const currentTemperatureStyle = {
      width: `${temperatureDiameter}vw`,
      height: `${temperatureDiameter}vw`,
      color: temperatureColour,
      position: "absolute",
      top: `${(maxDiameter-temperatureDiameter)/2}vw`,
      left: `${(maxDiameter-temperatureDiameter)/2}vw`,
      zIndex: "0",
    };

    const componentStyle = {
      justifyContent: 'center',
      position: 'relative',
      width: `${maxDiameter}vw`,
      verticalAlign: 'top',
      height: `${(maxDiameter/7)*5}vw`,
      paddingTop: `${(maxDiameter/7)*2}vw`,
    }
    const labelsStyle = {
      zIndex: '10',
      justifyContent: 'center',
      display: 'flex',
      flex: '1',
      flexDirection: 'row',
    }
    const labelsSetPointStyle = {
      width: `${(maxDiameter/10)*4}vw`,
      textAlign: 'right',
      fontSize: `${fontSize}vw`,
      paddingRight: '0.4em',
      zIndex: '10',
    }
    const labelsCurrentStyle = {
      width: `${(maxDiameter/10)*6}vw`,
      textAlign: 'left',
      lineHeight: '1em',
      fontSize: `${fontSizeBig}vw`,
      fontWeight: 'bold',
      zIndex: '10',
    }

    const gaugeStyle = {
      order: (this.props.focus) ? '1' : '3',
      alignSelf: (this.props.focus) ? 'center' : 'flex-end',
      // transition: 'order 2s',
    }

    let title;
    if (this.props.focus) {
      title = <h2>{this.state.title}</h2>
    } else {
      title = <h5 style={{margin: '1em'}}>{this.state.title}</h5>
    }

    return(

      <div className="Gauge" style={gaugeStyle}>
        {title}
        <div style={componentStyle}>
          <CircularProgress style={setPointTimeStyle} thickness={timeBorder} variant="static" value={100} />
          <CircularProgress style={currentTimeStyle} thickness={timeBorder} variant="static" value={currentTime} />

          <CircularProgress style={setPointWaterStyle} thickness={waterBorder} variant="static" value={100} />
          <CircularProgress style={currentWaterStyle} thickness={waterBorder} variant="static" value={currentWater} />

          <CircularProgress style={setPointTemperatureStyle} thickness={temperatureBorder} variant="static" value={100} />
          <CircularProgress style={currentTemperatureStyle} thickness={temperatureBorder} variant="static" value={currentTemp} />
          <div style={labelsStyle}>
            <div style={labelsSetPointStyle}><span style={{fontSize: '0.5em'}}>TEMPERATURE<br /></span> <strong>{this.props.setPointTemperature}°</strong></div>
            <div style={labelsCurrentStyle}><span style={{color: temperatureColour}}>{this.props.valueTemperature}</span></div>
          </div>
          <div style={labelsStyle}>
            <div style={labelsSetPointStyle}><span style={{fontSize: '0.5em'}}>PROCESS TIME<br /></span> <strong>{this.intToMinutes(this.props.setPointTime)}</strong> </div>
            <div style={labelsCurrentStyle}><span style={{color: timeColour}}>{this.intToMinutes(this.props.valueTime)}</span></div>
          </div>
          <div style={labelsStyle}>
            <div style={labelsSetPointStyle}><span style={{fontSize: '0.5em'}}>WATER VOLUME<br /></span> <strong>{this.props.setPointWater} L</strong> </div>
            <div style={labelsCurrentStyle}><span style={{color: waterColour}}>{this.props.valueWater}</span></div>
          </div>
        </div>
      </div>
    );
  }
}

export default Gauge;