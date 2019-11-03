import io from 'socket.io-client';

const BASE_URI = 'http://localhost:5000/ws';

class webSocket {
  constructor() {
      this.state.socket = io(BASE_URI, {})
  }

  componentDidMount() {
    const { socket } = this.state;
    socket.on('connect', () => {
        console.log('Socket connected!');
        socket.emit('Sucessfully connected!');
    });
  }
}

export default new webSocket();