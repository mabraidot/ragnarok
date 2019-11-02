import axios from 'axios';

const BASE_URI = 'http://localhost:5000';

const client = axios.create({
  baseURL: BASE_URI,
  json: true
});

class homeApi {
  constructor() {}

  async getMashTunTemperature() {
    return client({
      method: 'GET',
      url: '/mashtun/get/temperature',
      data: null
    }).then(resp => {
      return resp.data.temperature ? resp.data.temperature : 0;
    })
  };
}

export default homeApi;