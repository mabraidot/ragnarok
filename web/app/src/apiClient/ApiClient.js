import axios from 'axios';

const BASE_URI = 'http://localhost:8000';

const client = axios.create({
  baseURL: BASE_URI,
  json: true
});

class ApiClient {
  
  // MASH TUN ///////////////
  async setMashTunTemperature(newValue = 0) {
    return client({
      method: 'GET',
      url: `/mashtun/set/temperature/${newValue}`,
      data: null
    }).then(resp => {
      if (resp.data.error) {
        return resp.data.error;
      } else {
        return resp.data.response;
      }
    })
  };

  async setMashTunWaterLevel(newValue = 0) {
    return client({
      method: 'GET',
      url: `/mashtun/set/water/${newValue}`,
      data: null
    }).then(resp => {
      if (resp.data.error) {
        return resp.data.error;
      } else {
        return resp.data.response;
      }
    })
  };

  async setMashTunTime(newValue = 0) {
    return client({
      method: 'GET',
      url: `/mashtun/set/time/${newValue}`,
      data: null
    }).then(resp => {
      if (resp.data.error) {
        return resp.data.error;
      } else {
        return resp.data.response;
      }
    })
  };

  // BOIL KETTLE ///////////////
  async setBoilKettleTemperature(newValue = 0) {
    return client({
      method: 'GET',
      url: `/boilkettle/set/temperature/${newValue}`,
      data: null
    }).then(resp => {
      if (resp.data.error) {
        return resp.data.error;
      } else {
        return resp.data.response;
      }
    })
  };

  async setBoilKettleWaterLevel(newValue = 0) {
    return client({
      method: 'GET',
      url: `/boilkettle/set/water/${newValue}`,
      data: null
    }).then(resp => {
      if (resp.data.error) {
        return resp.data.error;
      } else {
        return resp.data.response;
      }
    })
  };

  async setBoilKettleTime(newValue = 0) {
    return client({
      method: 'GET',
      url: `/boilkettle/set/time/${newValue}`,
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