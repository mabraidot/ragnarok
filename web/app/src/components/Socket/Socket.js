const BASE_URI = `ws://${window.location.hostname}:8000/ws`;

class Socket {
  constructor() {
    this.socket = new WebSocket(BASE_URI)

    this.socket.onopen = () => {
      console.log('[WS]: Socket connected!');
    };
    
    this.socket.onerror = (error) => {
      console.log('[WS]: error!:', error.message);
      this.socket.close();
    };
    
    this.socket.onclose = (close) => {
      console.log('[WS]: Closing:', close.code, close.reason);
    };

  }

}

export default Socket;