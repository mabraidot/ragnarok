import axios from 'axios';

const BASE_URI = 'http://localhost:8000';

const client = axios.create({
  baseURL: BASE_URI,
  json: true
});

class ApiClient {
  
  async setPoint(hardware = 'MashTunTemperatureSetPoint', newValue = 0) {

    let url;
    switch (hardware) {
      default:
      case 'MashTunTemperatureSetPoint':
        url = `/mashtun/set/temperature/${newValue}`;
        break;
      case 'MashTunWaterLevelSetPoint':
        url = `/mashtun/set/water/${newValue}`;
        break;

      case 'MashTunTimeSetPoint':
        url = `/mashtun/set/time/${newValue}`;
        break;

      case 'BoilKettleTemperatureSetPoint':
        url = `/boilkettle/set/temperature/${newValue}`;
        break;

      case 'BoilKettleWaterLevelSetPoint':
        url = `/boilkettle/set/water/${newValue}`;
        break;

      case 'BoilKettleTimeSetPoint':
        url = `/boilkettle/set/time/${newValue}`;
        break;
    }

    return client({
      method: 'GET',
      url,
      data: null
    }).then(resp => {
      if (resp.data.error) {
        return resp.data.error;
      } else {
        return resp.data.response;
      }
    })
  };


  async setSwitch(hardware = 'MashTunValveInlet', newValue = false) {
    
    let url;
    switch (hardware) {
      case 'MashTunHeater':
        url = `/mashtun/set/heater/${newValue}`;
        break;
      case 'MashTunValveInlet':
        url = `/mashtun/valve/set/inlet/${(newValue) ? 100 : 0}`;
        break;
      case 'MashTunValveOutlet':
        url = `/mashtun/valve/set/outlet/${(newValue) ? 100 : 0}`;
        break;
      case 'BoilKettleHeater':
        url = `/boilkettle/set/heater/${newValue}`;
        break;
      case 'BoilKettleValveWater':
        url = `/boilkettle/valve/set/water/${(newValue) ? 100 : 0}`;
        break;
      case 'BoilKettleValveInlet':
        url = `/boilkettle/valve/set/inlet/${(newValue) ? 100 : 0}`;
        break;
      case 'BoilKettleValveOutlet':
        url = `/boilkettle/valve/set/outlet/${(newValue) ? 100 : 0}`;
        break;
      case 'ChillerValveWater':
        url = `/chiller/set/water/${(newValue) ? 100 : 0}`;
        break;
      case 'ChillerValveWort':
        url = `/chiller/set/wort/${(newValue) ? 100 : 0}`;
        break;
      case 'OutletValveDump':
        url = `/outlet/set/${(newValue) ? 100 : 0}`;
        break;
      default:
      case 'Pump':
        url = `/pump/set/${newValue}`;
        break;
    }

    return client({
      method: 'GET',
      url,
      data: null
    }).then(resp => {
      if (resp.data.error) {
        return resp.data.error;
      } else {
        return resp.data.response;
      }
    })
  };


}

export default new ApiClient();