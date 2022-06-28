import sys
import unittest

import mock
from ..client import BrowserClient

sys.path.append('..')


class ClientTests(unittest.TestCase):
    
    def setUp(self) -> None:
        self.client = BrowserClient(9999)
        self.host = self.client.host

    def tearDown(self) -> None:
        if self.client.socket is not None:
            self.client.socket.close()
            
    def test_client_send_called(self):
        data = {'msg': 'test'}
        with mock.patch.object(self.client, 'socket'):
            self.client.socket.recv.return_value = b'{"msg": "test"}'
            self.client.send(data)
            self.client.socket.send.assert_called_with(b'{"msg": "test"}')
        
    def test_client_send_response(self):
        data = {'msg': 'test'}
        with mock.patch.object(self.client, 'socket'):
            self.client.socket.recv.return_value = b'{"msg": "test"}'
            response = self.client.send(data)
            self.client.socket.recv.assert_called()
        self.assertEqual(response, data)
        
    @mock.patch('api.client.socket')
    def test_client_enter_context_creates_socket(self, mock_socket):
        with self.client:
            pass
        mock_socket.socket.assert_called()

    @mock.patch('api.client.socket')
    def test_client_enter_context_connects(self, _):
        with self.client:
            self.client.socket.connect.assert_called_with((self.host, 9999))

    @unittest.skip('Not sure how to implement')
    def test_client_exit_context_closes_socket(self, mock_socket):
        pass

    @mock.patch('api.client.socket')
    def test_client_exit_context_removes_socket(self, _):
        with self.client:
            pass
        self.assertIsNone(self.client.socket)
