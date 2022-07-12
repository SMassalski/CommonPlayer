"""Tests associated with browser client functionality."""
import sys
import unittest

import mock
from ..client import BrowserClient

sys.path.append("..")

# TODO: Mock server


class ClientTests(unittest.TestCase):
    """Tests for BrowserClient class."""

    # docstr-coverage:inherited
    def setUp(self) -> None:
        self.client = BrowserClient(address="./test.sock")

    # docstr-coverage:inherited
    def tearDown(self) -> None:
        if self.client.socket is not None:
            self.client.socket.close()

    def test_client_send_called(self):
        """send() method calls socket.send()"""
        data = {"msg": "test"}
        with mock.patch.object(self.client, "socket"):
            self.client.socket.recv.return_value = b'{"msg": "test"}'
            self.client.send(data)
            self.client.socket.send.assert_called_with(b'{"msg": "test"}')

    def test_client_send_response(self):
        """send() method waits for and parses response"""
        data = {"msg": "test"}
        with mock.patch.object(self.client, "socket"):
            self.client.socket.recv.return_value = b'{"msg": "test"}'
            response = self.client.send(data)
            self.client.socket.recv.assert_called()
        self.assertEqual(response, data)
