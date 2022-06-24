import socket


class BrowserClient:
    """Client class for communication with a browser server."""
    
    START = 'start'
    EXIT = 'exit'
    GOTO = 'go_to'
    GET = 'get_url'
    
    def __init__(self, port=7777):
        self.host = socket.gethostname()
        self.port = port
        self.socket = socket.socket()
        
    def connect(self):
        """Connect to a server."""
        self.socket.connect((self.host, self.port))
        
    def send(self, value):
        """Send data to the connected server.
        
        Parameters
        ----------
        value : str
            Data to be sent to the server.
        """
        self.socket.send(value.encode())
        
    def close(self):
        """Close the server connection."""
        self.socket.close()
        
    def response(self):
        """Await for a response and return it.
        
        Returns
        -------
        str
            The received data.
        """
        data = self.socket.recv(1024).decode()
        return data
