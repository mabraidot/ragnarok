import axios from 'axios';

const BASE_URI = `http://${window.location.hostname}:8000`;

const client = axios.create({
  baseURL: BASE_URI,
  json: true
});

class ApiClient {
  
  async sendBeerXML(xml = '') {

    return client({
      method: 'POST',
      url: '/recipes/import',
      data: xml
    }).then(resp => {
      return resp.data;
    })
  }


  async cook(recipeId) {

    return client({
      method: 'GET',
      url: `/cook/${recipeId}`,
    }).then(resp => {
      return resp.data;
    })
  }


  async powerOff() {

    return client({
      method: 'GET',
      url: `/power/off`,
    }).then(resp => {
      return resp.data;
    })
  }


  async cookResume() {

    return client({
      method: 'GET',
      url: `/cook/resume`,
    }).then(resp => {
      return resp.data;
    })
  }


  async cookStop() {

    return client({
      method: 'GET',
      url: `/cook/stop`,
    }).then(resp => {
      return resp.data;
    })
  }


  async deleteRecipe(recipeId) {

    return client({
      method: 'GET',
      url: `/recipes/${recipeId}/delete`,
    }).then(resp => {
      return resp.data;
    })
  }

  async getRecipes() {

    return client({
      method: 'POST',
      url: '/recipes/list',
    }).then(resp => {
      return resp.data;
    })
  }


  async startPIDAutotune(hardware = 'MashTun') {

    let url = '';
    if (hardware === 'MashTun') {
      url = '/mashtun/PIDAutoTune';
    } else {
      url = '/boilkettle/PIDAutoTune';
    }

    return client({
      method: 'GET',
      url,
      data: null
    }).then(resp => {
      return resp.data;
    })
  }


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
      return resp.data;
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
      case 'BoilKettleValveReturn':
        url = `/boilkettle/valve/set/return/${(newValue) ? 100 : 0}`;
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
      return resp.data;
    })
  };


}

export default new ApiClient();