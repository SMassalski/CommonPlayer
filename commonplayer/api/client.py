import socket
import json


class BrowserClient:
    """Client class for communication with a browser server."""
    
    START = 'start'
    EXIT = 'exit'
    GOTO = 'go_to'
    GET = 'get_url'
    CONTROL = 'control'
    
    def __init__(self, port=7777):
        self.host = socket.gethostname()
        self.port = port
        self.socket = socket.socket()
        
    def connect(self):
        """Connect to a server."""
        self.socket.connect((self.host, self.port))
        
    def send(self, value, receive=True):
        """Send data to the connected server.
        
        Parameters
        ----------
        value : dict
            Data to be sent to the server.
        receive : bool
            Whether to expect a response.
        Returns
        -------
        dict
            The received response. None if `receive` is False.
        """
        data = json.dumps(value)
        self.socket.send(data.encode())
        if receive:
            return self.response()
        return None
        
    def close(self):
        """Close the server connection."""
        self.socket.close()
        
    def response(self):
        """Await for a response and return it.
        
        Returns
        -------
        dict
            The received data.
        """
        data = self.socket.recv(1024).decode()
        return json.loads(data)
